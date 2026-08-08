"""
Build audio.json from the recordings you have actually saved.

Workflow:
  1. Record the words listed in RECORDING_LIST.csv (one clip per word form).
  2. Save each clip in the audio/ folder using the EXACT name in the
     "filename_to_save" column (e.g. audio/003_aya.mp3).
  3. Run:  python3 build_audio_manifest.py
     This scans audio/ and writes audio.json mapping each recorded word to its
     file. Words you have not recorded yet are simply left out — the game shows
     a 🔊 button only for words that have a file, so there are never dead buttons.

Re-run it whenever you add more recordings.
"""

import csv, json, os

rows = list(csv.DictReader(open("RECORDING_LIST.csv", encoding="utf-8")))
mapping = {}
missing = 0
for r in rows:
    path = r["filename_to_save"]
    if os.path.isfile(path):
        mapping[r["word"]] = path
    else:
        missing += 1

with open("audio.json", "w", encoding="utf-8") as fh:
    json.dump(mapping, fh, ensure_ascii=False, indent=1)

print(f"audio.json written: {len(mapping)} recorded, {missing} still to record "
      f"(of {len(rows)} total).")
