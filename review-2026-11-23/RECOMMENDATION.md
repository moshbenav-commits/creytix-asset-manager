# Review-pass recommendation — 2026-11-23 19:2x PST

## Verified current state (registry.json, live check 2026-11-23 19:19 PST)

- Total registry: **2,863** entries (was 3,240 — the other chat's Pro cleanup at 19:09 deleted 375 Pro duplicates, 461 MB, and archived 27 Moveras superseded videos; registry synced back to the VM).
- Approved 156, pending 2,658, superseded 49, rejected 0 (the 2 rejected Moveras entries were dropped with their already-deleted files).
- **Pending with no family: 2,657** (was 3,032): images 1,758, audio 890, video 9. Pro 1,969, Studio 688.
- Unique contents among those 2,657: **2,496 sha256** — **161 extra duplicate copies** remain.
- Registry auto-approve rules, run live: byte-identical to an approved file = **0**; directory rule (parent dir 3+ approved, 0 rejected) = **128**, all reporter portraits in one Pro folder.
- Junk-path pending (deleted-backup / _backup-pre-* / _trash-superseded): **98**
  - **Sole copy in the whole registry: 30** — 18 in article-images/out/_backup-pre-unify-2026-10-03, 4 in Studio chatterbox-voices/_deleted-backup, 4 in portraits/_trash-superseded/blue-duotone-treated, 3 in story-images/qc/_backup-pre-parity, 1 in portraits/batch-output/_backup-pre-theo-final.
  - **Has another copy elsewhere: 68** — e.g. _deleted-backup/ep-shelly-v3.mp3 is byte-identical to the live ep-lisa.mp3.
- Weekly cleanup cron: **fixed 2026-11-23 (commit 896bfb0)** — now only reports pending files and flags duplicates; it will never move or delete anything on its own. Quarantine is manual only. (The old rule would have quarantined 2,335 pending files on its next run, because they were registered in bulk, not because they are stale.)
- Verification runs in progress (Pro + Studio, existence + size + sha256 for every pending file, re-extracted from the current registry after the 19:09 rewrite).

## Recommendation (Ricardo's deleted-files rule adopted verbatim)

1. **Verify first** — existence + size + sha256 on Pro and Studio for all 2,657. Missing or hash-mismatched files stay pending with the reason recorded; nothing is approved on registry data alone.
2. **Tag families by path** — reporter slug, voice name, brand section, frontend section. No family, no batch approval.
3. **Dedupe before approving** — one canonical per sha256. Prefer the live/working copy over any backup/trash copy; prefer Studio canonical voice dirs and Pro frontend assets over worktree copies. Extra copies become superseded, not deleted yet.
4. **Deleted/trash files — Ricardo's rule:** sole-copy deleted-backup/trash files (30) are **kept** — promoted to approved as the canonical copy, family tagged, with a `sole-copy` note. The 68 junk copies that have a live copy elsewhere are **not kept**.
5. **Approve in batches where evidence supports it** — the 128 by-directory reporter portraits, plus canonical copies in source-of-truth dirs (reporter-voices, chatterbox-voices, frontend assets/img, brand logos/globe) once hash-verified. Taste picks stay with Ricardo as a short list: hero-v1/v2/v3, portrait treatments, jingle/orchestra variants — no guessing.
6. **Cleanup last, only after one copy + no dedups is confirmed** — delete the 68 junk duplicates and the other superseded extra copies, with the full list shown first. Nothing is deleted before its canonical copy is approved and verified present.

## What this does NOT do

- No blanket approval of all 2,657. The registry's own rules approve 128; the rest need the verification + dedupe + family steps above.
- No deletion of a sole copy, ever. No auto-quarantine (cron fixed).
- No approval of files that don't exist on their host or whose hash doesn't match the registry.
