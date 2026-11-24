#!/usr/bin/env python3
"""
Unified Asset Registry for Align Newsroom.

One registry, all asset types (audio, video, image, 3d, document).

Prevents contamination from unapproved assets:
- Every asset is registered with full provenance metadata
- Unapproved files are quarantined/deleted on schedule, never mixed with approved
- Duplicates detected by SHA256 hash
- Metadata embedded in WAV RIFF INFO chunks (audio)

Usage:
    python3 unified_registry.py register <file> [type-specific flags] [--status pending]
    python3 unified_registry.py approve <file>
    python3 unified_registry.py reject <file>
    python3 unified_registry.py supersede <old> <new>
    python3 unified_registry.py cleanup [--dry-run]
    python3 unified_registry.py status
    python3 unified_registry.py query [--type audio] [--engine chatterbox] [--status pending] ...
    python3 unified_registry.py history <family>
    python3 unified_registry.py flag --engine chatterbox --reason "..."
    python3 unified_registry.py characterize <file> --add raspy,high-energy
    python3 unified_registry.py canonical <family>
    python3 unified_registry.py tag <file>              # WAV RIFF INFO only
    python3 unified_registry.py migrate                 # import legacy registry entries

Type is auto-detected from file extension; override with --type.
Type-specific metadata:
    audio:    --voice --engine --prompt --stability --similarity-boost --style --speaker-boost
    video:    --resolution --fps --duration --codec
    image:    --dimensions --style
    3d:       --poly-count --format
    document: --doc-type
"""

import argparse
import hashlib
import json
import shutil
import sys
import wave
from datetime import datetime, timedelta
from pathlib import Path

BASE = Path(__file__).parent
REGISTRY = BASE / "registry.json"
QUARANTINE = BASE / "quarantine"
ARCHIVE = BASE / "archive"

PENDING_DAYS = 7  # pending files older than this get quarantined

AUDIO_EXTS = {".wav", ".mp3", ".m4a", ".flac", ".ogg", ".opus", ".aac", ".wma"}
VIDEO_EXTS = {".mp4", ".mov", ".mkv", ".avi", ".webm", ".m4v"}
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp",
              ".tiff", ".tif", ".heic", ".avif"}
THREE_D_EXTS = {".obj", ".stl", ".fbx", ".gltf", ".glb", ".blend", ".dae",
                ".ply", ".usd", ".usdz"}
DOC_EXTS = {".md", ".txt", ".pdf", ".docx", ".doc", ".json", ".html",
            ".htm", ".yaml", ".yml", ".csv", ".rtf"}


def detect_type(path):
    ext = Path(path).suffix.lower()
    if ext in AUDIO_EXTS:
        return "audio"
    if ext in VIDEO_EXTS:
        return "video"
    if ext in IMAGE_EXTS:
        return "image"
    if ext in THREE_D_EXTS:
        return "3d"
    if ext in DOC_EXTS:
        return "document"
    return "other"


def load_registry():
    if REGISTRY.exists():
        return json.loads(REGISTRY.read_text())
    return {"assets": {}}


def save_registry(reg):
    REGISTRY.write_text(json.dumps(reg, indent=2))


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def cmd_register(args):
    reg = load_registry()
    path = Path(args.file).resolve()
    if not path.exists():
        print(f"File not found: {path}")
        sys.exit(1)

    asset_type = args.type or detect_type(path)
    file_hash = sha256_of(path)

    # Dedupe check
    for existing_path, entry in reg["assets"].items():
        if entry.get("sha256") == file_hash and existing_path != str(path):
            print(f"DUPLICATE of {existing_path} — not registering separately")
            print(f"  Hash: {file_hash[:16]}...")
            return

    entry = {
        "type": asset_type,
        "sha256": file_hash,
        "status": args.status,
        "prompt": args.prompt,
        "created_at": datetime.now().isoformat(),
        "approved_at": None,
        "approved_by": None,
        "supersedes": None,
        "superseded_by": None,
        "is_canonical": False,
        "version": args.version,
        "family": args.family,
        "canonical_name": None,
        "characteristics": [],
    }

    # Type-specific metadata
    if asset_type == "audio":
        # audio style is a float param (e.g. 0.0); fall back to 0.0 if a
        # named style was passed
        try:
            audio_style = float(args.style)
        except (TypeError, ValueError):
            audio_style = 0.0
        entry["voice_id"] = args.voice
        entry["engine"] = args.engine
        entry["settings"] = {
            "stability": args.stability,
            "similarity_boost": args.similarity_boost,
            "style": audio_style,
            "use_speaker_boost": args.speaker_boost,
        }
    elif asset_type == "video":
        entry["resolution"] = args.resolution
        entry["fps"] = args.fps
        entry["duration_sec"] = args.duration
        entry["codec"] = args.codec
        if args.voice != "unknown":
            entry["voice_id"] = args.voice
        if args.engine != "chatterbox":
            entry["engine"] = args.engine
    elif asset_type == "image":
        # image style is a style NAME (e.g. newsprint, pencil)
        entry["dimensions"] = args.dimensions
        entry["style"] = args.style if args.style != "0.0" else "unknown"
    elif asset_type == "3d":
        entry["poly_count"] = args.poly_count
        entry["format"] = args.format or path.suffix.lower().lstrip(".")
    elif asset_type == "document":
        entry["doc_type"] = args.doc_type
    else:
        # 'other' — keep generic audio-ish fields for backward compat
        entry["voice_id"] = args.voice
        entry["engine"] = args.engine

    reg["assets"][str(path)] = entry
    save_registry(reg)
    detail = ""
    if asset_type == "audio":
        detail = f"  Voice: {args.voice} | Engine: {args.engine}"
    elif asset_type == "video":
        detail = f"  {args.resolution} @ {args.fps}fps | Codec: {args.codec}"
    elif asset_type == "image":
        detail = f"  {args.dimensions} | Style: {args.style}"
    elif asset_type == "3d":
        detail = f"  Format: {entry['format']} | Polys: {args.poly_count}"
    print(f"Registered: {path.name} [{args.status}] (type={asset_type})")
    if detail:
        print(detail)


def cmd_approve(args):
    reg = load_registry()
    path = str(Path(args.file).resolve())
    if path not in reg["assets"]:
        print(f"Not in registry: {path}")
        print("Register it first with: unified_registry.py register <file> ...")
        sys.exit(1)
    reg["assets"][path]["status"] = "approved"
    reg["assets"][path]["approved_at"] = datetime.now().isoformat()
    reg["assets"][path]["approved_by"] = args.by or "ricardo"
    save_registry(reg)
    print(f"Approved: {Path(path).name}")


def cmd_reject(args):
    reg = load_registry()
    path = Path(args.file).resolve()
    spath = str(path)
    if spath in reg["assets"]:
        reg["assets"][spath]["status"] = "rejected"
        save_registry(reg)
    if path.exists():
        path.unlink()
        print(f"Rejected and deleted: {path.name}")
    else:
        print(f"Already gone: {path.name}")


def cmd_supersede(args):
    """Mark old file as superseded by new file. Old goes to archive."""
    reg = load_registry()
    old = str(Path(args.old).resolve())
    new = str(Path(args.new).resolve())
    if old not in reg["assets"]:
        print(f"Old file not in registry: {old}")
        sys.exit(1)
    if new not in reg["assets"]:
        print(f"New file not in registry: {new}")
        sys.exit(1)
    reg["assets"][old]["status"] = "superseded"
    reg["assets"][old]["superseded_by"] = new
    reg["assets"][new]["supersedes"] = old
    save_registry(reg)
    print(f"{Path(old).name} superseded by {Path(new).name}")


def cmd_cleanup(args):
    reg = load_registry()
    now = datetime.now()
    actions = []

    for path_str, entry in list(reg["assets"].items()):
        path = Path(path_str)
        status = entry["status"]
        created = datetime.fromisoformat(entry["created_at"])

        if status == "rejected":
            if path.exists():
                if getattr(args, "scheduled", False):
                    # Unattended runs never delete: report only, Ricardo reviews
                    actions.append(("report-rejected", path, "rejected - deletion skipped (scheduled mode)"))
                else:
                    actions.append(("delete", path, "rejected"))
                    if not args.dry_run:
                        path.unlink()

        elif status == "pending" and (now - created) > timedelta(days=PENDING_DAYS):
            QUARANTINE.mkdir(exist_ok=True)
            dest = QUARANTINE / path.name
            if path.exists():
                actions.append(("quarantine", path, f"pending > {PENDING_DAYS}d"))
                if not args.dry_run:
                    shutil.move(str(path), str(dest))
                    # Update registry path
                    reg["assets"][str(dest)] = entry
                    del reg["assets"][path_str]

        elif status == "superseded":
            ARCHIVE.mkdir(exist_ok=True)
            dest = ARCHIVE / path.name
            # Only archive if the replacement is approved
            new_path = entry.get("superseded_by")
            if new_path and reg["assets"].get(new_path, {}).get("status") == "approved":
                if path.exists() and not dest.exists():
                    actions.append(("archive", path, "superseded by approved"))
                    if not args.dry_run:
                        shutil.move(str(path), str(dest))
                        reg["assets"][str(dest)] = entry
                        del reg["assets"][path_str]

    # Dedupe: find same-hash files, keep the approved one
    by_hash = {}
    for path_str, entry in reg["assets"].items():
        h = entry.get("sha256")
        if h:
            by_hash.setdefault(h, []).append((path_str, entry))

    for h, items in by_hash.items():
        if len(items) > 1:
            # Sort: approved first, then newest
            items.sort(key=lambda x: (
                0 if x[1]["status"] == "approved" else 1,
                x[1]["created_at"],
            ), reverse=False)
            keep = items[0]
            for dup_path_str, dup_entry in items[1:]:
                dup_path = Path(dup_path_str)
                if getattr(args, "scheduled", False):
                    # Unattended runs flag duplicates for Ricardo's review - never delete
                    actions.append(("flag-duplicate", dup_path, f"duplicate of {Path(keep[0]).name} - flagged, not deleted"))
                    if not args.dry_run:
                        dup_entry["duplicate_of"] = keep[0]
                        dup_entry["duplicate_flagged_at"] = now.isoformat()
                else:
                    actions.append(("dedupe", dup_path, f"duplicate of {Path(keep[0]).name}"))
                    if not args.dry_run and dup_path.exists():
                        dup_path.unlink()
                        del reg["assets"][dup_path_str]

    if not args.dry_run:
        save_registry(reg)

    if actions:
        print(f"{'[DRY RUN] ' if args.dry_run else ''}Cleanup actions:")
        for action, path, reason in actions:
            print(f"  {action.upper():12} {path.name} ({reason})")
    else:
        print("Nothing to clean.")


def cmd_status(args):
    reg = load_registry()
    by_status = {}
    by_type = {}
    for entry in reg["assets"].values():
        s = entry.get("status", "?")
        t = entry.get("type", "?")
        by_status[s] = by_status.get(s, 0) + 1
        by_type[t] = by_type.get(t, 0) + 1
    print("Registry status:")
    for s, c in sorted(by_status.items()):
        print(f"  {s}: {c}")
    print("By type:")
    for t, c in sorted(by_type.items()):
        print(f"  {t}: {c}")
    print(f"  total: {len(reg['assets'])}")


def cmd_canonical(args):
    """Mark the latest approved version of an asset family as canonical.
    Creates a stable symlink (e.g., intro-latest.wav -> align-intro-v12.wav)
    so consumers always get the approved version without tracking versions."""
    reg = load_registry()

    # Find all versions of this asset family
    family = args.family
    versions = []
    for path_str, entry in reg["assets"].items():
        # Match by family name in filename or explicit family tag
        fname = Path(path_str).name
        if family in fname or entry.get("family") == family:
            versions.append((path_str, entry))

    if not versions:
        print(f"No assets found for family: {family}")
        sys.exit(1)

    # Sort by version, find latest approved
    versions.sort(key=lambda x: x[1].get("version", 1))
    approved = [(p, e) for p, e in versions if e["status"] == "approved"]
    if not approved:
        print(f"No approved versions for family: {family}")
        sys.exit(1)

    latest_path, latest_entry = approved[-1]

    # Clear canonical flag on all, set on latest
    for _, e in versions:
        e["is_canonical"] = False
    latest_entry["is_canonical"] = True

    # Create/update symlink
    link_dir = Path(latest_path).parent
    ext = Path(latest_path).suffix
    link_name = f"{family}-latest{ext}"
    link_path = link_dir / link_name

    if link_path.is_symlink() or link_path.exists():
        link_path.unlink()
    link_path.symlink_to(Path(latest_path).name)

    save_registry(reg)
    print(f"Canonical: {link_name} -> {Path(latest_path).name}")
    print(f"  {len(versions)} versions, {len(approved)} approved")


def cmd_query(args):
    """Query assets by metadata. Examples:
    unified_registry.py query --engine chatterbox
    unified_registry.py query --type image --status approved
    unified_registry.py query --characteristic raspy
    unified_registry.py query --engine elevenlabs --format table
    """
    reg = load_registry()
    results = []
    for path_str, entry in reg["assets"].items():
        match = True
        if args.type and entry.get("type") != args.type:
            match = False
        if args.engine and entry.get("engine") != args.engine:
            match = False
        if args.status and entry.get("status") != args.status:
            match = False
        if args.family and entry.get("family") != args.family:
            match = False
        if args.voice and args.voice not in entry.get("voice_id", ""):
            match = False
        if args.characteristic:
            chars = entry.get("characteristics", [])
            if args.characteristic not in chars:
                match = False
        if args.style and entry.get("style") != args.style:
            match = False
        if match:
            results.append((path_str, entry))

    if args.format == "table":
        print(f"{'File':<40} {'Type':<8} {'Status':<12} {'Voice/Detail':<30} {'Chars'}")
        print("-" * 125)
        for path_str, e in results:
            chars = ",".join(e.get("characteristics", []))
            detail = e.get("voice_id", "") or e.get("style", "") or e.get("resolution", "")
            print(f"{Path(path_str).name:<40} {e.get('type',''):<8} "
                  f"{e['status']:<12} {detail:<30} {chars}")
    elif args.format == "paths":
        for path_str, _ in results:
            print(path_str)
    else:  # json
        print(json.dumps({p: e for p, e in results}, indent=2))

    print(f"\n{len(results)} assets matched")


def cmd_history(args):
    """Show full lineage/history for a brand or asset family."""
    reg = load_registry()
    family = args.family

    versions = []
    for path_str, entry in reg["assets"].items():
        if entry.get("family") == family or family in Path(path_str).name:
            versions.append((path_str, entry))

    if not versions:
        print(f"No history found for: {family}")
        sys.exit(1)

    versions.sort(key=lambda x: x[1].get("version", 0))

    print(f"\n=== History: {family} ===")
    print(f"{'Ver':<5} {'Type':<8} {'File':<40} {'Status':<12} {'Date'}")
    print("-" * 120)
    for path_str, e in versions:
        ver = e.get("version", "?")
        canonical = " [CANONICAL]" if e.get("is_canonical") else ""
        print(f"{ver:<5} {e.get('type',''):<8} {Path(path_str).name:<40} "
              f"{e['status']:<12} {e['created_at'][:10]}{canonical}")
        if e.get("prompt"):
            print(f"      Prompt: {e['prompt'][:80]}")
        if e.get("superseded_by"):
            print(f"      -> superseded by: {Path(e['superseded_by']).name}")

    approved = [v for v in versions if v[1]["status"] == "approved"]
    print(f"\n{len(versions)} versions total, {len(approved)} approved")


def cmd_flag(args):
    """Bulk-flag assets for replacement. Example:
    unified_registry.py flag --engine chatterbox --reason "switching to elevenlabs"
    Marks all matching assets as 'needs_replacement' without deleting."""
    reg = load_registry()
    count = 0
    for path_str, entry in reg["assets"].items():
        match = True
        if args.type and entry.get("type") != args.type:
            match = False
        if args.engine and entry.get("engine") != args.engine:
            match = False
        if args.voice and args.voice not in entry.get("voice_id", ""):
            match = False
        if args.family and entry.get("family") != args.family:
            match = False
        if match and entry.get("status") == "approved":
            entry["needs_replacement"] = True
            entry["replacement_reason"] = args.reason
            count += 1

    save_registry(reg)
    print(f"Flagged {count} approved assets for replacement")
    print(f"  Reason: {args.reason}")


def cmd_characterize(args):
    """Tag an asset with voice/content characteristics for querying.
    Example: unified_registry.py characterize <file> --add raspy,high-energy
    """
    reg = load_registry()
    path = str(Path(args.file).resolve())
    if path not in reg["assets"]:
        print(f"Not in registry: {path}")
        sys.exit(1)
    entry = reg["assets"][path]
    chars = set(entry.get("characteristics", []))
    if args.add:
        chars.update(args.add.split(","))
    if args.remove:
        chars.difference_update(args.remove.split(","))
    entry["characteristics"] = sorted(chars)
    save_registry(reg)
    print(f"{Path(path).name}: characteristics = {entry['characteristics']}")


def cmd_auto_approve(args):
    """Auto-approve pending assets by rules. Dry-run by default.
    Rules:
    1. Byte-identical to an approved file (same SHA256) -> approve
    2. In an approved directory (parent dir contains only approved files) -> approve
    3. Family batch: --family NAME approves all pending in that family
    """
    reg = load_registry()
    approved_hashes = set()
    for path_str, entry in reg["assets"].items():
        if entry.get("status") == "approved" and entry.get("sha256"):
            approved_hashes.add(entry["sha256"])

    actions = []

    for path_str, entry in list(reg["assets"].items()):
        if entry.get("status") != "pending":
            continue

        reason = None

        # Rule 1: byte-identical to approved
        if entry.get("sha256") in approved_hashes:
            reason = "byte-identical to approved file"

        # Rule 2: family batch
        elif args.family and entry.get("family") == args.family:
            reason = f"family batch: {args.family}"

        # Rule 3: directory-based (parent dir has approved files, no rejected)
        elif args.by_directory:
            parent = str(Path(path_str).parent)
            siblings = [e for p2, e in reg["assets"].items()
                        if str(Path(p2).parent) == parent]
            approved_sibs = [e for e in siblings if e.get("status") == "approved"]
            rejected_sibs = [e for e in siblings if e.get("status") == "rejected"]
            if approved_sibs and not rejected_sibs and len(approved_sibs) >= 3:
                reason = f"directory {parent} has {len(approved_sibs)} approved, 0 rejected"

        if reason:
            actions.append((path_str, reason))

    if args.dry_run:
        print(f"[DRY RUN] Would auto-approve {len(actions)} assets:")
        for path_str, reason in actions[:50]:
            print(f"  {Path(path_str).name} ({reason})")
        if len(actions) > 50:
            print(f"  ... and {len(actions) - 50} more")
    else:
        for path_str, reason in actions:
            reg["assets"][path_str]["status"] = "approved"
            reg["assets"][path_str]["approved_at"] = datetime.now().isoformat()
            reg["assets"][path_str]["approved_by"] = "auto-approve"
            reg["assets"][path_str]["auto_approve_reason"] = reason
        save_registry(reg)
        print(f"Auto-approved {len(actions)} assets")

    return len(actions)


def cmd_tag(args):
    """Embed metadata into WAV RIFF INFO chunk (audio only)."""
    reg = load_registry()
    path = str(Path(args.file).resolve())
    if path not in reg["assets"]:
        print(f"Not in registry: {path}")
        sys.exit(1)
    entry = reg["assets"][path]
    if not path.lower().endswith(".wav"):
        print("Tagging only supports .wav files (RIFF INFO chunks)")
        sys.exit(1)

    # Read existing WAV data
    with wave.open(path, "rb") as w:
        w.getparams()
        w.readframes(w.getnframes())

    # Build INFO chunk
    def info_field(tag, value):
        v = value.encode("utf-8") + b"\x00"
        if len(v) % 2:
            v += b"\x00"
        return tag.encode("ascii") + len(v).to_bytes(4, "little") + v

    info_data = b"INFO"
    info_data += info_field("IARL", f"type:{entry.get('type','')}")
    info_data += info_field("IART", f"voice:{entry.get('voice_id','')}")
    info_data += info_field("IENG", f"engine:{entry.get('engine','')}")
    info_data += info_field("ICRD", entry["created_at"][:10])
    info_data += info_field("ICMT",
                            f"status:{entry['status']} prompt:{entry.get('prompt','')[:100]}")
    list_chunk = b"LIST" + (len(info_data)).to_bytes(4, "little") + info_data

    # Rebuild WAV with INFO chunk before data
    with open(path, "rb") as f:
        raw = f.read()

    # Find data chunk and insert LIST before it
    data_idx = raw.find(b"data")
    if data_idx == -1:
        print("Could not find data chunk")
        sys.exit(1)

    new_raw = raw[:data_idx] + list_chunk
    if len(list_chunk) % 2:
        new_raw += b"\x00"
    new_raw += raw[data_idx:]

    # Fix RIFF size
    riff_size = len(new_raw) - 8
    new_raw = new_raw[:4] + riff_size.to_bytes(4, "little") + new_raw[8:]

    with open(path, "wb") as f:
        f.write(new_raw)

    print(f"Tagged: {Path(path).name}")
    print(f"  type={entry.get('type','')} voice={entry.get('voice_id','')} "
          f"engine={entry.get('engine','')} status={entry['status']}")


def cmd_migrate(args):
    """Migrate legacy registry entries into the unified format.

    Adds a 'type' field (auto-detected from extension) to every entry that
    lacks one, maps legacy 'asset_type' -> 'type', and backfills missing
    type-specific metadata blocks with sensible defaults. Backs up the
    original registry to registry.json.bak first. Safe to run repeatedly
    (idempotent).
    """
    if not REGISTRY.exists():
        print("No registry.json found — nothing to migrate.")
        return

    backup = BASE / "registry.json.bak"
    if not backup.exists():
        shutil.copy(REGISTRY, backup)
        print(f"Backup written: {backup}")

    reg = load_registry()
    migrated = 0
    for path_str, entry in reg["assets"].items():
        changed = False

        # Map legacy asset_type -> type
        if "asset_type" in entry and "type" not in entry:
            entry["type"] = entry.pop("asset_type")
            changed = True

        # Auto-detect type if missing
        if not entry.get("type"):
            entry["type"] = detect_type(path_str)
            changed = True

        t = entry["type"]

        # Backfill type-specific metadata blocks
        if t == "audio" and "settings" not in entry:
            entry["settings"] = {
                "stability": 0.5,
                "similarity_boost": 0.75,
                "style": 0.0,
                "use_speaker_boost": True,
            }
            entry.setdefault("voice_id", "unknown")
            entry.setdefault("engine", "chatterbox")
            changed = True
        elif t == "video":
            entry.setdefault("resolution", "unknown")
            entry.setdefault("fps", 0.0)
            entry.setdefault("duration_sec", 0.0)
            entry.setdefault("codec", "unknown")
            changed = True
        elif t == "image":
            entry.setdefault("dimensions", "unknown")
            entry.setdefault("style", "unknown")
            changed = True
        elif t == "3d":
            entry.setdefault("poly_count", 0)
            entry.setdefault("format",
                             Path(path_str).suffix.lower().lstrip("."))
            changed = True
        elif t == "document":
            entry.setdefault("doc_type", "unknown")
            changed = True

        entry.setdefault("characteristics", [])
        entry.setdefault("is_canonical", False)
        entry.setdefault("version", 1)

        if changed:
            migrated += 1

    save_registry(reg)
    print(f"Migration complete: {migrated} entries updated, "
          f"{len(reg['assets'])} total.")


def main():
    p = argparse.ArgumentParser(description="Unified Asset Registry (all types)")
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("register")
    r.add_argument("file")
    r.add_argument("--type", default=None,
                   choices=["audio", "video", "image", "3d", "document", "other"],
                   help="Asset type (auto-detected from extension if omitted)")
    r.add_argument("--prompt", default="")
    r.add_argument("--status", default="pending",
                   choices=["pending", "approved", "rejected", "superseded"])
    r.add_argument("--family", default=None,
                   help="Asset family for version tracking (e.g., 'align-intro')")
    r.add_argument("--version", type=int, default=1)
    # audio
    r.add_argument("--voice", default="unknown")
    r.add_argument("--engine", default="chatterbox")
    r.add_argument("--stability", type=float, default=0.5)
    r.add_argument("--similarity-boost", type=float, default=0.75)
    r.add_argument("--style", default="0.0",
                   help="Audio style param (float, e.g. 0.0) or, for images, "
                        "the style name (e.g. newsprint)")
    r.add_argument("--speaker-boost", action="store_true", default=True)
    # video
    r.add_argument("--resolution", default="1920x1080")
    r.add_argument("--fps", type=float, default=30.0)
    r.add_argument("--duration", type=float, default=0.0)
    r.add_argument("--codec", default="h264")
    # image
    r.add_argument("--dimensions", default="unknown")
    # 3d
    r.add_argument("--poly-count", type=int, default=0)
    r.add_argument("--format", default=None)
    # document
    r.add_argument("--doc-type", default="unknown")

    a = sub.add_parser("approve")
    a.add_argument("file")
    a.add_argument("--by", default=None)

    rj = sub.add_parser("reject")
    rj.add_argument("file")

    s = sub.add_parser("supersede")
    s.add_argument("old")
    s.add_argument("new")

    c = sub.add_parser("cleanup")
    c.add_argument("--dry-run", action="store_true")
    c.add_argument("--scheduled", action="store_true",
                   help="Unattended mode: quarantine pending>7d + archive superseded only; "
                        "duplicates flagged in registry, nothing is deleted")

    sub.add_parser("status")

    t = sub.add_parser("tag")
    t.add_argument("file")

    cn = sub.add_parser("canonical")
    cn.add_argument("family", help="Asset family name (e.g., align-intro)")

    q = sub.add_parser("query", help="Query assets by metadata")
    q.add_argument("--type", default=None)
    q.add_argument("--engine", default=None)
    q.add_argument("--status", default=None)
    q.add_argument("--family", default=None)
    q.add_argument("--voice", default=None)
    q.add_argument("--characteristic", default=None)
    q.add_argument("--style", default=None)
    q.add_argument("--format", default="table", choices=["table", "paths", "json"])

    h = sub.add_parser("history", help="Show version history for a brand/family")
    h.add_argument("family")

    f = sub.add_parser("flag", help="Bulk-flag assets for replacement")
    f.add_argument("--type", default=None)
    f.add_argument("--engine", default=None)
    f.add_argument("--voice", default=None)
    f.add_argument("--family", default=None)
    f.add_argument("--reason", required=True)

    ch = sub.add_parser("characterize", help="Tag voice/content characteristics")
    aa = sub.add_parser("auto-approve", help="Auto-approve pending by rules")
    aa.add_argument("--family", default=None, help="Approve all pending in a family")
    aa.add_argument("--by-directory", action="store_true",
                    help="Approve if parent dir has 3+ approved, 0 rejected")
    aa.add_argument("--dry-run", action="store_true")
    ch.add_argument("file")
    ch.add_argument("--add", default=None, help="Comma-separated: raspy,high-energy,smooth...")
    ch.add_argument("--remove", default=None)

    m = sub.add_parser("migrate", help="Migrate legacy registry entries to unified format")

    args = p.parse_args()
    {
        "register": cmd_register,
        "approve": cmd_approve,
        "reject": cmd_reject,
        "supersede": cmd_supersede,
        "cleanup": cmd_cleanup,
        "status": cmd_status,
        "tag": cmd_tag,
        "canonical": cmd_canonical,
        "query": cmd_query,
        "history": cmd_history,
        "flag": cmd_flag,
        "characterize": cmd_characterize,
        "auto-approve": cmd_auto_approve,
        "migrate": cmd_migrate,
    }[args.cmd](args)


if __name__ == "__main__":
    main()
