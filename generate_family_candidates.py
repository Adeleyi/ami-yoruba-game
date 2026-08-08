#!/usr/bin/env python3
"""
Generate CANDIDATE Yorùbá word families from the afri-dict dictionary
(taresco/afri-dict) for native-speaker review.

This is the "assisted dataset expansion" step, and it is HUMAN-IN-THE-LOOP:
the script only DRAFTS candidates by grouping dictionary words that share the
same toneless/subdotless skeleton and differ in tone or vowel quality. A native
speaker MUST review `candidate_families.json` before anything is merged into
`families.json`. The script never edits families.json itself.

Data source (either works):
  * default: fetches rows over the internet from the HuggingFace datasets-server
    (uses only the Python standard library — no pip installs).
  * --csv PATH: reads a local CSV with columns  word,pos,definition
    (download it from https://huggingface.co/datasets/taresco/afri-dict).

Usage:
  python3 generate_family_candidates.py                 # fetch online
  python3 generate_family_candidates.py --csv afri.csv  # from a local CSV
"""
import json, unicodedata, re, sys, csv, urllib.request

# strip tone marks (grave/acute) AND the subdot, matching families.json keys
def bare(s):
    d = unicodedata.normalize("NFD", s)
    return "".join(c for c in d if c not in "̣̀́").lower()

def short_gloss(defn, n=60):
    g = re.split(r"[;\n]", defn.strip())[0].strip()
    return (g[:n].rstrip() + "…") if len(g) > n else g

def fetch_online():
    base = ("https://datasets-server.huggingface.co/rows"
            "?dataset=taresco/afri-dict&config=yor&split=train&offset={o}&length=100")
    rows, off = [], 0
    while True:
        with urllib.request.urlopen(base.format(o=off), timeout=30) as r:
            batch = json.load(r).get("rows", [])
        if not batch:
            break
        for item in batch:
            row = item["row"]
            rows.append((row.get("word", ""), row.get("pos", ""), row.get("definition", "")))
        off += len(batch)
        print(f"  fetched {off} rows…", file=sys.stderr)
        if len(batch) < 100:
            break
    return rows

def read_csv(path):
    with open(path, encoding="utf-8") as fh:
        return [(r.get("word", ""), r.get("pos", ""), r.get("definition", ""))
                for r in csv.DictReader(fh)]

def build(rows):
    try:
        existing = {f["key"] for f in json.load(open("families.json", encoding="utf-8"))}
    except Exception:
        existing = set()

    groups = {}
    for word, pos, defn in rows:
        w = word.strip()
        if not w or " " in w or not defn.strip():   # skip phrases / variant forms / empties
            continue
        key = bare(w)
        if not key.isalpha():                        # skip anything with hyphens, digits, etc.
            continue
        groups.setdefault(key, {})
        groups[key].setdefault(w, short_gloss(defn))

    candidates = []
    for key, members in sorted(groups.items()):
        if len(members) < 2:                         # a family needs a contrast
            continue
        candidates.append({
            "key": key,
            "review": True,
            "source": "afri-dict",
            "new": key not in existing,
            "syllables": len(re.findall(r"[aeiou]", key)),
            "members": [{"word": w, "meaning": g} for w, g in sorted(members.items())],
        })
    return candidates

def main():
    csvpath = sys.argv[sys.argv.index("--csv") + 1] if "--csv" in sys.argv else None
    rows = read_csv(csvpath) if csvpath else fetch_online()
    print(f"loaded {len(rows)} dictionary entries")
    candidates = build(rows)
    new = sum(1 for c in candidates if c["new"])
    json.dump(candidates, open("candidate_families.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print(f"candidate families: {len(candidates)} total, {new} not already in families.json")
    print("wrote candidate_families.json  — REVIEW with a native speaker before merging.")

if __name__ == "__main__":
    main()
