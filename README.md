# Àmì — a Yorùbá tone game

A small classroom game. Each question shows a Yorùbá sentence with a blank and
two words that look the same but differ in tone (and sometimes vowel quality),
so they mean different things. The player picks the one that fits.

No model, no training data: just the question bank plus the logic in `app.py`.

## Files
- `app.py` — the game (Streamlit), multi-screen: Home, Play, Learn, How to play, About
- `questions.json` — 50 questions with explanations
- `families.json` — word families for the Learn screen
- `requirements.txt` — dependencies

## Run on your computer
    pip install -r requirements.txt
    streamlit run app.py

## Put it online (free) — Streamlit Community Cloud
1. Upload all four files to a GitHub repo.
2. Go to https://share.streamlit.io and sign in with GitHub.
3. New app, pick the repo, main file `app.py`, Deploy. Public link in minutes.

## Easy edits
- Game name: `GAME_NAME` at the top of `app.py`.
- Team names: `TEAM` at the top of `app.py`.
- Questions per round: `ROUND_SIZE`.
- Add more questions: append to `questions.json` in the same shape, then
  regenerate families if you like.
