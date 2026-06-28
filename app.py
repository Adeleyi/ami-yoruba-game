"""
Àmì — Yorùbá tone learning game.

This Streamlit app serves the game as a single self-contained page.
The whole game (the arrangement, the cards, the lessons) lives in the HTML
below; Streamlit hosts it and gives it a public web address.

To change the game name, edit GAME_NAME.
The questions and word families are read from the two JSON files, so to add or
edit content you only touch questions.json and families.json.
"""

import json
import streamlit as st
import streamlit.components.v1 as components

# ---- settings you can edit -------------------------------------------------
GAME_NAME = "Àmì"        # the title shown on the home screen
ROUND_SIZE = 10           # questions per round
POINTS_CORRECT = 10       # points per correct answer
HINTS_PER_ROUND = 3       # hints allowed per round
# ---------------------------------------------------------------------------

st.set_page_config(page_title=GAME_NAME, page_icon="🎵", layout="centered")

# hide Streamlit's own chrome so only the game shows
st.markdown("""
<style>
#MainMenu, header, footer {visibility:hidden;}
.block-container{padding:0 !important; max-width:720px !important;}
[data-testid="stAppViewContainer"]{background:#faf7f2;}
</style>
""", unsafe_allow_html=True)

QUESTIONS = json.load(open("questions.json", encoding="utf-8"))
FAMILIES = json.load(open("families.json", encoding="utf-8"))

GAME_HTML = r'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>AMI</title>
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
.home{text-align:center;margin:3rem 0 1.6rem;}
.title{color:var(--indigo);font-weight:800;font-size:4.2rem;line-height:1;letter-spacing:-1px;margin:0;}
.marks{font-size:2.8rem;letter-spacing:.65rem;color:var(--indigo);margin:.5rem 0 0;}
.marks b{color:var(--gold);}
.h2{color:var(--indigo);font-weight:800;font-size:1.7rem;margin:.2rem 0 .7rem;}
.lead{color:#555;margin:0 0 8px;}
.meta{display:flex;justify-content:space-between;color:#6b7280;font-size:.85rem;margin:14px 0 6px;}
.bar{height:6px;background:#eadfce;border-radius:6px;overflow:hidden;margin-bottom:14px;}
.bar>i{display:block;height:100%;background:var(--gold);transition:width .3s;}
.sentence{background:#fff;border:1px solid #ece5d8;border-left:5px solid var(--gold);
border-radius:10px;padding:18px 20px;font-size:1.5rem;margin:.2rem 0;}
.hint{color:#6b7280;font-size:1.02rem;margin:8px 2px 16px;}
.opts{display:grid;grid-template-columns:1fr 1fr;gap:12px;}
.card{background:#fff;border:2px solid #e6ded0;border-radius:12px;padding:18px 14px;text-align:center;cursor:pointer;transition:.15s;}
.card:hover{border-color:var(--indigo);}
.card.good{border-color:var(--good);background:#eaf5ef;}
.card.bad{border-color:var(--bad);background:#fbeef0;}
.card.lock{cursor:default;}
.word{font-size:2rem;font-weight:800;color:var(--indigo);}
.mean{color:#6b7280;font-size:.92rem;margin-top:4px;min-height:1.1em;}
.hintnote{color:#6b7280;font-size:.9rem;margin-top:10px;}
.feed{margin-top:16px;padding:14px 16px;border-radius:10px;font-size:1.02rem;}
.feed.good{background:#eaf5ef;border-left:5px solid var(--good);color:#1c5a40;}
.feed.bad{background:#fbeef0;border-left:5px solid var(--bad);color:#7c2531;}
.fcard{background:#fff;border:1px solid #ece5d8;border-radius:10px;padding:12px 16px;margin-bottom:10px;}
.fam{font-weight:800;color:var(--gold);font-size:1.15rem;}
.muted{color:#6b7280;}
.lesson{background:#fff;border:1px solid #ece5d8;border-radius:10px;padding:6px 20px;line-height:1.6;}
.lesson li{margin:6px 0;}
</style></head><body><div class="wrap"><div id="app"></div></div>
<script>
const QUESTIONS=__Q__, FAMILIES=__F__;
const NAME="__NAME__", ROUND=__ROUND__, PTS=__PTS__, HINTS=__HINTS__;
const MSG={
perfect:["Perfect round. You read every tone correctly. You are a champion.","Flawless, ten out of ten. Your ear for tone is excellent.","A clean sweep. Every single answer was right."],
strong:["Very strong. Just a little more for a perfect score.","Excellent work. You missed only a few.","Almost perfect. Your tone reading is sharp."],
middle:["Good work. You are getting the hang of the tones.","Solid round. Keep practising and the score will climb.","Nicely done. A few more rounds will sharpen it."],
low:["You are getting there. Try another round.","A fair start. Visit Learn, then play again.","Keep going. Each round will make the tones clearer."],
vlow:["Do not worry, tones take practice. Visit Learn, then try again.","Tone is tricky at first. Spend a moment in Learn and come back.","A tough round. The Learn section will help, then give it another go."]};
let seen=new Set(), rd=[], i=0, points=0, streak=0, hintsLeft=HINTS;
const app=()=>document.getElementById("app");
const pickOne=a=>a[Math.random()*a.length|0];
function shuffle(a){for(let k=a.length-1;k>0;k--){const j=Math.random()*(k+1)|0;[a[k],a[j]]=[a[j],a[k]];}return a;}
function sample(a,n){return shuffle([...a]).slice(0,n);}

function newRound(){let un=QUESTIONS.filter(q=>!seen.has(q.id));
if(un.length<ROUND){seen=new Set();un=[...QUESTIONS];}
rd=sample(un,ROUND);
rd.forEach(q=>{seen.add(q.id);q._sides=Math.random()<.5?["A","B"]:["B","A"];
q._answered=false;q._picked=null;q._hint=false;});
i=0;points=0;streak=0;hintsLeft=HINTS;play();}

function play(){const q=rd[i],N=rd.length,sides=q._sides;
const show=q._hint||q._answered, allAns=rd.every(x=>x._answered);
function card(s){const o=q[s];let c="card";
if(q._answered){c+=" lock";if(s===q.correct)c+=" good";else if(s===q._picked)c+=" bad";}
return `<div class="${c}" data-s="${s}"><div class="word">${o.word}</div><div class="mean">${show?o.meaning:""}</div></div>`;}
let feed="",hintArea="";
if(q._answered){const ok=q._picked===q.correct;
feed=`<div class="feed ${ok?'good':'bad'}">${ok?'\u2713 Correct. ':'\u2717 Not quite. The answer is <b>'+q[q.correct].word+'</b>. '}${q.explanation}</div>`;}
else if(q._hint){hintArea=`<div class="hintnote">Hints left: ${hintsLeft}</div>`;}
else{hintArea=`<button class="btn ghost" onclick="useHint()" ${hintsLeft===0?'disabled':''}>${hintsLeft===0?'No hints left':'Hint'} (${hintsLeft} left)</button>`;}
const nav=`<div class="row">
<button class="btn ghost" onclick="prev()" ${i===0?'disabled':''}>\u2190 Previous</button>
<button class="btn ghost" onclick="next()" ${i===N-1?'disabled':''}>Next \u2192</button></div>`;
const finish=allAns?`<button class="btn gold" onclick="results()">See your score</button>`:"";
app().innerHTML=`
<div class="meta"><span>Question ${i+1} of ${N} \u00b7 ${points} pts${streak?' \u00b7 streak '+streak:''}</span>
<a href="#" onclick="home();return false" class="muted">Quit</a></div>
<div class="bar"><i style="width:${(i+1)/N*100}%"></i></div>
<div class="sentence">${q.sentence}</div><div class="hint">\uD83D\uDCAC ${q.translation}</div>
<div class="opts">${card(sides[0])}${card(sides[1])}</div>${feed}${hintArea}${nav}${finish}`;
if(!q._answered){app().querySelectorAll(".card").forEach(c=>c.onclick=()=>choose(c.dataset.s));}}

function choose(s){const q=rd[i];if(q._answered)return;q._answered=true;q._picked=s;
if(s===q.correct){points+=PTS;streak++;}else{streak=0;}play();}
function useHint(){const q=rd[i];if(q._hint||q._answered||hintsLeft===0)return;q._hint=true;hintsLeft--;play();}
function prev(){if(i>0){i--;play();}}
function next(){if(i<rd.length-1){i++;play();}}

function results(){const correct=rd.filter(x=>x._answered&&x._picked===x.correct).length;
let b=correct===ROUND?"perfect":correct>=8?"strong":correct>=6?"middle":correct>=4?"low":"vlow";
app().innerHTML=`<div class="h2">Round complete</div>
<div class="sentence">You got <b>${correct} / ${ROUND}</b> correct &nbsp;\u00b7&nbsp; ${points} points
<br><span class="muted">${pickOne(MSG[b])}</span></div>
<button class="btn" onclick="newRound()">Play again</button>
<div class="row"><button class="btn ghost" onclick="learn()">Learn</button>
<button class="btn ghost" onclick="home()">Home</button></div>`;}

function home(){app().innerHTML=`
<div class="home"><div class="title">${NAME}</div><div class="marks">\u00e0 <b>a</b> \u00e1</div></div>
<button class="btn" onclick="newRound()">Play</button>
<div class="row"><button class="btn ghost" onclick="learn()">Learn</button>
<button class="btn ghost" onclick="howto()">How to play</button></div>`;}

function learn(){app().innerHTML=`<div class="h2">Learn</div>
<button class="btn" onclick="tonemarks()">Tone marks (the three tones)</button>
<button class="btn" onclick="vowel()">Vowel quality (the subdot)</button>
<button class="btn" onclick="families()">Word families</button>
<button class="btn ghost" onclick="home()">\u2190 Home</button>`;}

function tonemarks(){app().innerHTML=`<div class="h2">Tone marks, the three tones</div>
<div class="lesson">Yor\u00f9b\u00e1 has three tones. Think of them like the notes <b>do, re, mi</b>.
<ul><li><b>Low (do).</b> Written with a grave mark, like <b>\u00e0</b>. Example: <i>\u00ecs\u00e0l\u1EB9\u0300</i>.</li>
<li><b>Mid (re).</b> No mark at all, like <b>a</b>. The plain, middle voice.</li>
<li><b>High (mi).</b> Written with an acute mark, like <b>\u00e1</b>. Example: <i>\u00f2k\u00e8</i>.</li></ul>
Many words are spelled the same but mean different things. The tone mark tells them apart, in writing and in speech.</div>
<button class="btn ghost" onclick="learn()">\u2190 Back to Learn</button>`;}

function vowel(){app().innerHTML=`<div class="h2">Vowel quality, the subdot</div>
<div class="lesson">Some Yor\u00f9b\u00e1 letters carry a small dot underneath: <b>\u1EB9, \u1ECD, \u1E63</b>. This dot is called the <b>subdot</b>, and it changes the sound the letter makes.
<ul><li><b>e</b> and <b>\u1EB9</b> are different sounds. The <b>e</b> is closed, like the <i>ay</i> in <i>day</i>. The <b>\u1EB9</b> is more open, like the <i>e</i> in <i>bed</i>.</li>
<li><b>o</b> and <b>\u1ECD</b> differ too. The <b>o</b> is closed, like the <i>o</i> in <i>go</i>. The <b>\u1ECD</b> is more open, like the <i>aw</i> in <i>saw</i>.</li>
<li><b>s</b> and <b>\u1E63</b> differ as well. The <b>\u1E63</b> is the <i>sh</i> sound, as in <i>shoe</i>.</li></ul>
Because the subdot changes the sound, it can change a word\u2019s meaning, just like a tone mark. Some questions differ in both tone and vowel quality, and the feedback will say so.</div>
<button class="btn ghost" onclick="learn()">\u2190 Back to Learn</button>`;}

function families(){let cards=FAMILIES.map(f=>{
let rows=f.members.map(m=>`<div>\u2022 <b>${m.word}</b> <span class="muted">${m.meaning}</span></div>`).join("");
return `<div class="fcard"><div class="fam">${f.key}</div>${rows}</div>`;}).join("");
app().innerHTML=`<div class="h2">Word families</div>
<p class="lead">Words that share the same letters but change meaning with tone or vowel. Study these, then test yourself in Play.</p>
${cards}<button class="btn ghost" onclick="learn()">\u2190 Back to Learn</button>`;}

function howto(){app().innerHTML=`<div class="h2">How to play</div>
<div class="lesson"><ol><li>Read the Yor\u00f9b\u00e1 sentence and the English line under it.</li>
<li>Yor\u00f9b\u00e1 uses three tone marks: low (<b>\u00e0</b>), mid (<b>a</b>, no mark), high (<b>\u00e1</b>). They change what a word means.</li>
<li>Pick the word whose marks fit the sentence.</li>
<li>Stuck? Use a <b>Hint</b> to reveal the meanings. You get ${HINTS} hints each round.</li>
<li>Use <b>Previous</b> and <b>Next</b> to move around and review the explanations before you finish.</li></ol>
You score ${PTS} points per correct answer, and each round has ${ROUND} questions. New to tones? Open <b>Learn</b> first.</div>
<div class="row"><button class="btn" onclick="newRound()">Play now</button>
<button class="btn ghost" onclick="home()">\u2190 Home</button></div>`;}

window.home=home;window.learn=learn;window.tonemarks=tonemarks;window.vowel=vowel;
window.families=families;window.howto=howto;window.newRound=newRound;
window.next=next;window.prev=prev;window.choose=choose;window.useHint=useHint;window.results=results;
home();
</script></body></html>'''

html = (GAME_HTML
        .replace("__Q__", json.dumps(QUESTIONS, ensure_ascii=False))
        .replace("__F__", json.dumps(FAMILIES, ensure_ascii=False))
        .replace("__NAME__", GAME_NAME)
        .replace("__ROUND__", str(ROUND_SIZE))
        .replace("__PTS__", str(POINTS_CORRECT))
        .replace("__HINTS__", str(HINTS_PER_ROUND)))

components.html(html, height=900, scrolling=True)