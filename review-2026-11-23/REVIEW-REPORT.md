# Asset review pass — final report, 2026-11-23

Ricardo: "The remaining work is the 3,032 pending approvals — that's your review pass."
Tap given 2026-11-23 19:19 PST for the recommendation in RECOMMENDATION.md.

## What the backlog actually was

- At pass start (19:06): 3,032 pending with no family (2,132 images, 892 audio, 9 video).
- At 19:09 the other chat's Pro duplicate cleanup landed: 375 Pro duplicates deleted, registry 3,240 → 2,863.
- Pass ran against the current registry: **2,657 pending with no family** (Pro 1,969, Studio 688).

## Verification (read-only, both hosts)

- **Studio: 688/688 present-match**, 0 missing, 0 hash/size mismatch. (Studio dropped off the network ~12 min mid-run, recovered on its own; output recovered intact.)
- **Pro: 1,958/1,969 present-match**, 0 hash mismatch, 2 size-mismatch (SVGs edited since scan), 9 missing — all 9 are AppleDouble `._` sidecar files in `globe/verify-v9-deploy/`, not real assets.
- Registry's own auto-approve rules alone would have approved 128 (directory rule) + 0 (byte-identical to approved). The rest needed this pass.

## Decisions applied to registry.json (backup: registry-before-review-2026-11-23.json)

| Decision | Count | Meaning |
|---|---|---|
| APPROVE | 2,538 | Verified present + hash-match, live copy |
| APPROVE-KEEP-SOLE-COPY | 30 | Deleted/trash-path file that is the only copy in the whole registry — kept per Ricardo's rule |
| SUPERSEDE | 26 | Backup copy; same-named live copy is now the approved canonical |
| REJECT | 9 | AppleDouble `._` sidecars; file does not exist, not an asset |
| REVIEW-PENDING | 54 | Left pending with reason recorded (see below) |

Registry now: **approved 2,724, superseded 75, rejected 9, pending 55, total 2,863.**
Pending no-family: **0**. The 55 pending = the 54 review-pending below + 1 delgado-segment (has a family, out of this pass's scope).

## Left pending for Ricardo (54, each with a reason in the registry)

- **42 Studio backup voice files** — byte-identical to a different-named live file (e.g. deleted `ep-shelly-v3.mp3` = live `ep-lisa.mp3`). Either a mislabel or a real duplicate; approving it as a voice would be guessing.
- **10 version sets** — orchestra `align-newsroom` v5–v8, orchestra `breaking-news` v2–v4, hero-video `hero` v1–v3. Needs his canonical pick.
- **2 SVGs** — `card-ai.svg`, `hero-globe.svg`: changed size since the registry scan; hash not verified, needs re-registration.

## Rules the pass followed

- Byte-identical ≠ duplicate: a reporter's `intro-en`/`intro-native` are the same audio for English-native reporters, and announcer/narrator files share audio across roles. Same bytes, different jobs — kept as separate assets. Only same-name backup copies were superseded.
- No sole copy was deleted or superseded. No file was approved without a hash-verified present copy on its host.
- Families tagged from paths (reporter slug, voice name, brand/frontend section) on all 2,657.

## Cleanup — NOT yet run (needs the list shown first, then a tap)

Candidates, all on the Studio, all superseded with their canonical live copy now approved + hash-verified:
- The 26 superseded `_deleted-backup` files (list in `cleanup-list-2026-11-23.md`).
- The 42 review-pending backup files are NOT cleanup candidates until Ricardo rules on them.
- The 9 rejected AppleDouble files do not exist on disk — nothing to delete.

## Files in review-2026-11-23/

- `RECOMMENDATION.md`, `REVIEW-REPORT.md`, `cleanup-list-2026-11-23.md`
- `studio-verify.json`, `studio-verify-out.tsv`, `studio-paths.tsv`, `studio-decisions.json`
- `pro-verify.json`, `pro-verify-out.tsv`, `pro-verify-out-raw.tsv`, `pro-paths.tsv`, `pro-paths-removed-2026-11-23.tsv`, `pro-decisions.json`
- `registry-before-review-2026-11-23.json` (pre-pass backup), `recon-2026-11-23.json`
