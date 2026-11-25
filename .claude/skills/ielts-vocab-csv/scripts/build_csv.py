"""Build an Anki-style vocab CSV (same format as output/trunk_tuan_*.csv).

Usage: python build_csv.py <input.json> <output.csv> [--ipa path/to/ipa.json] [--header]

input.json: list of objects with keys en, ipa, pos, vi, formula, colloc, note.
IPA is British English (RP). Empty ipa cells are filled from ipa.json
(British) in the current directory, or from the file given with --ipa.
"""
import csv
import json
import os
import sys

HEADER = ["en", "ipa", "pos", "vi", "formula", "colloc", "note"]
NOTE_NEWLINE = "<br>"


def load_ipa(path):
    if path and os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return {}


def norm_ipa(ipa):
    ipa = (ipa or "").strip()
    if ipa and not ipa.startswith("/"):
        ipa = "/" + ipa.strip("/") + "/"
    return ipa


def fmt_note(s):
    s = (s or "").strip().replace("\r\n", "\n")
    while "\n\n\n" in s:
        s = s.replace("\n\n\n", "\n\n")
    return s.replace("\n", NOTE_NEWLINE)


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    if len(args) < 2:
        sys.exit(__doc__)
    src, dst = args[0], args[1]
    ipa_path = "ipa.json"
    if "--ipa" in argv:
        ipa_path = argv[argv.index("--ipa") + 1]
    ipa_db = load_ipa(ipa_path)

    with open(src, encoding="utf-8") as f:
        words = json.load(f)

    seen, rows, missing = set(), [], []
    for w in words:
        en, pos = w["en"].strip(), w.get("pos", "").strip()
        key = (en.lower(), pos)
        if key in seen:
            continue
        seen.add(key)
        ipa = w.get("ipa") or ipa_db.get(f"{en}|{pos}") or ipa_db.get(en) or ""
        ipa = norm_ipa(ipa)
        if not ipa:
            missing.append(en)
        rows.append([en, ipa, pos, w.get("vi", "").strip(), w.get("formula", "").strip(),
                     w.get("colloc", "").strip(), fmt_note(w.get("note", ""))])

    os.makedirs(os.path.dirname(os.path.abspath(dst)), exist_ok=True)
    with open(dst, "w", encoding="utf-8-sig", newline="") as f:
        wr = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        if "--header" in argv:
            wr.writerow(HEADER)
        wr.writerows(rows)
    print(f"{len(rows)} words -> {dst}")
    if missing:
        print("Missing IPA:", ", ".join(missing))


if __name__ == "__main__":
    main(sys.argv[1:])
