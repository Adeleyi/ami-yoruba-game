"""
Àmì — Beginner Onboarding (standalone)
----------------------------------------
Separate script, built to match the style of the main app.py (single
self-contained HTML/CSS/JS block rendered via components.html), so it can
be reviewed on its own and merged in later.

Flow:
  1. Title screen — just "Àmì", nothing else
  2. "New to Yorùbá?" choice (minimal, no long paragraph)
  3. Tone intro — what tone is, where it occurs, how it changes meaning,
     minimal pairs
  4. "Guess the Tone" — no sentences yet. A bare word (+ optional picture)
     and its English meaning are shown; the learner picks the correctly
     toned Yorùbá form from the options. Feedback names the tone (low,
     mid, high) and explains why the other option(s) are wrong.
     Starts with monosyllabic words, then moves to bisyllabic words
     (mix of nouns, verbs, a couple of adjectives).

NOTE ON THE WORD LIST: monosyllabic (Level 1) has 9 starter items pending
the team's verified list. Bisyllabic (Level 2) now has 11 pairs / 22
items, all from the team's own data — two pairs (ọkọ/ọkọ̀, owó/òwò) were
already in this file and matched exactly, which is a good sign. Level 2
now draws a random round of 10 questions per playthrough, same as the
main app.

Author: Popoola Adesewa
Course: CLN 733 — Language Sound Systems, Group 3
"""

import json
import streamlit as st
import streamlit.components.v1 as components

# ---- settings you can edit -------------------------------------------------
GAME_NAME = "Àmì"
POINTS_CORRECT = 10
ROUND_SIZE = 10
# ---------------------------------------------------------------------------

st.set_page_config(page_title=f"{GAME_NAME} — Getting Started", page_icon="🎵", layout="centered")

st.markdown("""
<style>
#MainMenu, header, footer {visibility:hidden;}
.block-container{padding:0 !important; max-width:720px !important;}
[data-testid="stAppViewContainer"]{background:#faf7f2;}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# GUESS-THE-TONE ITEMS
# Each item: bare (untoned) spelling, optional picture (emoji placeholder —
# swap for a real image asset later), English gloss, word class, a list of
# tone-marked options, which one is correct, and an explanation.
# ---------------------------------------------------------------------------

GUESS1_MONO = [
    {
        "id": "g1_1", "bare": "fo", "picture": "🧼", "gloss": "to wash", "class": "verb",
        "options": [{"form": "fọ̀", "tone": "Low"}, {"form": "fọ́", "tone": "High"}],
        "correct": "fọ̀",
        "explanation": "fọ̀ is Low and means 'to wash'. fọ́ is High and means 'to break'.",
    },
    {
        "id": "g1_2", "bare": "fo", "picture": "🔨", "gloss": "to break", "class": "verb",
        "options": [{"form": "fọ̀", "tone": "Low"}, {"form": "fọ́", "tone": "High"}],
        "correct": "fọ́",
        "explanation": "fọ́ is High and means 'to break'. fọ̀ is Low and means 'to wash'.",
    },
    {
        "id": "g1_3", "bare": "ra", "picture": "🐌", "gloss": "to crawl / vanish", "class": "verb",
        "options": [{"form": "rá", "tone": "High"}, {"form": "rà", "tone": "Low"}],
        "correct": "rá",
        "explanation": "rá is High and means 'to crawl/vanish'. rà is Low and means 'rotten'.",
    },
    {
        "id": "g1_4", "bare": "ra", "picture": "🤢", "gloss": "rotten", "class": "adjective",
        "options": [{"form": "rá", "tone": "High"}, {"form": "rà", "tone": "Low"}],
        "correct": "rà",
        "explanation": "rà is Low and means 'rotten'. ra is Mid and means 'to crawl/vanish'.",
    },
    {
        "id": "g1_5", "bare": "gun", "picture": "🥣", "gloss": "to pound", "class": "verb",
        "options": [{"form": "gún", "tone": "High"}, {"form": "gùn", "tone": "Low"}],
        "correct": "gún",
        "explanation": "gún is High and means 'to pound'. gùn is Low and means 'to climb'.",
    },
    {
        "id": "g1_6", "bare": "gun", "picture": "🧗", "gloss": "to climb", "class": "verb",
        "options": [{"form": "gún", "tone": "High"}, {"form": "gùn", "tone": "Low"}],
        "correct": "gùn",
        "explanation": "gùn is Low and means 'to climb'. gún is High and means 'to pound'.",
    },
    {
        "id": "g1_7", "bare": "so", "picture": "👀", "gloss": "to watch over something", "class": "verb",
        "options": [{"form": "sọ́", "tone": "High"}, {"form": "sọ", "tone": "Mid"}],
        "correct": "sọ́",
        "explanation": "sọ́ is High and means 'to watch over something'. sọ is Mid and means 'to say something'.",
    },
    {
        "id": "g1_8", "bare": "so", "picture": "🗣️", "gloss": "to say something", "class": "verb",
        "options": [{"form": "sọ́", "tone": "High"}, {"form": "sọ", "tone": "Mid"}],
        "correct": "sọ",
        "explanation": "sọ is Mid and means 'to say something'. sọ́ is High and means 'to watch over something'.",
    },
    {
        "id": "g1_9", "bare": "mu", "picture": "✋", "gloss": "to take", "class": "verb",
        "options": [{"form": "mú", "tone": "High"}, {"form": "mu", "tone": "Mid"}],
        "correct": "mú",
        "explanation": "mú is High and means 'to take'. mu is Mid and means 'to drink'.",
    },
    {
        "id": "g1_10", "bare": "mu", "picture": "🥤", "gloss": "to drink", "class": "verb",
        "options": [{"form": "mú", "tone": "High"}, {"form": "mu", "tone": "Mid"}],
        "correct": "mu",
        "explanation": "mu is Mid and means 'to drink'. mú is High and means 'to take'.",
    },
    {
        "id": "g1_11", "bare": "ya", "picture": "📄", "gloss": "to tear", "class": "verb",
        "options": [{"form": "ya", "tone": "Mid"}, {"form": "yá", "tone": "High"}],
        "correct": "ya",
        "explanation": "ya is Mid and means 'to tear'. yá is High and means 'to borrow'.",
    },
    {
        "id": "g1_12", "bare": "ya", "picture": "📚", "gloss": "to borrow", "class": "verb",
        "options": [{"form": "ya", "tone": "Mid"}, {"form": "yá", "tone": "High"}],
        "correct": "yá",
        "explanation": "yá is High and means 'to borrow'. ya is Mid and means 'to tear'.",
    },
    {
        "id": "g1_13", "bare": "lo", "picture": "🚶", "gloss": "to go", "class": "verb",
        "options": [{"form": "lọ", "tone": "Mid"}, {"form": "lọ́", "tone": "High"}],
        "correct": "lọ",
        "explanation": "lọ is Mid and means 'to go'. lọ́ is High and means 'to twist'.",
    },
    {
        "id": "g1_14", "bare": "lo", "picture": "🌀", "gloss": "to twist", "class": "verb",
        "options": [{"form": "lọ", "tone": "Mid"}, {"form": "lọ́", "tone": "High"}],
        "correct": "lọ́",
        "explanation": "lọ́ is High and means 'to twist'. lọ is Mid and means 'to go'.",
    },
    {
        "id": "g1_15", "bare": "ja", "picture": "✂️", "gloss": "to cut", "class": "verb",
        "options": [{"form": "já", "tone": "High"}, {"form": "jà", "tone": "Low"}],
        "correct": "já",
        "explanation": "já is High and means 'to cut'. jà is Low and means 'to fight'.",
    },
    {
        "id": "g1_16", "bare": "ja", "picture": "🥊", "gloss": "to fight", "class": "verb",
        "options": [{"form": "já", "tone": "High"}, {"form": "jà", "tone": "Low"}],
        "correct": "jà",
        "explanation": "jà is Low and means 'to fight'. já is High and means 'to cut'.",
    },
    {
        "id": "g1_17", "bare": "fe", "picture": "↔️", "gloss": "wide", "class": "adjective",
        "options": [{"form": "fẹ̀", "tone": "Low"}, {"form": "fẹ́", "tone": "High"}],
        "correct": "fẹ̀",
        "explanation": "fẹ̀ is Low and means 'wide'. fẹ́ is High and means 'to want'.",
    },
    {
        "id": "g1_18", "bare": "fe", "picture": "❤️", "gloss": "to want", "class": "verb",
        "options": [{"form": "fẹ̀", "tone": "Low"}, {"form": "fẹ́", "tone": "High"}],
        "correct": "fẹ́",
        "explanation": "fẹ́ is High and means 'to want'. fẹ̀ is Low and means 'wide'.",
    },
    {
        "id": "g1_19", "bare": "sun", "picture": "😴", "gloss": "to sleep", "class": "verb",
        "options": [{"form": "sùn", "tone": "Low"}, {"form": "sún", "tone": "High"}],
        "correct": "sùn",
        "explanation": "sùn is Low and means 'to sleep'. sún is High and means 'to push'.",
    },
    {
        "id": "g1_20", "bare": "sun", "picture": "👉", "gloss": "to push", "class": "verb",
        "options": [{"form": "sùn", "tone": "Low"}, {"form": "sún", "tone": "High"}],
        "correct": "sún",
        "explanation": "sún is High and means 'to push'. sùn is Low and means 'to sleep'.",
    },
]

GUESS2_BI = [
    {
        "id": "g2_1",
        "bare": "oko",
        "picture": "💑",
        "gloss": "husband",
        "class": "noun",
        "options": [
            {"form": "ọkọ", "tone": "Mid-Mid"},
            {"form": "ọkọ̀", "tone": "Mid-Low"},
        ],
        "correct": "ọkọ",
        "explanation": "ọkọ (Mid-Mid) means 'husband'. ọkọ̀ (Mid-Low) means 'vehicle'. Two syllables — the second one carries the difference.",
    },
    {
        "id": "g2_2",
        "bare": "oko",
        "picture": "🚗",
        "gloss": "vehicle",
        "class": "noun",
        "options": [
            {"form": "ọkọ", "tone": "Mid-Mid"},
            {"form": "ọkọ̀", "tone": "Mid-Low"},
        ],
        "correct": "ọkọ̀",
        "explanation": "ọkọ̀ (Mid-Low) means 'vehicle'. ọkọ (Mid-Mid) means 'husband'.",
    },
    {
        "id": "g2_3",
        "bare": "ogun",
        "picture": "⚔️",
        "gloss": "war",
        "class": "noun",
        "options": [
            {"form": "ogun", "tone": "Mid-Mid"},
            {"form": "ogún", "tone": "Mid-High"},
        ],
        "correct": "ogun",
        "explanation": "ogun (Mid-Mid) means 'war'. ogún (Mid-High) means 'twenty'.",
    },
    {
        "id": "g2_4",
        "bare": "ogun",
        "picture": "2️⃣0️⃣",
        "gloss": "twenty",
        "class": "noun",
        "options": [
            {"form": "ogun", "tone": "Mid-Mid"},
            {"form": "ogún", "tone": "Mid-High"},
        ],
        "correct": "ogún",
        "explanation": "ogún (Mid-High) means 'twenty'. ogun (Mid-Mid) means 'war'.",
    },
    {
        "id": "g2_5",
        "bare": "owo",
        "picture": "💰",
        "gloss": "money",
        "class": "noun",
        "options": [
            {"form": "owó", "tone": "High-High"},
            {"form": "òwò", "tone": "Low-Low"},
        ],
        "correct": "owó",
        "explanation": "owó (High-High) means 'money'. òwò (Low-Low) means 'trade/business'.",
    },
    {
        "id": "g2_6",
        "bare": "owo",
        "picture": "🏪",
        "gloss": "trade / business",
        "class": "noun",
        "options": [
            {"form": "owó", "tone": "High-High"},
            {"form": "òwò", "tone": "Low-Low"},
        ],
        "correct": "òwò",
        "explanation": "òwò (Low-Low) means 'trade/business'. owó (High-High) means 'money'.",
    },
    {
        "id": "g2_7",
        "bare": "pade",
        "picture": "🤝",
        "gloss": "to meet",
        "class": "verb",
        "options": [
            {"form": "pàdé", "tone": "Low-High"},
            {"form": "padé", "tone": "Mid-High"},
        ],
        "correct": "pàdé",
        "explanation": "pàdé (Low-High) means 'to meet'. padé (Mid-High) means 'close/near'.",
    },
    {
        "id": "g2_8",
        "bare": "pade",
        "picture": "🚪",
        "gloss": "close / near",
        "class": "adjective",
        "options": [
            {"form": "pàdé", "tone": "Low-High"},
            {"form": "padé", "tone": "Mid-High"},
        ],
        "correct": "padé",
        "explanation": "padé (Mid-High) means 'close/near'. pàdé (Low-High) means 'to meet'.",
    },
    {
        "id": "g2_9",
        "bare": "iya",
        "picture": "👩",
        "gloss": "mother",
        "class": "noun",
        "options": [
            {"form": "ìyá", "tone": "Low-High"},
            {"form": "ìyà", "tone": "Low-Low"},
        ],
        "correct": "ìyá",
        "explanation": "ìyá (Low-High) means 'mother'. ìyà (Low-Low) means 'suffering'.",
    },
    {
        "id": "g2_10",
        "bare": "iya",
        "picture": "😢",
        "gloss": "suffering",
        "class": "noun",
        "options": [
            {"form": "ìyá", "tone": "Low-High"},
            {"form": "ìyà", "tone": "Low-Low"},
        ],
        "correct": "ìyà",
        "explanation": "ìyà (Low-Low) means 'suffering'. ìyá (Low-High) means 'mother'.",
    },
    {
        "id": "g2_11",
        "bare": "igba",
        "picture": "🥣",
        "gloss": "calabash",
        "class": "noun",
        "options": [
            {"form": "igbá", "tone": "Mid-High"},
            {"form": "igba", "tone": "Mid-Mid"},
        ],
        "correct": "igbá",
        "explanation": "igbá (Mid-High) means 'calabash'. igba (Mid-Mid) means 'two hundred'.",
    },
    {
        "id": "g2_12",
        "bare": "igba",
        "picture": "2️⃣0️⃣0️⃣",
        "gloss": "two hundred",
        "class": "noun",
        "options": [
            {"form": "igbá", "tone": "Mid-High"},
            {"form": "igba", "tone": "Mid-Mid"},
        ],
        "correct": "igba",
        "explanation": "igba (Mid-Mid) means 'two hundred'. igbá (Mid-High) means 'calabash'.",
    },
    {
        "id": "g2_13",
        "bare": "igba",
        "picture": "⏳",
        "gloss": "time",
        "class": "noun",
        "options": [
            {"form": "ìgbà", "tone": "Low-Low"},
            {"form": "ìgbá", "tone": "Low-High"},
        ],
        "correct": "ìgbà",
        "explanation": "ìgbà (Low-Low) means 'time'. ìgbá (Low-High) means 'garden eggs'.",
    },
    {
        "id": "g2_14",
        "bare": "igba",
        "picture": "🍆",
        "gloss": "garden eggs",
        "class": "noun",
        "options": [
            {"form": "ìgbà", "tone": "Low-Low"},
            {"form": "ìgbá", "tone": "Low-High"},
        ],
        "correct": "ìgbá",
        "explanation": "ìgbá (Low-High) means 'garden eggs'. ìgbà (Low-Low) means 'time'.",
    },
    {
        "id": "g2_15",
        "bare": "oko",
        "picture": "🪨",
        "gloss": "stone",
        "class": "noun",
        "options": [
            {"form": "òkò", "tone": "Low-Mid"},
            {"form": "oko", "tone": "Mid-Mid"},
        ],
        "correct": "òkò",
        "explanation": "òkò (Low-Mid) means 'stone'. oko (Mid-Mid) means 'farm'.",
    },
    {
        "id": "g2_16",
        "bare": "oko",
        "picture": "🌾",
        "gloss": "farm",
        "class": "noun",
        "options": [
            {"form": "òkò", "tone": "Low-Mid"},
            {"form": "oko", "tone": "Mid-Mid"},
        ],
        "correct": "oko",
        "explanation": "oko (Mid-Mid) means 'farm'. òkò (Low-Mid) means 'stone'.",
    },
    {
        "id": "g2_17",
        "bare": "aja",
        "picture": "🐕",
        "gloss": "dog",
        "class": "noun",
        "options": [
            {"form": "ajá", "tone": "Mid-High"},
            {"form": "àjà", "tone": "Low-Low"},
        ],
        "correct": "ajá",
        "explanation": "ajá (Mid-High) means 'dog'. àjà (Low-Low) means 'roof'.",
    },
    {
        "id": "g2_18",
        "bare": "aja",
        "picture": "🏠",
        "gloss": "roof",
        "class": "noun",
        "options": [
            {"form": "ajá", "tone": "Mid-High"},
            {"form": "àjà", "tone": "Low-Low"},
        ],
        "correct": "àjà",
        "explanation": "àjà (Low-Low) means 'roof'. ajá (Mid-High) means 'dog'.",
    },
    {
        "id": "g2_19",
        "bare": "ewa",
        "picture": "🫘",
        "gloss": "beans",
        "class": "noun",
        "options": [
            {"form": "ẹ̀wà", "tone": "Low-Low"},
            {"form": "ẹwà", "tone": "Mid-Low"},
        ],
        "correct": "ẹ̀wà",
        "explanation": "ẹ̀wà (Low-Low) means 'beans'. ẹwà (Mid-Low) means 'beauty'.",
    },
    {
        "id": "g2_20",
        "bare": "ewa",
        "picture": "✨",
        "gloss": "beauty",
        "class": "noun",
        "options": [
            {"form": "ẹ̀wà", "tone": "Low-Low"},
            {"form": "ẹwà", "tone": "Mid-Low"},
        ],
        "correct": "ẹwà",
        "explanation": "ẹwà (Mid-Low) means 'beauty'. ẹ̀wà (Low-Low) means 'beans'.",
    },
    {
        "id": "g2_21",
        "bare": "eko",
        "picture": "📚",
        "gloss": "education",
        "class": "noun",
        "options": [
            {"form": "ẹ̀kọ́", "tone": "Low-High"},
            {"form": "ẹ̀kọ", "tone": "Low-Mid"},
        ],
        "correct": "ẹ̀kọ́",
        "explanation": "ẹ̀kọ́ (Low-High) means 'education'. ẹ̀kọ (Low-Mid) means 'pap'.",
    },
    {
        "id": "g2_22",
        "bare": "eko",
        "picture": "🍲",
        "gloss": "pap",
        "class": "noun",
        "options": [
            {"form": "ẹ̀kọ́", "tone": "Low-High"},
            {"form": "ẹ̀kọ", "tone": "Low-Mid"},
        ],
        "correct": "ẹ̀kọ",
        "explanation": "ẹ̀kọ (Low-Mid) means 'pap'. ẹ̀kọ́ (Low-High) means 'education'.",
    },
]

GAME_HTML = r'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>AMI Onboarding</title>
<style>
:root{--indigo:#1d2b53;--indigo2:#2c3e6b;--gold:#c8902a;--paper:#faf7f2;
--good:#2e7d5b;--bad:#b23a48;--ink:#222838;}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);
font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;}
.wrap{max-width:680px;margin:0 auto;padding:24px 18px 70px;}
button{font-family:inherit;cursor:pointer;}
.btn{width:100%;border:1px solid var(--indigo);background:var(--indigo);color:#fff;
font-weight:700;border-radius:10px;padding:13px;font-size:1rem;margin-top:10px;}
.btn:hover{background:var(--indigo2);}
.btn.ghost{background:#fff;color:var(--indigo);}
.btn.gold{background:var(--gold);border-color:var(--gold);}
.btn:disabled{opacity:.45;cursor:default;}
.row{display:flex;gap:10px;}
.home{text-align:center;margin:4.5rem 0 2rem;}
.title{color:var(--indigo);font-weight:800;font-size:4.6rem;line-height:1;letter-spacing:-1px;margin:0;}
.h2{color:var(--indigo);font-weight:800;font-size:1.7rem;margin:.2rem 0 .7rem;}
.lead{color:#555;margin:0 0 8px;}
.meta{display:flex;justify-content:space-between;color:#6b7280;font-size:.85rem;margin:14px 0 6px;}
.bar{height:6px;background:#eadfce;border-radius:6px;overflow:hidden;margin-bottom:14px;}
.bar>i{display:block;height:100%;background:var(--gold);transition:width .3s;}
.lesson{background:#fff;border:1px solid #ece5d8;border-radius:10px;padding:6px 20px;line-height:1.65;}
.lesson li{margin:8px 0;}
.tonerow{display:flex;justify-content:center;gap:2.4rem;margin:1.4rem 0;}
.tonecell{text-align:center;}
.toneword{font-size:2.6rem;font-weight:800;color:var(--indigo);}
.tonelabel{color:#6b7280;font-size:.85rem;text-transform:uppercase;letter-spacing:.04em;margin-top:2px;}
.tonepitch{color:var(--gold);font-size:1rem;margin-top:2px;}
.muted{color:#6b7280;}
.promptcard{background:#fff;border:1px solid #ece5d8;border-radius:10px;padding:24px 20px;text-align:center;margin:.2rem 0 16px;}
.promptpic{font-size:2.6rem;margin-bottom:6px;}
.promptbare{font-size:1.1rem;color:#6b7280;letter-spacing:.03em;}
.promptgloss{font-size:1.6rem;font-weight:800;color:var(--indigo);margin-top:2px;}
.promptclass{color:#a8471f;font-size:.8rem;text-transform:uppercase;letter-spacing:.06em;margin-top:4px;}
.opts{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:12px;}
.card{background:#fff;border:2px solid #e6ded0;border-radius:12px;padding:16px 10px;text-align:center;cursor:pointer;transition:.15s;}
.card:hover{border-color:var(--indigo);}
.card.good{border-color:var(--good);background:#eaf5ef;}
.card.bad{border-color:var(--bad);background:#fbeef0;}
.card.lock{cursor:default;}
.word{font-size:1.9rem;font-weight:800;color:var(--indigo);}
.tonetag{color:#6b7280;font-size:.8rem;margin-top:4px;text-transform:uppercase;letter-spacing:.03em;}
.feed{margin-top:16px;padding:14px 16px;border-radius:10px;font-size:1.02rem;}
.feed.good{background:#eaf5ef;border-left:5px solid var(--good);color:#1c5a40;}
.feed.bad{background:#fbeef0;border-left:5px solid var(--bad);color:#7c2531;}
</style></head><body><div class="wrap"><div id="app"></div></div>
<script>
const NAME="__NAME__", PTS=__PTS__, ROUND=__ROUND__;
const G1=__G1__, G2=__G2__;
let stage=[], si=0, points=0, correctCount=0, seenG1=new Set(), seenG2=new Set();
let missed=[], redoMode=false;
const app=()=>document.getElementById("app");

function shuffle(a){for(let k=a.length-1;k>0;k--){const j=Math.random()*(k+1)|0;[a[k],a[j]]=[a[j],a[k]];}return a;}
function sample(a,n){return shuffle([...a]).slice(0,n);}
function pairKey(q){ return q.options.map(o=>o.form).slice().sort().join('|'); }
function buildPairs(items){
const map=new Map();
items.forEach(q=>{
const key=pairKey(q);
if(!map.has(key)) map.set(key,[]);
map.get(key).push(q);
});
return [...map.values()];
}

function levelMessage(pct){
if(pct>=80) return "🪶 You've Earned Your Wings — your ear for tone is sharp.";
if(pct>=50) return "Nice progress — a little more practice and it'll click.";
return "Tone takes practice. Feel free to try this level again.";
}

// ---------- Page 1: title only ----------
function titlePage(){
app().innerHTML=`
<div class="home"><div class="title">${NAME}</div></div>
<button class="btn" onclick="checkLevel()">Start</button>`;
}

// ---------- Page 2: new to Yorùbá? ----------
function checkLevel(){
app().innerHTML=`
<div class="h2">Are you new to Yorùbá?</div>
<button class="btn" onclick="introTones()">Yes, I'm new</button>
<button class="btn ghost" onclick="doneOnboarding()">No, I am not new</button>
<button class="btn ghost" onclick="titlePage()">← Back</button>`;
}

// ---------- Tone intro ----------
function introTones(){
app().innerHTML=`
<div class="h2">Yorùbá tone</div>
<div class="lesson">
<p>Yorùbá is a <b>tonal language</b>: the pitch of your voice on a word is part of the word itself, the same way a consonant or a vowel is. Say the same letters with a different pitch, and you often get a completely different word.</p>
<p>There are three tones. Think of them like the notes <b>do &ndash; re &ndash; mi</b>:</p>
</div>
<div class="tonerow">
<div class="tonecell"><div class="toneword">à</div><div class="tonelabel">Low</div><div class="tonepitch">do</div></div>
<div class="tonecell"><div class="toneword">a</div><div class="tonelabel">Mid, no mark</div><div class="tonepitch">re</div></div>
<div class="tonecell"><div class="toneword">á</div><div class="tonelabel">High</div><div class="tonepitch">mi</div></div>
</div>
<div class="lesson">
<p><b>Where tone appears.</b> Tone is not just carried by vowels. It also appears on the syllabic nasal consonants <b>m</b> and <b>n</b> when they form their own syllable. So watch vowels <i>and</i> these nasal syllables.</p>
<p><b>How tone changes meaning.</b> Two words can be spelled with the same letters and mean entirely different things, because the tone marks are different. For example: <b>ọkọ</b> (husband), <b>ọkọ̀</b> (vehicle) &mdash; same letters, different tone, different word.</p>
<p><b>Minimal pairs.</b> A pair of words like that, identical except for one tone (or one vowel-quality dot), is called a <b>minimal pair</b>. That's exactly what you're about to practise spotting.</p>
</div>
<button class="btn" onclick="startStage(1)">Start Level 1 →</button>
<button class="btn ghost" onclick="checkLevel()">← Back</button>`;
}

// ---------- Levels ----------
function startStage(n){
const items = n===1 ? G1 : G2;
const seenSet = n===1 ? seenG1 : seenG2;
const pairs = buildPairs(items);
let unseenPairs = pairs.filter(p=>!seenSet.has(pairKey(p[0])));
if(unseenPairs.length===0){ seenSet.clear(); unseenPairs=pairs; }
const roundPairs = sample(unseenPairs, Math.min(ROUND, unseenPairs.length));
stage = roundPairs.map(group=>{
seenSet.add(pairKey(group[0]));
return group[Math.random()*group.length|0];
});
si=0; points=0; correctCount=0; missed=[]; redoMode=false;
stage.forEach(q=>{q._answered=false;q._picked=null;});
playItem(n);
}

function playItem(stageNum){
const q=stage[si], N=stage.length;
const label = stageNum===1 ? "LEVEL 1 · GUESS THE TONE" : "LEVEL 2 · GUESS THE TONE";
function card(opt){
let c="card";
if(q._answered){
c+=" lock";
if(opt.form===q.correct) c+=" good";
else if(opt.form===q._picked) c+=" bad";
}
return `<div class="${c}" data-f="${opt.form}"><div class="word">${opt.form}</div><div class="tonetag">${opt.tone}</div></div>`;
}
let feed="";
if(q._answered){
const ok=q._picked===q.correct;
feed=`<div class="feed ${ok?'good':'bad'}">${ok?'\u2713 Correct. ':'\u2717 Not quite. The answer is <b>'+q.correct+'</b>. '}${q.explanation}</div>`;
}
const pic = q.picture ? `<div class="promptpic">${q.picture}</div>` : "";
const nav = `<div class="row">
<button class="btn ghost" onclick="prevItem(${stageNum})">← Previous</button>
<button class="btn ghost" onclick="nextItem(${stageNum})" ${q._answered?'':'disabled'}>${(si===N-1)?'Continue':'Next'} →</button>
</div>`;
app().innerHTML=`
<div class="meta"><span>${label} &middot; ${si+1} of ${N}</span></div>
<div class="bar"><i style="width:${(si+1)/N*100}%"></i></div>
<div class="promptcard">
${pic}
<div class="promptbare">${q.bare}</div>
<div class="promptgloss">${q.gloss}</div>
<div class="promptclass">${q.class}</div>
</div>
<div class="opts">${q.options.map(card).join("")}</div>
${feed}
${nav}`;
if(!q._answered){
app().querySelectorAll(".card").forEach(c=>c.onclick=()=>{
q._answered=true; q._picked=c.dataset.f;
if(c.dataset.f===q.correct){ points+=PTS; correctCount++; } else { missed.push(q); }
playItem(stageNum);
});
}
}

function prevItem(stageNum){
if(si>0){
si--;
playItem(stageNum);
} else if(stageNum===2){
stage=G1; si=G1.length-1;
playItem(1);
} else {
introTones();
}
}

function nextItem(stageNum){
si++;
if(si>=stage.length){
if(redoMode){ redoComplete(stageNum); }
else if(stageNum===1){ level1Complete(); }
else { level2Complete(); }
} else {
playItem(stageNum);
}
}

function redoMissed(stageNum){
if(missed.length===0) return;
stage=[...missed];
missed=[];
si=0; correctCount=0; points=0; redoMode=true;
stage.forEach(q=>{q._answered=false;q._picked=null;});
playItem(stageNum);
}

function redoComplete(stageNum){
const total=stage.length;
const nextLabel = stageNum===1 ? "Level 2 →" : "Level 3 →";
const nextFn = stageNum===1 ? "startStage(2)" : "doneOnboarding()";
const redoBtn = missed.length>0
? `<button class="btn ghost" onclick="redoMissed(${stageNum})">↺ Redo missed (${missed.length})</button>`
: "";
app().innerHTML=`
<div class="h2">Redo results</div>
<div class="promptcard">${correctCount} / ${total} correct this time.</div>
<button class="btn" onclick="${nextFn}">${nextLabel}</button>
${redoBtn}`;
}

function level1Complete(){
const pct=Math.round(100*correctCount/stage.length);
const redoBtn = missed.length>0
? `<button class="btn ghost" onclick="redoMissed(1)">↺ Redo missed (${missed.length})</button>`
: "";
app().innerHTML=`
<div class="h2">Level 1 complete</div>
<div class="promptcard">${correctCount} / ${stage.length} correct
<br><span class="muted">${levelMessage(pct)}</span></div>
<button class="btn" onclick="startStage(2)">Level 2 →</button>
${redoBtn}
<button class="btn ghost" onclick="prevItem(1)">← Previous</button>`;
}

function level2Complete(){
const pct=Math.round(100*correctCount/stage.length);
const redoBtn = missed.length>0
? `<button class="btn ghost" onclick="redoMissed(2)">↺ Redo missed (${missed.length})</button>`
: "";
app().innerHTML=`
<div class="h2">Level 2 complete</div>
<div class="promptcard">${correctCount} / ${stage.length} correct
<br><span class="muted">${levelMessage(pct)}</span></div>
<button class="btn" onclick="doneOnboarding()">Level 3 →</button>
${redoBtn}
<div class="row">
<button class="btn ghost" onclick="playItem(2)">← Previous</button>
<button class="btn ghost" onclick="titlePage()">↺ Restart</button>
</div>`;
}

function doneOnboarding(){
app().innerHTML=`<div class="h2">Level 3: Àmì</div>
<div class="lesson">This is where the full game begins.</div>
<button class="btn ghost" onclick="titlePage()">↺ Back to start</button>`;
}

window.checkLevel=checkLevel; window.introTones=introTones; window.startStage=startStage;
window.nextItem=nextItem; window.prevItem=prevItem; window.doneOnboarding=doneOnboarding;
window.titlePage=titlePage; window.level1Complete=level1Complete; window.level2Complete=level2Complete;
window.redoMissed=redoMissed; window.redoComplete=redoComplete;
titlePage();
</script></body></html>'''

html = (GAME_HTML
        .replace("__NAME__", GAME_NAME)
        .replace("__PTS__", str(POINTS_CORRECT))
        .replace("__ROUND__", str(ROUND_SIZE))
        .replace("__G1__", json.dumps(GUESS1_MONO, ensure_ascii=False))
        .replace("__G2__", json.dumps(GUESS2_BI, ensure_ascii=False)))

components.html(html, height=900, scrolling=True)
