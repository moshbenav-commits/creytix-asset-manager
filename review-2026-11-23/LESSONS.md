# Lessons — asset review pass, 2026-11-23

Real lessons from the 3,032-pending-approval review pass (registry
2,863 assets; review commits `0711a21` + `784875e` on main in
creytix-asset-manager). Read before the next registry pass or cleanup.

## 1. Byte-identical is not duplicate (2026-11-23)

A reporter's `intro-en.wav` and `intro-native.wav` are the same audio
for English-native reporters; announcer/narrator files share audio
across roles (`alignnewsroom-announcer-v3` = `mlm-narrator` =
`moveras-narrator` = 10 `mlm-verify-*` files). Same bytes, different
jobs — kept as separate approved assets. Only same-name backup copies
were superseded (26 files). Lesson: dedupe on (sha + name + role),
never on sha alone. The registry's `duplicate_of` flag conflated the
two — 775 flagged "duplicates" pointed at other pending copies or at
nothing in the registry, none at an approved file.

## 2. The registry is a moving target — re-verify counts before acting (2026-11-23)

Mid-verification, the other chat's Pro duplicate cleanup rewrote
`registry.json` (3,240 → 2,863 entries; 375 Pro duplicates deleted).
The Pro verifier had to re-extract its path list from the current
registry and filter results to the 1,969 paths still present. The 375
removed entries turned out to be exactly the ones missing on disk in
the old-list run — the cleanup and the verification agreed, but only
because the totals were reconciled (2,344 old-list rows, 384 missing =
375 removed + 9 AppleDouble). Lesson: never act on registry counts
from the start of a pass; re-read the registry and reconcile before
every decision write. Registry drift after our pass (Nov 24: 2,877
total, +14 new VM-local audio files from other work, delgado-segment
approved by another chat) is the same lesson again.

## 3. The tool's own auto-approve rules approve almost nothing (2026-11-23)

Rule 1 (byte-identical to approved) = 0 assets. Rule 3 (by-directory)
= 128 reporter portraits. Of 3,032 pending, the rules alone would
have cleared 128 — a blanket "approve all" would have approved trash,
deleted backups, training data, and multiple copies of the same file.
Lesson: a review pass is verification + family tagging + dedupe, not
a button. The pass is the product.

## 4. Keep a sole copy, even in the trash (2026-11-23, Ricardo's rule)

Ricardo: "for the deleted files i am ok with that to keep them if
there is only one coy and then once we have one copy and no dedups
then we clean up the files." 30 sole-copy deleted/trash files were
promoted to approved as canonical, with a `sole-copy` note. The 68
junk copies that had a live copy elsewhere were not kept — 26
superseded and deleted (canonical-gated), 42 left pending because
their bytes matched a *different-named* live file (mislabeled or
duplicate — needs a human call, not a guess). Lesson: deletion
privileges the canonical copy, never the directory it sits in.

## 5. Two chats, one registry — coordinate through the file, not memory (2026-11-23)

This pass and the "Analyze and fix broken movie files" chat worked the
same registry the same evening: their Pro dedupe (375 files, 461.3 MB)
landed at 19:09 while our verifiers were mid-run. Nothing broke,
because both sides read the file live and reconciled counts — but it
was luck plus checking, not a lock. Lesson: when two runs share a
registry, check `registry.json` mtime + totals at the start of every
step, and never hold a stale in-memory copy across a write.

## 6. A scheduled cleanup that quarantines by age will quarantine working files (2026-11-23)

The weekly `asset-cleanup-weekly` cron's pending-older-than-7-days
rule would have quarantined 2,335 working files in its dry run — the
files are old because they were registered in bulk, not because they
are stale. Fixed (commit `896bfb0`, other chat): the cron now only
reports pending files and flags duplicates; it never moves or deletes
anything on its own. Quarantine is manual only. Lesson: an age rule on
a bulk-registered registry is a mass-delete rule. Any future
automation that moves files needs a per-file reason, not a date.

## 7. Gate every deletion on its canonical copy, on the host (2026-11-23)

The cleanup script verified, per file, that the canonical live copy
still existed on the Studio with the registry sha256 *before*
deleting the backup: 26/26 deleted, 0 skipped, 150.9 MiB freed.
Lesson: a superseded flag in the registry is a claim; the hash check
on the host is the proof. Never delete from the registry alone.

## 8. The check-before-showing rule was minted by work in this same registry (2026-11-24)

The 5 regenerated podcast episodes were delivered Nov 23 without a
speed check; Ricardo's ear caught Elena (88 wpm), Hana (73 wpm),
Tarun (71 wpm) at half normal speaking rate (~150 wpm). Root cause
was dead air (46–77s of true silence vs 9–12s in the good ones), not
slow speech. The rule (AGENTS.md, Nov 24): verify work before
presenting it — audio measured (wpm, pitch, silence), images OCR
parity, pages/builds loaded live. Those same 5 episode files are now
in this registry as new pending (family `podcast-ep001`), registered
Nov 24 by other work. Lesson: the registry records the artifacts; the
rule records what the artifacts taught. Both belong in the same
review.
