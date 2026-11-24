# Align Newsroom — File Locations Map

**Generated:** 2026-10-19
**Purpose:** Know where everything lives. No more hunting.

Three machines: **this VM** (`~` = /home/hatch), **MacBook Pro** (`pro-workspace` = /Users/ricardo), **Mac Studio** (`fleet-studio`).

> ⚠️ SSH note: always pass `-F /home/hatch/.ssh/config` (e.g. `ssh -F /home/hatch/.ssh/config pro-workspace`).

---

## AUDIO

### Voice reference clips (SOURCE OF TRUTH)
**Mac Studio:** `/Users/mac-mini-studio/expedia-data/chatterbox-voices/`
- 380 files, 1.1 GB
- `alignnewsroom-{slug}.wav` — 58 unique reporter voice references (30s pitch-shifted clips)
- `alignnewsroom-announcer.wav`, `-v2`, `-v3`, `-v4` — announcer iterations
- `[lang]-male-news.wav` / `[lang]-female-news.wav` — 29 languages × M/F generic newsreader voices (NOT reporter replacements)
- `_deleted-backup/` — old removed voices
- **This is canonical.** Registered in Chatterbox sidecar (port 4123). Never edit in place — supersede via re-register.

### Per-reporter generated audio (SOURCE OF TRUTH)
**Mac Studio:** `/Users/mac-mini-studio/expedia-data/reporter-voices/`
- 326 files, 559 MB, 74 dirs (58 reporters + MANIFEST.json + batch.log)
- Per reporter: `voice-reference.wav`, `intro-native.wav`, `intro-en.wav`, `intro-native-clean.wav`, `intro-en-fixed.wav`
- `MANIFEST.json` — machine-readable: slug → voice_id, seed, pitch_shift, languages
- **VM mirror:** `~/workspace/reporter-voices/` (390 files, 277 MB) — convenience copy + docs (`MANIFEST.md`, `LANGUAGE_COVERAGE.md`, `FISH_SPEECH_SELFHOSTED.md`). Treat Studio as canonical.

### Raw voice source material
**Mac Studio:** `/Users/mac-mini-studio/expedia-data/voice-sources/`
- 19 files, 208 MB — `calls/`, `interviews-2023/`, `team-chat/`
- Original recordings voices were cloned from. Keep, don't touch.

### Intro / sound-design workbench
**This VM:** `~/workspace/video-sample/`
- 1,808 files, 178 MB — ⚠️ HEAVY DUPLICATION, cleanup candidate
- `align-intro-v1.wav` … `align-intro-v12.wav`, `align-intro-FINAL.wav` — intro iterations (v12+ is current lineage)
- `announcer-candidates/` — smooth-1/2/3, older-1/2/3, announcer-v2/v3/v4 tests
- `real-phone-ring.mp3`, `real-flatline.mp3` — licensed SFX from 101soundboards (APPROVED, registered)
- `newsroom-chatter-clean.wav` — clean 9-voice chatter bed (APPROVED, registered)
- `newsroom-ambience-v2.wav` — ⚠️ CONTAMINATED (old synth phone baked in), do not use
- `chatter-clips/` — raw per-voice chatter clips
- `orch-*.mp3` — orchestra theme pulls from Pro
- `align-intro-v9-bed.wav`, `tagline-*.wav` — intermediate builds

### Approved audio registry (SOURCE OF TRUTH for approvals)
**This VM:** `~/workspace/audio-asset-system/`
- `asset_manager.py` — register / approve / reject / supersede / cleanup / tag
- `registry.json` — every file's status, voice_id, engine, settings, prompt, hash
- `quarantine/` — old pending files go here, not deleted blindly
- `archive/` — superseded versions (kept only after replacement is approved)
- `FILE_LOCATIONS.md` — this file
- Rule: nothing unapproved sits alongside approved assets. Run `cleanup --dry-run` first.

### Podcast episodes (SOURCE OF TRUTH)
**This VM:** `~/workspace/podcasts/`
- 63 files, 168 MB
- `{slug}/episode-001.mp3` + `{slug}/episode-001-fixed.mp3` — 5 pilots (elena-cruz, marisol-ochoa, hana-iverson, tarun-vashist, graham-ellsworth)
- `{slug}/deep-dive-001.mp3` + `-script.md` — 13-min deep dives (elena, marisol)
- `scripts.py`, `mix.py`, `gen_fixed_episodes.py`, `assemble_fixed_episodes.py` — pipeline
- `MANIFEST.md` — format docs

### Orchestra / jingles / combos (SOURCE OF TRUTH)
**MacBook Pro:** `~/Desktop/Workspace.nosync/newsroom-voices/`
- 1,201 files, 1.0 GB total. Subdirs:
- `orchestra/` — `align-newsroom-v5…v8.mp3` (instrumental themes), `align-newsroom-voiced.mp3` (7s voiced intro), `align-voice.mp3`, `voice-comingup/signoff/tonight.mp3`, `breaking-news-v2/v3/v4.mp3`, `orchestra.py`, `ORCHESTRA.md`, `samples/` (VSCO-2 orchestral samples)
- `jingles/` — `breaking/culture/finance/technology/veracity/world.mp3` + `v8/` (departments, countries, marks)
- `combos/` — `combo-a-winner` … `combo-i-drop-test` (music+voice combo tests)
- `brief-pipeline/out/` — 10 generated news briefs (nvidia, deepseek, korea-ai…)
- `briefs/` — reporter brief samples (cecilia-olliveira…)
- `reporters/` — `ai-editor-sample`, `fake-news-reporter-sample`, `fashion-editor-sample`
- `demo-brazilian-reporter.mp3`, `demo-brazilian-reporter-pt.mp3` — early Elena demos
- `design-upgrade/`, `feed-wiring/`, `style-reverse-engineering/`, `lora-dataset/`, `reporter-brains/`, `trust-widget/`, `collage-system/` — pipeline work

### Chime (SOURCE OF TRUTH)
**This VM:** `~/workspace/newsroom-live/chime.mp3` (+ `chime.wav`)
- 4.0s, the Align Newsroom signature chime. Used in every intro build.

---

## VIDEO

- **No video assets produced yet.** Video pipeline is specced, not built.
- Strategy docs: `~/workspace/ai-reporter-pipeline/VIDEO_GENERATION.md`, `VIDEO_DEALS.md`, `VIRAL_AI_VIDEO_TOOLS.md` (this VM)
- Newsroom desk environment (for future video backgrounds): `~/workspace/newsroom-live/environments/` — `newsroom-desk-v2.jpg` (approved), v1
- Brand video refs on Pro: `~/Desktop/Workspace.nosync/align-newsroom-brand/dive-video/`, `hero-video/`

---

## IMAGES

### Reporter portraits (SOURCE OF TRUTH)
**MacBook Pro:** `~/Desktop/Workspace.nosync/align-newsroom-brand/portraits/`
- `REPORTER_PORTRAIT_STYLE_SPEC.md` — the style bible (cross-hatch lithograph, B&W person, parchment, torn-paper color blocks)
- `batch-output/` — generated portraits, `batch-briefs/` — generation briefs
- **VM mirror:** `~/workspace/reporter-portraits/` — 174 files, 165 MB (46 + variants + 12 additional)

### Reporter scenery (SOURCE OF TRUTH)
**This VM:** `~/workspace/reporter-scenery/`
- 26 files, 5.2 MB
- `backgrounds/{slug}-v2.jpg` — 1920×1080 photorealistic, no people, no text (5 done: elena, marisol, tarun, hana, graham)
- `profiles/{slug}.md` — "What's on the desk (and why)"
- `continuity/{slug}.json` — scene version + change log
- `RULES.md` — every object must earn its place

### Brand / logos / globe
**MacBook Pro:** `~/Desktop/Workspace.nosync/align-newsroom-brand/`
- 1,396 files, 1.1 GB
- `globe/` — `EASTER-EGGS.md`, textures (v10/v11/v12 equirect), `easter-eggs-v2/`, `deploy-bundle/`
- `logos/` + `logos-by-brand/` — 6 brand sheets (AlignHeart, Expedia Parts, Creytix, Boats Studios, Peak Powertrain, Ironclad), NOT yet vectorized
- `article-images/`, `story-images/`, `headers/`, `headers-dna/`, `headers-new/`, `social/`, `favicon/`, `monogram/`, `wordmark*`, `palette.json/md`, `typeface/`, `typography/`
- `build-bible/`, `copy/`, `essence/`, `grade/`, `design-sheets/`, `APPROVAL-WORKFLOW.md`
- **VM:** `~/workspace/align-newsroom-logo/` (89 files) — working copies

### Article images
**This VM:** `~/workspace/article-images-v2/` — 19 approved gritty-newsprint heroes (`.webp`, zero text, 16:9). Prompt system: `~/workspace/align-newsroom-prompt-system-v2.md`.

---

## SCRIPTS / CODE

### Chatterbox sidecar (Cratex Voice Labs)
**Mac Studio:** `/Users/mac-mini-studio/expedia-data/voice-worker/chatterbox-sidecar-el-prod/`
- Port **4123**, device=mps, multilingual model. API: `POST /v1/audio/speech` `{"model":"chatterbox","input":"...","voice":"..."}` ✓ correct. `/v1/text-to-speech/{id}` → 404.
- Voice add: `POST /v1/voices/add` (multipart field name is `files`, not `file`)
- ⚠️ MPS memory leak: OOMs after ~25–30 requests → restart via launchd plist (NOT `python3 app.py`). First request after load ~60s. Reference clips ≤30s.
- Fish Speech S2-Pro self-hosted: port **4124** (Research License — non-commercial only)

### Podcast pipeline
**This VM:** `~/workspace/podcasts/*.py` — `scripts.py` (script gen), `mix.py` (assembly), `gen_fixed_episodes.py`, `assemble_fixed_episodes.py`

### Audio asset manager
**This VM:** `~/workspace/audio-asset-system/asset_manager.py` — register/approve/reject/supersede/cleanup/tag

### Site frontend
**MacBook Pro:** `~/Desktop/Workspace.nosync/newsroom-build/align-newsroom-front/`
- 1,467 files (with newsroom-build), 153 MB. Working dir per prior notes: `/Users/ricardo/nr-design-wt/align-newsroom-front/` — verify which is current before editing.
- Publish: `~/publish-newsroom.sh` → `~/nr-deploy-newsroom/` (backup each run). Commits use `ALLOW_STATE_COMMIT=1`. **No git remote — never pushed.**
- Also in newsroom-build: `podcast/` (ep001 + scripts), `tools/chart-gen/`, `gov-rating-pipeline/`, `reporters-meta.json`

### OYA / gov ratings pipeline
**MacBook Pro:** `~/Desktop/Workspace.nosync/newsroom-oya/` + `~/Desktop/Workspace.nosync/.worktrees/pup-h14/newsroom-oya/` (existing engine)

---

## DOCS

**This VM:**
- `~/workspace/ai-reporter-pipeline/` — 30 files: `ARCHITECTURE.md`, `PRIORITY_BRAIN_V2.md`, `VOICE_FACE_MATCHING.md`, `AI_CALLING.md`, `LORA_RESPONSES.md`, `VIDEO_GENERATION.md`, `INSTAGRAM_AVATARS.md`, `FISH_AUDIO_VOICES.md`, `pilot/` (5 pilot content packs)
- `~/workspace/voice-psychology/ANNOUNCER_VOICE_RESEARCH.md` — announcer voice science + product-wide casting framework + evaluation checklist
- `~/workspace/reporter-dossier.md` + `reporter-dossier-identities-v2.md` — 58 reporters, zero duplicate beats
- `~/workspace/reporter-intel/` — 105 files: per-reporter `briefs/` + `pages/`
- `~/workspace/goals/align-newsroom-intro-audio-build/` — goal workspace (GOAL.md, briefs, crons, files, hidden_files)
- `~/workspace/ASSET_AUDIT_VOICE_AUDIO.md`, `~/workspace/voice-audit/`, `~/workspace/voice-resources/` (2,049 files, 38 MB), `~/workspace/voice-stack-survey/`
- `~/workspace/newsroom-parity/` — 2,564 files, 631 MB ⚠️ large, verify before cleanup

**MacBook Pro:**
- `~/Desktop/Workspace.nosync/newsroom-voices/orchestra/ORCHESTRA.md`
- `~/Desktop/Workspace.nosync/align-newsroom-brand/APPROVAL-WORKFLOW.md`
- `~/Desktop/Workspace.nosync/newsroom-build/REQUEST-FOR-COMMENT-POLICY.md`, `SEPARATION-POLICY.md`
- ~25 other `newsroom-*` dirs: `newsroom-deploy/`, `newsroom-connectors/`, `newsroom-loop/`, `newsroom-articles/`, `newsroom-oya/`, `newsroom-design/`, `newsroom-map-build/`, … (see `ls ~/Desktop/Workspace.nosync | grep newsroom`)

---

## SOURCE-OF-TRUTH SUMMARY

| Asset type | Canonical location | Mirror / working copy |
|---|---|---|
| Voice reference clips | Studio `expedia-data/chatterbox-voices/` | — |
| Per-reporter audio | Studio `expedia-data/reporter-voices/` | VM `~/workspace/reporter-voices/` |
| Raw voice sources | Studio `expedia-data/voice-sources/` | — |
| Chatterbox sidecar | Studio `expedia-data/voice-worker/` | — |
| Intro sound design | VM `~/workspace/video-sample/` (workbench) | Approved → `audio-asset-system/registry.json` |
| Approval registry | VM `~/workspace/audio-asset-system/` | — |
| Podcast episodes | VM `~/workspace/podcasts/` | — |
| Orchestra/jingles/combos | Pro `newsroom-voices/` | VM `video-sample/orch-*` (pulls) |
| Chime | VM `~/workspace/newsroom-live/chime.mp3` | — |
| Portraits | Pro `align-newsroom-brand/portraits/` | VM `~/workspace/reporter-portraits/` |
| Scenery | VM `~/workspace/reporter-scenery/` | — |
| Logos/globe/brand | Pro `align-newsroom-brand/` | VM `~/workspace/align-newsroom-logo/` |
| Site frontend | Pro `newsroom-build/align-newsroom-front/` | `~/nr-deploy-newsroom/` (deploy staging) |
| Strategy docs | VM `~/workspace/ai-reporter-pipeline/` | — |
| Voice research | VM `~/workspace/voice-psychology/` | — |
| Reporter dossiers | VM `~/workspace/reporter-dossier*.md` | — |

## KNOWN CLEANUP CANDIDATES

1. `~/workspace/video-sample/` — 1,808 files; intro v1–v11 superseded by v12/FINAL. Run through `asset_manager.py reject` after Ricardo confirms.
2. `~/workspace/newsroom-voices/` — `newsroom-ambience-v2.wav` CONTAMINATED (synth phone baked in). Replaced by `newsroom-chatter-clean.wav`.
3. `~/workspace/newsroom-parity/` — 631 MB, 2,564 files. Contents unverified; audit before touching.
4. `~/workspace/voice-resources/` — 2,049 files, 38 MB. Audit before touching.
5. `~/workspace/reporter-voices-fixed/` — empty dir, remove.
6. Pro `newsroom-voices/` brief-pipeline `out/` — 10 old briefs; superseded by VM podcast pipeline.
