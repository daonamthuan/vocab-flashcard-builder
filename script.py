"""Export base-vocab.json to CSV files that can be imported into Anki.

Each vocabulary set (one array element) gets its own folder:
    output/<set name>/<set name>.csv
"""
import json, csv, os, re

# ====== Settings ======
NOTE_NEWLINE = "<br>"   # replaces line breaks in notes. Use "\n" to keep them
ADD_HEADER = False      # write a header row; keep False for Anki import
# ======================

HEADER = ["en", "ipa", "pos", "vi",
          "formula", "colloc", "note"]

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(ROOT, "output")

with open(os.path.join(ROOT, "base-vocab.json"), encoding="utf-8") as f:
    sets = json.load(f)
with open(os.path.join(ROOT, "ipa.json"), encoding="utf-8") as f:
    IPA = json.load(f)


def safe_name(name):
    """Make a valid Windows folder/file name: replace reserved characters, strip trailing dots/spaces."""
    name = re.sub(r'[<>:"/\\|?*]', "_", name).strip().rstrip(". ")
    return name or "untitled"


def get_ipa(en, pos):
    k = en.strip()
    ipa = (IPA.get(f"{k}|{pos}") or IPA.get(k) or "").strip()
    if ipa and not ipa.startswith("/"):
        ipa = f"/{ipa}/"
    return ipa


def fmt_note(s):
    s = (s or "").strip()
    while "\n\n\n" in s:
        s = s.replace("\n\n\n", "\n\n")
    return s.replace("\n", NOTE_NEWLINE)


os.makedirs(OUT_DIR, exist_ok=True)
missing_all = []
used_names = set()

for item in sets:
    name = safe_name(item.get("name") or f"set_week_{item.get('week', 'x')}")
    # avoid folder clashes caused by letter case or replaced characters
    base, n = name, 2
    while name.lower() in used_names:
        name = f"{base} ({n})"
        n += 1
    used_names.add(name.lower())

    seen, rows = set(), []
    for w in item["words"]:
        key = (w["en"].lower(), w["pos"])
        if key in seen:
            continue
        seen.add(key)

        ipa = get_ipa(w["en"], w["pos"])
        if not ipa:
            missing_all.append(f'{name}: {w["en"]}')

        rows.append([
            w["en"],
            ipa,
            w["pos"],              # keep the original tag: n, v, adj, adv, prep...
            w.get("vi", ""),
            w.get("formula", ""),
            w.get("colloc", ""),
            fmt_note(w.get("note", "")),
        ])

    set_dir = os.path.join(OUT_DIR, name)
    os.makedirs(set_dir, exist_ok=True)
    path = os.path.join(set_dir, f"{name}.csv")
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        wr = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        if ADD_HEADER:
            wr.writerow(HEADER)
        wr.writerows(rows)
    print(f"{name}: {len(rows)} words -> {path}")

if missing_all:
    print("\nMissing IPA:", ", ".join(missing_all))
