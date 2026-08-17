# Audio production — tools, techniques, recipes

Reference for producing audio artifacts (NPC voicemails, phone calls, ambient scenes, security-cam clips) for Underleaf. All techniques described here are known-working as of 2026-08-16 and can be reproduced with the specified tools.

**Scope:** this is a public tools-and-techniques doc. Actual voice-reference source files are private (see the DM's local `private-assets/` — not in any git repo). Generated MP3s are committed to `underleaf/assets/audio/`.

---

## Stack (all free, all local)

| Tool | Purpose | Install |
|---|---|---|
| **piper** | Fast, robotic-sounding TTS (best for in-fiction robotic voice: automated menus, Morgan's own TTS-based communications) | `pip install piper-tts` + download voice files |
| **coqui-tts (XTTS v2 fork)** | High-quality neural TTS with voice cloning + prosody transfer via reference audio (best for NPCs) | See install notes below |
| **ffmpeg** | Phone-quality filtering, mixing, level normalization, effects | Standard package |
| **freesound.org API** | Downloading CC0 ambient recordings + effects | Free account + API key |

Piper works well when you WANT it to sound robotic (Morgan's in-character use of TTS). Coqui XTTS v2 is what to reach for when you want the delivery to sound human.

### Coqui-tts install (CPU-only, project-scoped venv)

Full working install as of 2026-08-16. Python 3.12. Pin these versions if newer break something:

```bash
python3 -m venv /path/to/tts-venv
source /path/to/tts-venv/bin/activate
pip install --upgrade pip
pip install coqui-tts
pip install 'transformers<5.0'                          # newer transformers removes symbols coqui-tts imports
pip install 'coqui-tts[codec]'                          # torchcodec dep
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu       # CPU-only PyTorch
pip uninstall torchcodec -y                             # replace GPU torchcodec with CPU variant
pip install torchcodec --index-url https://download.pytorch.org/whl/cpu
```

Verify: `python -c "import torchcodec; print('OK', torchcodec.__version__)"` should print `OK 0.16.0+cpu` (or later `+cpu`).

Model cache goes under `XDG_DATA_HOME/tts/`. Explicitly redirect to a project-local path to keep model files inside the tree:

```bash
export XDG_DATA_HOME=/path/to/tts-cache
export COQUI_TOS_AGREED=1              # auto-accept XTTS's CPML license prompt (personal/non-commercial use)
```

XTTS v2 model is ~2GB on first download. Real-time factor on CPU ≈ 2-3x (40s of audio in ~2-3 minutes).

**License:** XTTS v2 uses the Coqui Public Model License — non-commercial use only. Fine for personal campaigns; needs replacement if the campaign is ever sold.

---

## Production pipeline (NPC voicemail example)

### 1. Write two transcript versions

Per the `audio-inclusion-pattern` convention:

- **`<slug>-transcript.txt`** — clean readable English for the DM to read aloud when offline. Standard punctuation. Goes into the DM-facing scene document.
- **`<slug>-tts-input.txt`** — same content but with conservative prosody markers for TTS (em-dashes and 1-2 strategic ellipses at meaningful pauses; nothing more). XTTS respects punctuation as prosody signal but does NOT support SSML.

**Prosody-marker calibration** (learned the hard way):
- Ellipses in the middle of clauses cause XTTS to insert random pauses. Use SPARINGLY — maybe two per voicemail max.
- Em-dashes work well for strategic beat-changes (a detective's vocal tic; a pivot in thought). Reliable.
- Very short single-word sentences (e.g., "Nine years ago.") often play weird — the sentence-splitter processes them as isolated units with their own prosody. Prefer commas.
- Trust the reference-audio's cadence for most of the delivery; use markers only for the 1-2 moments that need explicit shaping.

### 2. Generate raw TTS via XTTS with voice cloning

```bash
tts --text "$(cat ortiz-voicemail-tts-input.txt)" \
    --model_name "tts_models/multilingual/multi-dataset/xtts_v2" \
    --language_idx en \
    --speaker_wav /path/to/voice-reference.wav \
    --out_path npc-name-raw.wav
```

Voice references live outside the public repo (private) — see the DM's local `private-assets/` tree.

Alternative if you don't have a reference clip: `--speaker_idx "Alison Dietlinde"` (or one of ~60 built-in XTTS speakers). List with `tts --list_speaker_idxs --model_name "tts_models/multilingual/multi-dataset/xtts_v2"`.

### 3. Post-process to phone-quality with ffmpeg

Standard POTS phone-line signature (300-3400 Hz bandpass + compressor + 8kHz mono):

```bash
ffmpeg -y -i npc-name-raw.wav \
  -af "atempo=1.10, highpass=f=300, lowpass=f=3400, acompressor=threshold=0.089:ratio=9:attack=200:release=1000, loudnorm=I=-18:TP=-2" \
  -ar 8000 -ac 1 -b:a 32k \
  npc-name-voice.mp3
```

**Speed control:** `atempo=1.10` speeds up ~10%. Ranges: 1.0 = natural, 1.05-1.15 = businesslike, 0.9-0.95 = slower/deliberate. `atempo` preserves pitch, only changes speed.

**Dynamic pacing** (slower opening, faster main): split the raw WAV at a natural boundary, apply different `atempo` values, concat. Best used when a character would naturally "settle into" a message:

```bash
ffmpeg -y -i raw.wav \
  -filter_complex "[0:a]atrim=0:3,asetpts=PTS-STARTPTS,atempo=1.03[slow]; [0:a]atrim=3,asetpts=PTS-STARTPTS,atempo=1.18[fast]; [slow][fast]concat=n=2:v=0:a=1[voiceraw]; [voiceraw]highpass=f=300, lowpass=f=3400, acompressor=threshold=0.089:ratio=9:attack=200:release=1000, aresample=8000[voice]" \
  -map "[voice]" -ar 8000 -ac 1 -b:a 32k \
  npc-name-voice.mp3
```

Alternate phone characters:
- **GSM cellular:** 200-3500 Hz bandpass, softer compression
- **Wideband cell:** 50-7000 Hz bandpass (much clearer, sounds more "modern smartphone call")
- **Voicemail-menu tone:** append a 1 kHz sine beep at the end (see `make-voicemail.sh` in DM tmp dir for the recipe)

### 4. Add ambient background (mix)

**ALWAYS analyze the ambient BEFORE mixing:**

```bash
# Loudness (integrated LUFS), true peak
ffmpeg -i ambient.mp3 -af "ebur128=peak=true" -f null - 2>&1 | grep -E "^\s+I:|^\s+Peak:|^\s+LRA:"

# Silent sections >= 1s at < -40dB (catches "silent intro" traps)
ffmpeg -i ambient.mp3 -af "silencedetect=noise=-40dB:d=1.0" -f null - 2>&1 | grep silence
```

Freesound recordings vary WILDLY in level — anywhere from -24 LUFS (well-mastered) to -38 LUFS (nearly-silent). If a source is 10 dB quieter than another, compensate at the `volume=` step. Otherwise "-8dB relative" turns into "-46 LUFS actual" and disappears in the mix.

**Mix recipe** (voice + ambient, both bandpassed for phone quality, ambient duckable via `volume` compensation):

```bash
ffmpeg -y -i voice-raw.wav -i ambient.mp3 \
  -filter_complex "[0:a]atempo=1.10, highpass=f=300, lowpass=f=3400, acompressor=threshold=0.089:ratio=9:attack=200:release=1000, aresample=8000[voice]; [1:a]atrim=0:40, highpass=f=200, lowpass=f=2000, volume=+5dB, aresample=8000[amb]; [voice][amb]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[mix]; [mix]loudnorm=I=-18:TP=-2[out]" \
  -map "[out]" -ar 8000 -ac 1 -b:a 32k \
  npc-name-with-ambient.mp3
```

Key filter details:
- **`amix normalize=0`** — critical. Default amix behavior halves each input's gain to prevent clipping (a hidden -6dB attenuation). We want manual gain control, so disable.
- **Final `loudnorm=I=-18:TP=-2`** — normalizes the whole mix to broadcast standard -18 LUFS, -2 dBFS true peak. Catches gain-staging errors before shipping.
- **`atrim=0:40`** — trims ambient to voice duration; loops longer or shorter recordings as needed.
- **Ambient `volume=+5dB`** — a compensation offset; the correct number depends on source level (compensate for LUFS delta vs. voice) plus the desired relative loudness.

### 5. Verify

```bash
# Post-mix loudness check
ffmpeg -i final.mp3 -af "ebur128=peak=true" -f null - 2>&1 | grep -E "^\s+I:|^\s+Peak:"
# Target: I ≈ -18 to -20 LUFS, Peak ≈ -1 to -2 dBFS
```

If mix and voice-only versions of the same clip are more than 2 dB apart in LUFS, the mixing is wrong (likely the `amix normalize` issue).

---

## Sourcing ambient audio (freesound.org)

Prefer **CC0** (public domain, no attribution required) for anything committed to the public repo. Attribution-required (CC-BY, CC-BY-SA) works but requires credit in the scene file.

API-key access: user's key at `~/.freesound-api.key`. Preview MP3s (lo/hi quality) are downloadable without OAuth — just use the key as `?token=<key>` on API queries. Actual downloads use the CDN URL from the response, no token needed on the CDN.

Search recipe:

```bash
export FREESOUND_KEY=$(cat ~/.freesound-api.key | tr -d '\n\r ')
curl -sS "https://freesound.org/apiv2/search/text/?query=<QUERY>&filter=license:%22Creative+Commons+0%22+duration:%5B30.0+TO+300.0%5D&fields=id,name,duration,previews&sort=downloads_desc&page_size=5&token=$FREESOUND_KEY" | jq '.results[]'
```

Then download the preview MP3 from the CDN URL in the response (`previews.preview-hq-mp3`).

**Rule: always analyze downloaded ambient BEFORE mixing.** See the mix section above.

---

## Directory conventions

- **`underleaf/assets/audio/`** — final MP3s (published)
- **`underleaf/assets/audio/<slug>-transcript.txt`** — DM-facing readable transcript alongside each audio file
- **DM tmp `tmp/<episode-planning>/audio/`** — working files: raw WAVs, TTS input variants, intermediate mixes, iteration outputs. Not published.
- **DM private `private-assets/voice-references/`** — voice-clone reference clips per NPC. Never published (source rights unclear).
- **DM private `tmp/tts-venv/`** — Python virtualenv for coqui-tts. Reusable across sessions.
- **DM private `tmp/tts-cache/`** — XTTS model cache (~2GB). Reusable across sessions.
- **DM private `tmp/piper-voices/`** — piper voice models (~60MB each). Reusable across sessions.

---

## What we've learned (log of gotchas as they were discovered)

- **Piper Amy voice is passable but flat.** Fine for robotic-in-character use. Not naturalistic enough for NPC voicemails.
- **XTTS v2 is significantly better** but needs voice-cloning reference for the best result — the built-in speakers are a step down from a well-chosen reference clip.
- **Phone bandpass masks a lot of TTS artifacts.** Even mediocre TTS sounds acceptable through a 300-3400 Hz bandpass because listeners expect phone audio to be lo-fi.
- **Prosody markers are risky.** Heavy use of ellipses causes weird pauses. Use conservatively.
- **`amix normalize=0` is required** for correct level control. Default `amix` silently halves each input's gain.
- **Freesound ambient levels vary by 15 dB or more** across otherwise similar recordings. Analyze first.
- **Torchcodec has GPU dependencies** even when torch is CPU-only. Reinstall from PyTorch's CPU index if the default one loads with libnvrtc errors.
- **Piper first-run downloads voice files** but not everything is under a stable URL forever — cache the downloaded ONNX + JSON locally rather than re-fetching each session.

---

## Not covered here

- Music generation (Suno, MusicGen) — not tried yet for Underleaf
- Real-time or in-app playback — Quire runtime doesn't currently render `<audio>` tags; audio playback is out-of-app for now
- Voice cloning of specific real people — do NOT do this (impersonation risk); use only samples we have rights to as generic reference voices
- Commercial use — XTTS's CPML license blocks commercial redistribution of the model output; if the campaign ever monetizes, we replace the TTS stack
