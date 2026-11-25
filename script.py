"""Xuất base-vocab.json thành CSV để import vào Anki.

Mỗi bộ từ vựng (phần tử trong mảng) có một thư mục riêng:
    output/<tên bộ>/<tên bộ>.csv
"""
import json, csv, os, re

# ====== Cấu hình ======
NOTE_NEWLINE = "<br>"   # thay xuống dòng trong ghi chú. Đặt "\n" nếu muốn giữ nguyên
ADD_HEADER = False      # ghi dòng tiêu đề; để False khi import vào Anki
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
    """Tên thư mục/file hợp lệ trên Windows: bỏ ký tự cấm, bỏ dấu chấm/khoảng trắng cuối."""
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
    name = safe_name(item.get("name") or f"trunk_tuan_{item.get('week', 'x')}")
    # tránh trùng tên thư mục do khác biệt hoa/thường hoặc ký tự bị thay thế
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
            w["pos"],              # giữ nguyên ký hiệu gốc: n, v, adj, adv, prep...
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
    print(f"{name}: {len(rows)} từ -> {path}")

if missing_all:
    print("\nChưa có phiên âm:", ", ".join(missing_all))
