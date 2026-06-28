"""
Àmì — a Yorùbá tone game (Streamlit).

Streamlit re-runs this file top to bottom on every click, so anything that must
survive a click (current screen, score, current question, hints left) lives in
st.session_state. No model, no training: the game is questions.json plus the
logic below.

Screens routed by st.session_state.screen:
home, play, results, learn, tonemarks, vowel, families, howto
"""

import json
import random
import streamlit as st

# ---------------------------------------------------------------- settings
GAME_NAME = "\u00c0m\u00ec"                 # change here when the team picks a name
ROUND_SIZE = 10                             # questions per round
POINTS_CORRECT = 10
HINTS_PER_ROUND = 3
TEAM = ["Esther", "Adesewa", "Blessing", "Siju", "(member 5)"]   # used in the report

@st.cache_data
def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

QUESTIONS = load("questions.json")
FAMILIES = load("families.json")

# result messages: a pool per score band, picked at random (English only)
MESSAGES = {
    "perfect": ["Perfect round. You read every tone correctly. You are a champion.",
                "Flawless, ten out of ten. Your ear for tone is excellent.",
                "A clean sweep. Every single answer was right."],
    "strong":  ["Very strong. Just a little more for a perfect score.",
                "Excellent work. You missed only a few.",
                "Almost perfect. Your tone reading is sharp."],
    "middle":  ["Good work. You are getting the hang of the tones.",
                "Solid round. Keep practising and the score will climb.",
                "Nicely done. A few more rounds will sharpen it."],
    "low":     ["You are getting there. Try another round.",
                "A fair start. Visit Learn, then play again.",
                "Keep going. Each round will make the tones clearer."],
    "vlow":    ["Do not worry, tones take practice. Visit Learn, then try again.",
                "Tone is tricky at first. Spend a moment in Learn and come back.",
                "A tough round. The Learn section will help, then give it another go."],
}

# ---------------------------------------------------------------- styling
st.set_page_config(page_title=GAME_NAME, page_icon="\u25CC\u0301", layout="centered")
st.markdown("""
<style>
:root{ --indigo:#1d2b53; --indigo2:#2c3e6b; --gold:#c8902a; --paper:#faf7f2;
       --good:#2e7d5b; --bad:#b23a48; --ink:#222838; }
.stApp{ background:var(--paper); }
.block-container{ max-width:680px; padding-top:2.2rem; }
.home{ text-align:center; margin:2.2rem 0 1.4rem; }
.title{ color:var(--indigo); font-weight:800; font-size:4rem; line-height:1;
       letter-spacing:-1px; margin:0; }
.marks{ font-size:2.6rem; letter-spacing:.6rem; color:var(--indigo); margin:.5rem 0 0;}
.marks b{ color:var(--gold); }
.h2{ color:var(--indigo); font-weight:800; font-size:1.7rem; margin:.2rem 0 .7rem; }
.sentence{ background:#fff; border:1px solid #ece5d8; border-left:5px solid var(--gold);
       border-radius:10px; padding:18px 20px; font-size:1.5rem; color:var(--ink); margin:.3rem 0; }
.hint{ color:#6b7280; font-size:1.02rem; margin:8px 2px 14px; }
.word{ font-size:2rem; font-weight:800; color:var(--indigo); text-align:center; }
.feed-good{ background:#eaf5ef; border-left:5px solid var(--good); color:#1c5a40;
       padding:14px 16px; border-radius:10px; font-size:1.02rem; }
.feed-bad{ background:#fbeef0; border-left:5px solid var(--bad); color:#7c2531;
       padding:14px 16px; border-radius:10px; font-size:1.02rem; }
.card{ background:#fff; border:1px solid #ece5d8; border-radius:10px; padding:12px 16px;
       margin-bottom:10px; }
.fam{ font-weight:800; color:var(--gold); font-size:1.15rem; }
.muted{ color:#6b7280; }
.lesson{ background:#fff; border:1px solid #ece5d8; border-radius:10px; padding:4px 20px; }
div.stButton>button{ width:100%; border-radius:10px; font-weight:700;
       border:1px solid var(--indigo); background:var(--indigo); color:#fff; padding:.55rem; }
div.stButton>button:hover{ background:var(--indigo2); border-color:var(--indigo2); color:#fff; }
div.stButton>button:disabled{ opacity:.5; }
</style>
""", unsafe_allow_html=True)

def go(screen):
    st.session_state.screen = screen

if "screen" not in st.session_state:
    st.session_state.screen = "home"
if "seen" not in st.session_state:
    st.session_state.seen = set()

# ---------------------------------------------------------------- round logic
def new_round():
    unseen = [q for q in QUESTIONS if q["id"] not in st.session_state.seen]
    if len(unseen) < ROUND_SIZE:
        st.session_state.seen = set()
        unseen = list(QUESTIONS)
    picks = random.sample(unseen, ROUND_SIZE)
    for q in picks:
        st.session_state.seen.add(q["id"])
    st.session_state.round = picks
    st.session_state.r_idx = 0
    st.session_state.points = 0
    st.session_state.streak = 0
    st.session_state.hints_left = HINTS_PER_ROUND
    # each question keeps its own memory so the player can move back and forth
    # and review answered questions without losing anything.
    st.session_state.rec = [{"answered": False, "picked": None, "hint": False}
                            for _ in picks]
    # lock a random left/right order for each question once (no rerun reshuffle,
    # and not biased by the answer-key skew).
    st.session_state.sides = [random.choice([["A", "B"], ["B", "A"]]) for _ in picks]
    go("play")

def goto(idx):
    st.session_state.r_idx = max(0, min(idx, len(st.session_state.round) - 1))

# ================================================================ HOME
def home():
    st.markdown(f'<div class="home"><div class="title">{GAME_NAME}</div>'
                f'<div class="marks">\u00e0 <b>a</b> \u00e1</div></div>', unsafe_allow_html=True)
    if st.button("Play"):
        new_round(); st.rerun()
    c1, c2 = st.columns(2)
    if c1.button("Learn"): go("learn"); st.rerun()
    if c2.button("How to play"): go("howto"); st.rerun()

# ================================================================ PLAY
def play():
    rd = st.session_state.round
    i = st.session_state.r_idx
    q = rd[i]
    rec = st.session_state.rec[i]
    n = len(rd)
    all_answered = all(r["answered"] for r in st.session_state.rec)

    top = st.columns([3, 1])
    streak_txt = f"   \u00b7   streak {st.session_state.streak}" if st.session_state.streak else ""
    top[0].caption(f"Question {i+1} of {n}   \u00b7   {st.session_state.points} pts{streak_txt}")
    if top[1].button("Quit", key="quit"):
        go("home"); st.rerun()
    st.progress((i + 1) / n)

    st.markdown(f'<div class="sentence">{q["sentence"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="hint">\U0001F4AC {q["translation"]}</div>', unsafe_allow_html=True)

    left, right = st.session_state.sides[i]

    def option(col, key):
        opt = q[key]
        col.markdown(f'<div class="word">{opt["word"]}</div>', unsafe_allow_html=True)
        if rec["hint"] or rec["answered"]:
            col.markdown(f'<div class="muted" style="text-align:center">{opt["meaning"]}</div>',
                         unsafe_allow_html=True)
        if col.button("Choose", key=f"{key}{i}", disabled=rec["answered"]):
            rec["answered"] = True
            rec["picked"] = key
            if key == q["correct"]:
                st.session_state.points += POINTS_CORRECT
                st.session_state.streak += 1
                if st.session_state.streak >= 3:
                    st.balloons()
            else:
                st.session_state.streak = 0
            st.rerun()

    c1, c2 = st.columns(2)
    option(c1, left)
    option(c2, right)

    # Hint: 3 per round, no point cost. Reveals the meanings for this question.
    if not rec["answered"]:
        if rec["hint"]:
            st.caption(f"Hints left: {st.session_state.hints_left}")
        else:
            out = st.session_state.hints_left == 0
            label = "Hint" if not out else "No hints left"
            if st.button(f"{label}  ({st.session_state.hints_left} left)", key=f"hint{i}", disabled=out):
                rec["hint"] = True
                st.session_state.hints_left -= 1
                st.rerun()

    if rec["answered"]:
        if rec["picked"] == q["correct"]:
            st.markdown(f'<div class="feed-good">\u2713 Correct. {q["explanation"]}</div>',
                        unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="feed-bad">\u2717 Not quite. The answer is '
                        f'<b>{q[q["correct"]]["word"]}</b>. {q["explanation"]}</div>',
                        unsafe_allow_html=True)

    # navigation: move back to review, or forward through the round
    st.write("")
    nav = st.columns(2)
    if nav[0].button("\u2190 Previous", key=f"prev{i}", disabled=(i == 0)):
        goto(i - 1); st.rerun()
    if nav[1].button("Next \u2192", key=f"next{i}", disabled=(i == n - 1)):
        goto(i + 1); st.rerun()

    # finish is offered once every question has been answered
    if all_answered:
        if st.button("See your score", key="finish"):
            go("results"); st.rerun()

# ================================================================ RESULTS
def results():
    correct = sum(1 for j, r in enumerate(st.session_state.rec)
                  if r["answered"] and r["picked"] == st.session_state.round[j]["correct"])
    st.session_state.last_correct = correct
    if correct == ROUND_SIZE:    band = "perfect"
    elif correct >= 8:           band = "strong"
    elif correct >= 6:           band = "middle"
    elif correct >= 4:           band = "low"
    else:                        band = "vlow"
    msg = random.choice(MESSAGES[band])
    st.markdown('<div class="h2">Round complete</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sentence">You got <b>{correct} / {ROUND_SIZE}</b> '
                f'correct &nbsp;\u00b7&nbsp; {st.session_state.points} points<br>'
                f'<span class="muted">{msg}</span></div>', unsafe_allow_html=True)
    st.write("")
    if st.button("Play again"):
        new_round(); st.rerun()
    c1, c2 = st.columns(2)
    if c1.button("Learn"): go("learn"); st.rerun()
    if c2.button("Home"): go("home"); st.rerun()

# ================================================================ LEARN
def learn():
    st.markdown('<div class="h2">Learn</div>', unsafe_allow_html=True)
    if st.button("Tone marks (the three tones)"): go("tonemarks"); st.rerun()
    if st.button("Vowel quality (the subdot)"): go("vowel"); st.rerun()
    if st.button("Word families"): go("families"); st.rerun()
    st.write("")
    if st.button("\u2190 Home", key="learn_home"): go("home"); st.rerun()

def tonemarks():
    st.markdown('<div class="h2">Tone marks, the three tones</div>', unsafe_allow_html=True)
    st.markdown("""<div class="lesson">

Yor\u00f9b\u00e1 has three tones. Think of them like the notes **do, re, mi**.

- **Low (do).** Written with a grave mark, like **\u00e0**. Example: *\u00ecs\u00e0l\u1EB9\u0300*.
- **Mid (re).** No mark at all, like **a**. This is the plain, middle voice.
- **High (mi).** Written with an acute mark, like **\u00e1**. Example: *\u00f2k\u00e8*.

Many Yor\u00f9b\u00e1 words are spelled with the same letters but mean different
things. The tone mark is what tells them apart, in writing and in speech. This
game is about spotting that difference.

</div>""", unsafe_allow_html=True)
    if st.button("\u2190 Back to Learn", key="tm_back"): go("learn"); st.rerun()

def vowel():
    st.markdown('<div class="h2">Vowel quality, the subdot</div>', unsafe_allow_html=True)
    st.markdown("""<div class="lesson">

Some Yor\u00f9b\u00e1 letters carry a small dot underneath: **\u1EB9, \u1ECD, \u1E63**.
This dot is called the **subdot**, and it changes the sound the letter makes.

- **e** and **\u1EB9** are different sounds. The **e** is closed, like the *ay* in
  *day*. The **\u1EB9** is more open, like the *e* in *bed*.
- **o** and **\u1ECD** are different too. The **o** is closed, like the *o* in *go*.
  The **\u1ECD** is more open, like the *aw* in *saw*.
- **s** and **\u1E63** differ as well. The **\u1E63** is the *sh* sound, as in *shoe*.

Because the subdot changes the sound, it can change the meaning of a word, just
like a tone mark does. Some questions in this game differ in both their tone and
their vowel quality, and the feedback will tell you when that happens.

</div>""", unsafe_allow_html=True)
    if st.button("\u2190 Back to Learn", key="vq_back"): go("learn"); st.rerun()

def families():
    st.markdown('<div class="h2">Word families</div>', unsafe_allow_html=True)
    st.write("Words that share the same letters but change meaning with tone or "
             "vowel. Study these, then test yourself in Play.")
    for fam in FAMILIES:
        rows = "".join(
            f'<div>\u2022 <b>{m["word"]}</b> <span class="muted">{m["meaning"]}</span></div>'
            for m in fam["members"])
        st.markdown(f'<div class="card"><div class="fam">{fam["key"]}</div>{rows}</div>',
                    unsafe_allow_html=True)
    if st.button("\u2190 Back to Learn", key="fam_back"): go("learn"); st.rerun()

# ================================================================ HOW TO PLAY
def howto():
    st.markdown('<div class="h2">How to play</div>', unsafe_allow_html=True)
    st.markdown(f"""<div class="lesson">

1. Read the Yor\u00f9b\u00e1 sentence and the English line under it.
2. Yor\u00f9b\u00e1 uses three tone marks: low (**\u00e0**), mid (**a**, no mark),
   high (**\u00e1**). They change what a word means.
3. Pick the word whose marks fit the sentence.
4. Stuck? Use a **Hint** to reveal the meanings. You get {HINTS_PER_ROUND} hints each round.

You score {POINTS_CORRECT} points for each correct answer, and each round has
{ROUND_SIZE} questions. New to tones? Open **Learn** first.

</div>""", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    if c1.button("Play now"): new_round(); st.rerun()
    if c2.button("\u2190 Home", key="howto_home"): go("home"); st.rerun()

# ---------------------------------------------------------------- router
SCREENS = {"home": home, "play": play, "results": results, "learn": learn,
           "tonemarks": tonemarks, "vowel": vowel, "families": families, "howto": howto}
SCREENS.get(st.session_state.screen, home)()
