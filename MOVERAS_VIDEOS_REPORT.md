# Moveras Videos — Asset Inventory & Registry Report

**Date:** 2026-10-20
**Status:** Inventory + registration complete. Nothing deleted.

## Summary

| Metric | Value |
|---|---|
| Total video files | 32 |
| Total size | 976.1 MB |
| Locations | MacBook Pro only (none on VM) |
| Registry status | All 32 registered as `pending` in unified registry |
| Exact duplicates | 2 groups (4 files), ~71.6 MB wasted |

## Canonical source locations

| Content | Location |
|---|---|
| Whitelabel renders & segments (28 files) | `pro:/Users/ricardo/Desktop/Workspace.nosync/whitelabel/work/` |
| Logo animation (1 file) | `pro:/Users/ricardo/Desktop/Workspace.nosync/whitelabel/assets/ep_logo_animation.mp4` |
| Original source download (2 dupes) | `pro:/Users/ricardo/Desktop/workspace.nosync/browser_downloads/sess-1761628938/` |

**No Moveras videos exist on the VM.** The VM's 114 `*moveras*` matches are Expedia Parts backend code (catalog sync, pricing, portal scraper), not video assets. This is why they "kept being pulled from source" — there's no local mirror.

## Version families

| Family | Versions | Notes |
|---|---|---|
| `moveras-ep-v2-final` | v1 → v5 (5 files, ~111 MB each) | Full version chain, all distinct hashes |
| `moveras-buildprocess` | CLEAN_v12, CLEAN_v13 + original source | Source = `Moveras_Build_Process.mp4` (68.5 MB, downloaded 2026-10-09) |
| `moveras-whitelabeled-test` | v3–v6 + 2 mobile variants | Test renders before finals |
| `moveras-v2proof` | source, source_local, master, panseg | `source` and `source_local` are exact duplicates |
| `moveras-segments` | 12 fix/segment clips | dyno, shutter, sign fixes + segintel proof |
| `moveras-ep-logo` | 1 | Logo animation |

## Exact duplicates found

1. **`v2proof_source.mp4` ↔ `v2proof_source_local.mp4`**
   - Hash: `8c4d6227…` | 3,125,171 bytes each | ~3.1 MB wasted
   - Same directory — safe to remove one

2. **`Moveras_Build_Process.mp4` source download × 2**
   - Hash: `ced3f4c1…` | 68,463,992 bytes each | ~68.5 MB wasted
   - Locations: `workspace.nosync/browser_downloads/` and `.worktrees/gf-repair/browser_downloads/`
   - This is the original source the CLEAN versions were derived from — keep one copy

## Recommended actions (pending Ricardo's approval)

1. Delete one of each duplicate pair (~71.6 MB recovered)
2. Review `moveras-ep-v2-final` v1–v5: approve one as canonical, supersede the rest
3. Review `moveras-buildprocess`: approve CLEAN_v13 or source, archive the other
4. Approve/reject the 12 segment clips and test renders
5. Consider mirroring approved videos to the VM hub so they never need re-pulling from the Pro

## Registry queries

```bash
cd ~/workspace/audio-asset-system
python3 unified_registry.py query --type video --family moveras-ep-v2-final
python3 unified_registry.py query --type video --family moveras-buildprocess
python3 unified_registry.py history moveras-ep-v2-final
```
