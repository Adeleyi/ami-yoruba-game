# Recordings go here

Record the 101 word forms listed in `../RECORDING_LIST.csv` (one short clip per
word). Save each as **MP3**, using the exact name from the `filename_to_save`
column — e.g. the row for `aya` (wife) is saved as `003_aya.mp3` in this folder.

Tips:
- One clip = one word, said clearly, in a quiet room, consistent volume.
- A native speaker should record these; tone must be correct.
- Keep a WAV master if you like, but export **MP3** for the app (small + plays
  everywhere).

When you have recorded some words, run from the project root:

    python3 build_audio_manifest.py

That writes `audio.json`, and the game automatically shows a 🔊 button for every
word it finds a recording for. Words not yet recorded stay silent (no button).
