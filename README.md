# Asset Management System — Align Newsroom

One unified registry for ALL asset types (audio, video, image, 3d, document).

## Main tool

`unified_registry.py` — single entry point; single `registry.json`.

Every asset gets:
- `type`: audio | video | image | 3d | document | other (auto-detected from extension)
- `status`: approved | pending | rejected | superseded
- `sha256` hash (dedupe)
- `family` + `version` for version tracking and canonical marking
- Type-specific metadata:
  - **audio**: voice_id, engine, settings (stability, similarity_boost, style, speaker_boost), prompt
  - **video**: resolution, fps, duration_sec, codec
  - **image**: dimensions, style
  - **3d**: poly_count, format
  - **document**: doc_type
- `characteristics` tags (e.g. raspy, high-energy) for bulk queries

## Usage

```bash
# Register
python3 unified_registry.py register <file> [--type image] --style newsprint --family <fam> --version <n>
python3 unified_registry.py register <file>.wav --voice <id> --engine chatterbox --prompt "..."
python3 unified_registry.py register <file>.mp4 --resolution 1920x1080 --fps 30 --codec h264

# Lifecycle
python3 unified_registry.py approve <file>
python3 unified_registry.py reject <file>        # deletes the file
python3 unified_registry.py supersede <old> <new>
python3 unified_registry.py canonical <family>   # marks latest approved + creates <family>-latest symlink

# Find / bulk ops
python3 unified_registry.py query --type image --status approved
python3 unified_registry.py query --engine chatterbox        # e.g. engine swap
python3 unified_registry.py query --characteristic raspy
python3 unified_registry.py history <family>                 # full version lineage
python3 unified_registry.py flag --engine chatterbox --reason "switching engines"
python3 unified_registry.py characterize <file> --add raspy,high-energy

# Housekeeping
python3 unified_registry.py cleanup --dry-run    # preview: quarantine stale pending, archive superseded, dedupe
python3 unified_registry.py cleanup
python3 unified_registry.py status               # counts by status and type
python3 unified_registry.py tag <file>.wav       # embed metadata in WAV RIFF INFO
python3 unified_registry.py migrate              # (re)apply unified format to legacy entries; writes registry.json.bak once
```

## Legacy wrappers (backward compatible)

- `asset_manager.py` — forwards all args to `unified_registry.py`
- `video_asset_manager.py` — forwards, injecting `--type video` on register

Originals preserved as `asset_manager.py.orig` / `video_asset_manager.py.orig`.

## Files

- `registry.json` — the single registry (3,687 assets after 2026-10-19 full scan)
- `registry.json.bak` — pre-migration backup
- `FILE_LOCATIONS.md` — where every asset lives across VM / Pro / Studio
- `FULL_REPO_SCAN.md` — full scan report (3,865 assets, duplicates, cleanup preview)
