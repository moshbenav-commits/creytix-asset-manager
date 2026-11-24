# Full Repo Asset Scan — 2026-10-19

**3,865 assets registered. 4.88 GB total. 755 duplicate groups wasting 1.59 GB.**

## Summary by Type

| Type | Count | Approved | Pending | Superseded |
|------|-------|----------|---------|------------|
| Image | 2,411 | 82 | 2,324 | 5 |
| Audio | 1,433 | 6 | 1,414 | 13 |
| Video | 17 | 0 | 17 | 0 |
| **Total** | **3,865** | **88** | **3,755** | **22** |

## Summary by Location

| Target | Files | Size | Host |
|--------|-------|------|------|
| studio:chatterbox-voices | 378 | 1,121 MB | Studio |
| pro:align-newsroom-brand | 1,095 | 1,070 MB | Pro |
| pro:newsroom-voices | 690 | 1,003 MB | Pro |
| studio:reporter-voices | 310 | 558 MB | Studio |
| pro:frontend-nr-design-wt | 489 | 374 MB | Pro |
| vm:reporter-voices | 364 | 276 MB | VM |
| vm:podcasts | 51 | 168 MB | VM |
| vm:reporter-portraits | 174 | 165 MB | VM |
| vm:video-sample | 140 | 141 MB | VM |
| pro:frontend-newsroom-build | 135 | 96 MB | Pro |
| vm:article-images-v2 | 19 | 19 MB | VM |
| vm:reporter-scenery | 10 | 5 MB | VM |
| vm:newsroom-live | 6 | 3 MB | VM |

## Duplicates: 755 Groups, 1,773 Files, 1.59 GB Wasted

### Pattern 1: Voice references in 3 places (biggest waste)
Every reporter's `voice-reference.wav` exists identically in:
- `vm:reporter-voices/{slug}/voice-reference.wav` (VM mirror)
- `studio:chatterbox-voices/alignnewsroom-{slug}.wav` (Studio source)
- `studio:reporter-voices/{slug}/voice-reference.wav` (Studio generated)

~58 reporters × 3 copies × ~13 MB = **~750 MB** in triplicate voice files.

**Recommendation:** Studio `chatterbox-voices/` is the source of truth. VM mirror is a working copy (keep if actively used, else delete). The `reporter-voices/{slug}/voice-reference.wav` copies are redundant.

### Pattern 2: `_deleted-backup` isn't deleted
`studio:chatterbox-voices/_deleted-backup/` contains files identical to live ones:
- `alignnewsroom-vivienne-hart.wav` (live + backup)
- `alignnewsroom-sofia-bellini.wav` (live + backup)
- `alignnewsroom-isaac-carlisle.wav` (live + backup)
- ...and more

**Recommendation:** The `_deleted-backup` directory name suggests these were meant to be removed. Verify, then delete.

### Pattern 3: Hero video frames with different names, same content
`pro:align-newsroom-brand/hero-video/frame-*.png` — 12 files with different names but identical content (frame-0009.png = frame-0008.png = frame-0003.png...).

**Recommendation:** Dedupe to one file per unique frame.

### Pattern 4: Orchestra files mirrored with `orch-` prefix
`vm:video-sample/orch-*.mp3` are byte-identical to `pro:newsroom-voices/orchestra/*.mp3`.

**Recommendation:** VM copies are redundant mirrors. Delete after confirming Pro has them.

### Pattern 5: Pro demo pulls duplicated on VM
`vm:video-sample/pro-demo-brazilian-*.mp3` = `pro:newsroom-voices/demo-brazilian-*.mp3`.

**Recommendation:** VM copies were for review. Now that they're reviewed, delete VM copies.

## Cleanup Preview (dry-run): 1,036 Actions

| Action | Count | Description |
|--------|-------|-------------|
| ARCHIVE | 17 | Superseded intro v1–v11, v1 scenery, contaminated ambience → archive/ |
| DEDUPE | 1,019 | Duplicate files (keeps approved/newest, flags rest) |

**No files were actually deleted or moved.** Run without `--dry-run` to execute.

### Archive candidates (17)
- `align-intro-v1.wav` through `align-intro-v11.wav` (superseded by v12)
- `align-intro-v9-bed.wav` (superseded)
- `newsroom-ambience-v2.wav` (contaminated, superseded by clean chatter)
- `elena-cruz-v1.jpg`, `marisol-ochoa-v1.jpg`, `hana-iverson-v1.jpg`, `tarun-vashist-v1.jpg`, `graham-ellsworth-v1.jpg` (v1 scenery)

### Dedupe candidates (1,019)
Full list in `dup-groups.json`. Largest groups:
1. Voice reference triplicates (~750 MB)
2. `_deleted-backup` dupes (~200 MB)
3. Hero video frame dupes (~27 MB)
4. Orchestra `orch-` prefix mirrors (~5 MB)

## Largest Space Wasters

| Location | Size | % of total | Action |
|----------|------|------------|--------|
| studio:chatterbox-voices | 1,121 MB | 23% | Dedupe triplicates, clear _deleted-backup |
| pro:align-newsroom-brand | 1,070 MB | 22% | Dedupe hero frames, audit globe/ dir |
| pro:newsroom-voices | 1,003 MB | 21% | Audit brief-pipeline/ (10 old briefs), combos/ |
| studio:reporter-voices | 558 MB | 11% | Dedupe voice-reference copies |

## Recommended Approval Actions for Ricardo

### Approve (bulk)
1. **Reporter voice references** (58× `alignnewsroom-{slug}.wav` on Studio) — these are the canonical voice clones
2. **Newsreader voices** (`{lang}-{male,female}-news`) — 29 languages, generic but approved for use
3. **Orchestra themes** (`align-newsroom-v5` through `v8`, `align-newsroom-voiced`) — the 12 played on 2026-10-18
4. **Brand logos** (42 SVGs in `assets/img/logo/`) — already vectorized via cf-logo-lane
5. **Portrait variants** (`*-camera.webp`, `*-chat.webp`) — if the crop variants are approved for use

### Review then decide
1. **`_deleted-backup/` on Studio** — verify these are truly meant to be deleted, then clear (~200 MB)
2. **Brief pipeline outputs** (10 old MP3s from Oct 6) — still needed or archive?
3. **Combo files** (`combo-a` through `combo-i`) — which won? Archive the losers.
4. **Jingle v8 departments/countries** — still in use or superseded?
5. **Pro frontend assets** (624 files across 2 frontend dirs) — which frontend dir is current? (Already flagged in FILE_LOCATIONS.md)

### Reject (delete)
1. **Contaminated `newsroom-ambience-v2.wav`** — has machine-gun artifacts baked in, replaced by clean chatter
2. **Intro v1–v11** — superseded by v12 (already marked for archive, could go straight to reject)
3. **Duplicate `orch-` prefixed files** on VM — mirrors of Pro originals

## Registry

- **Location:** `~/workspace/audio-asset-system/registry.json` (3,865 entries)
- **Scan log:** `~/workspace/audio-asset-system/scan-log.json`
- **Dup groups:** `~/workspace/audio-asset-system/dup-groups.json`
- **Cleanup:** `python3 asset_manager.py cleanup --dry-run` to preview, without flag to execute

## Notes

- **Studio is READ ONLY** in this system — remote paths use `studio:` prefix, cleanup skips them automatically
- **Pro paths** use `pro:` prefix, also skipped by cleanup (manual action needed on Pro)
- **VM paths** are the only ones cleanup will actually touch
- The 4 pre-existing approved assets (intro-v12, clean chatter, flatline, phone ring) were preserved
- 58 main portraits + 19 article images + 5 v2 scenery marked approved
- 22 superseded (intro chain, v1 scenery, old announcer candidates, contaminated ambience)
