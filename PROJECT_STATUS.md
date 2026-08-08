# Àmì — Project Status & Roadmap

A snapshot of what the game does now and what is planned, for the project
document. Written to be pasted/adapted into the formal write-up.

_Last updated: 2026-08-08_

---

## 1. What the game is

**Àmì** is a browser game that teaches Yorùbá **tone** and **vowel quality**.
Learners read a prompt and choose the correctly-marked word; minimal pairs
(words that look identical but change meaning with tone/vowel) are used as the
main teaching device, but the goal is to teach tone/vowel quality on words in
general, not only pairs.

All content lives in two reviewed data files — `questions.json` (sentences) and
`families.json` (minimal-pair word families) — so linguists can add content
without touching code.

---

## 2. Implemented in this phase

- **Graded difficulty ladder** — Monosyllabic → Bisyllabic → Trisyllabic →
  Sentences → Mixed. Word levels are **generated automatically from the reviewed
  word families**, split by syllable count (62 monosyllabic + 39 bisyllabic
  items from current data). No fabricated content.
- **Word-level "guess the tone"** — a single word + its English meaning is shown;
  the learner picks the correctly-toned form. Distractors are the word's own
  family members, and the explanation is built automatically from the glosses.
- **Phrasal combination (tone sandhi) lesson** — teaches that a word can change
  tone when it joins another (e.g. a monosyllabic verb's low tone is suppressed
  before a noun object). Grounded in the linguistics literature and the game's
  own data (question S07). Questions may carry an optional `sandhi_note`.
- **Tone-shift rule verified** — the "verb loses low tone before a noun object"
  rule was checked against published Yorùbá tonology (see Sources) before use.
- **Dictionary lookup** — type a word *without* tone marks (e.g. "oko") to see
  every toned form and its meaning (husband / vehicle / farm / hoe / spear).
  Searches locally over the reviewed data; no server, no cost.
- **Word families inside a round** — consult a family without losing your place.
- **Progress retention** — coins, best score and rank persist in the browser
  (localStorage). Returning on the same device resumes automatically; no login.
- **Gamification** — a coin per correct answer and free starter coins. (A rank
  ladder was prototyped and then removed for now; see further work.)
- **Continue & resume** — rounds continue (2, 3, …) with the next level gently
  blended in, then graduate up; progress is saved so learners can **Resume** their
  level. A UX pass removed redundant labels/metrics and merged duplicate lessons.
- **Audio hook** — an optional `audio` field per item and a 🔊 button, ready for
  native recordings (hidden until recordings exist).
- **Static web app** — the game was extracted to a single `index.html` (+ the
  JSON files) that runs in any browser and deploys free on Vercel / Netlify /
  GitHub Pages. Streamlit (`app.py`) is retained as legacy.

## 3. Design decisions (and why)

- **No AI/model inside the running game** — a live model costs money per use. AI
  is used only at *build time* with a human reviewer, so the shipped game has
  zero runtime cost.
- **localStorage instead of accounts** — avoids running a server/database and
  storing personal data; accounts are deferred until cross-device sync is truly
  needed (then via a free Supabase/Firebase tier, not hand-built auth).
- **Web app, not native app** — one codebase, reaches every phone browser; can
  later become an installable PWA for an app-like feel, still free.
- **Content lives in reviewed JSON, not code** — so non-programmers can
  contribute and every item can be checked.

## 4. Further work (planned)

Priority order:

1. **Native-speaker review of all tone/vowel data** + Owolabi citations. The
   accuracy of the marks is the foundation of the whole project.
2. **Native audio recordings** — unlocks listening practice and self-comparison.
3. **Assisted dataset expansion** — draft candidate families from the afri-dict
   Yorùbá dictionary (12,200 entries, with diacritics) and candidate sentences
   from the lexicon, each **verified by a native speaker before inclusion**
   (human-in-the-loop). Drafting is done offline at build time (no runtime AI).
4. **Contributor workflow for non-technical reviewers** — a shared spreadsheet
   (word / tone / meaning / source / reviewed?) exported to JSON, so linguists
   review content without editing code.
5. **Difficulty as a learner curriculum** — a Beginner / Intermediate / Advanced
   tag mapping which exercise types belong to each stage.
6. **Record-and-compare pronunciation** — the learner records their voice and
   plays it beside the native recording (self-assessment; recordings stay on the
   device). Needs the reference audio first. No automatic tone scoring
   (unreliable and out of budget).
7. **Additional exercise types** beyond multiple choice — e.g. "mark the tone of
   each syllable" and "listen and identify" — so words *without* a minimal pair
   can also be taught.
8. **Accounts / cross-device progress** — free Supabase/Firebase tier, with
   unique usernames, only when the need is real.
9. **Ranks & richer gamification** — a Yorùbá rank ladder (names native-reviewed),
   badges, streak rewards. Prototyped once; deferred to keep the core focused.
10. **Audio in Learn & Dictionary** — 🔊 on lesson examples and dictionary results
    once native recordings exist.

Deferred / later: subscriptions & tokens, player ranks with cultural names,
Yorùbá songs & chants on success, cultural/history content, children's mode
(rhymes, folktales / àlọ́), Yorùbá tongue twisters.

## 5. Data quality & ethics notes

- Items carry a `source`/`review` flag; rank names and any generated content are
  flagged for native review before they count as final.
- **Voice recordings**: get the speaker's consent before publishing their voice;
  attribute contributors; choose a content licence (e.g. CC-BY) if sharing.
- **User data**: minimise it. Learner voice recordings (record-and-compare) stay
  on-device and are not uploaded. If accounts are added later, a privacy notice
  and consent are required (Nigeria NDPR / GDPR), especially for younger users.

## 6. Tech & deployment

- **Run locally:** `python3 -m http.server` then open `http://localhost:8000`.
- **Deploy (free):** push to GitHub, then GitHub Pages (deploy from branch,
  root) or import the repo into Vercel (framework: Other, no build step).
- **Files:** `index.html` (game), `questions.json`, `families.json`, optional
  `audio/` folder for recordings. `app.py` is the legacy Streamlit version.

## 7. Sources (tone-shift rule)

- Courtenay, *The assimilated low tone in Yoruba*.
- *On the left edge of Yorùbá complements* (verb low tone suppressed before an
  accusative complement).
- Akinlabi & Liberman, *The tonal phonology of Yoruba clitics*.
- **To cite in the write-up:** Owolabi, *Ìjìnlẹ̀ Ítúpẹ̀lẹ̀ Èdè Yorùbá* — for the
  authoritative statement and page number.
