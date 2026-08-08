# Àmì — Yorùbá tone game

A small browser game for learning Yorùbá **tone** and **vowel quality**. Learners
choose the correctly-marked word; minimal pairs (words that look identical but
change meaning with tone/vowel) are the main teaching device.

It is a **static web app** — plain `index.html` plus two JSON data files. No
server, no database, no cost. Progress is saved in the browser (localStorage).

## Run it locally

Do **not** double-click `index.html` (a `file://` page can't load the data).
Start a tiny web server from this folder instead:

```
python3 -m http.server
```

Then open **http://localhost:8000**.

## Deploy for free

Push to GitHub, then either:
- **GitHub Pages:** repo → Settings → Pages → deploy from branch → `main` / root.
- **Vercel:** import the repo, framework preset **Other**, no build step.

## Files

| File | What it is |
|---|---|
| `index.html` | The whole game (HTML/CSS/JS). **Source of truth.** |
| `questions.json` | Sentence-level questions. |
| `families.json` | Minimal-pair word families. Word levels are generated from these. |
| `audio/` | Native recordings (MP3), named per `RECORDING_LIST.csv`. |
| `RECORDING_LIST.csv` | The 101 words to record, with the exact filename for each. |
| `build_audio_manifest.py` | Scans `audio/` and writes `audio.json` so recordings light up in the game. |
| `generate_family_candidates.py` | Drafts new families from the afri-dict dictionary for **native review**. |
| `PROJECT_STATUS.md` | What's done, decisions, and the roadmap. |

## Adding content

- **Words/sentences:** edit `families.json` / `questions.json` (see existing
  entries for the shape). Every item should be checked by a native speaker.
- **Audio:** record the words in `RECORDING_LIST.csv` as MP3 into `audio/`, then
  run `python3 build_audio_manifest.py`.
- **Expand from the dictionary:** run `python3 generate_family_candidates.py` to
  draft candidate families from afri-dict, then review before merging.

See `PROJECT_STATUS.md` for the full status and roadmap.
