#!/usr/bin/env python3
"""
Genera tutti gli MP3 della voce di Astrid da audio_manifest.json via ElevenLabs.

Uso:
  export ELEVENLABS_API_KEY=...        # chiave solo in locale, mai committata
  python tools/generate_audio.py       # genera solo i file mancanti
  python tools/generate_audio.py --force   # rigenera tutto (consuma crediti)

Dipendenze: solo stdlib (urllib). Nessuna installazione richiesta.
Gli MP3 NON vanno committati: vengono generati in locale.
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error

VOICE_ID = "7tclrsOlhqwMBR23TChD"
API_URL = (
    f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    "?output_format=mp3_44100_128"
)
MODEL_ID = "eleven_multilingual_v2"
VOICE_SETTINGS = {
    "stability": 0.5,
    "similarity_boost": 0.75,
    "style": 0.0,
    "use_speaker_boost": True,
    "speed": 0.91,
}

PAUSE_BETWEEN = 0.4      # secondi tra una richiesta e l'altra
MAX_RETRIES_429 = 5      # tentativi su rate-limit

# Radici: lo script vive in tools/, il manifest e la cartella audio stanno nella root.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST_PATH = os.path.join(ROOT, "audio_manifest.json")


def fatal(msg):
    print(f"ERRORE: {msg}", file=sys.stderr)
    sys.exit(1)


def synth(api_key, text):
    """Chiama ElevenLabs e ritorna i byte MP3. Gestisce il backoff sul 429."""
    body = json.dumps({
        "text": text,
        "model_id": MODEL_ID,
        "voice_settings": VOICE_SETTINGS,
    }).encode("utf-8")

    attempt = 0
    while True:
        req = urllib.request.Request(API_URL, data=body, method="POST")
        req.add_header("xi-api-key", api_key)
        req.add_header("Content-Type", "application/json")
        req.add_header("Accept", "audio/mpeg")
        try:
            with urllib.request.urlopen(req) as resp:
                return resp.read()
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < MAX_RETRIES_429:
                attempt += 1
                # Rispetta Retry-After se presente, altrimenti backoff esponenziale.
                retry_after = e.headers.get("Retry-After")
                wait = float(retry_after) if retry_after else (2 ** attempt)
                print(f"    429 rate-limit, attendo {wait:.0f}s (tentativo {attempt}/{MAX_RETRIES_429})")
                time.sleep(wait)
                continue
            detail = ""
            try:
                detail = e.read().decode("utf-8", "replace")[:300]
            except Exception:
                pass
            raise RuntimeError(f"HTTP {e.code} {e.reason} {detail}")
        except urllib.error.URLError as e:
            raise RuntimeError(f"Errore di rete: {e.reason}")


def main():
    force = "--force" in sys.argv[1:]

    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        fatal("variabile d'ambiente ELEVENLABS_API_KEY non impostata. "
              "Esegui: export ELEVENLABS_API_KEY=...")

    if not os.path.isfile(MANIFEST_PATH):
        fatal(f"manifest non trovato: {MANIFEST_PATH}")

    try:
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            manifest = json.load(f)
    except json.JSONDecodeError as e:
        fatal(f"audio_manifest.json non e JSON valido: {e}")

    if not isinstance(manifest, list):
        fatal("audio_manifest.json deve essere un array di oggetti {file, text}.")

    total = len(manifest)
    generati = saltati = falliti = 0

    print(f"Manifest: {total} clip · modalita: {'FORCE (rigenera tutto)' if force else 'solo mancanti'}\n")

    for i, voce in enumerate(manifest, start=1):
        rel = voce.get("file")
        text = voce.get("text")
        if not rel or not text:
            print(f"[{i}/{total}] voce malformata, salto: {voce!r}")
            falliti += 1
            continue

        out_path = os.path.join(ROOT, rel)

        if os.path.isfile(out_path) and not force:
            print(f"[{i}/{total}] esiste, salto: {rel}")
            saltati += 1
            continue

        try:
            audio = synth(api_key, text)
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with open(out_path, "wb") as f:
                f.write(audio)
            print(f"[{i}/{total}] generato: {rel} ({len(audio)} byte)")
            generati += 1
        except Exception as e:
            print(f"[{i}/{total}] FALLITO: {rel} -> {e}", file=sys.stderr)
            falliti += 1

        time.sleep(PAUSE_BETWEEN)

    print(f"\nRiepilogo: generati={generati} · saltati={saltati} · falliti={falliti} · totale={total}")
    if falliti:
        sys.exit(1)


if __name__ == "__main__":
    main()
