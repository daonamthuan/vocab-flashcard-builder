# vocab-flashcards

Bộ công cụ tạo flashcard từ vựng IELTS dưới dạng file CSV để import vào [Anki](https://apps.ankiweb.net/).

- `script.py` xuất từng bộ từ vựng trong `base-vocab.json` thành `output/<tên bộ>/<tên bộ>.csv`, mỗi bộ một thư mục con.
- Skill Claude Code `ielts-vocab-csv` tạo bộ từ vựng từ ảnh chụp một bài tập Reading/Listening, chỉ lấy các từ được bôi vàng.

Phiên âm dùng **IPA Anh–Anh** (British, RP), lấy từ `ipa.json`.

## Cấu trúc

```
.
├── script.py                 # base-vocab.json -> output/<tên bộ>/<tên bộ>.csv
├── base-vocab.json           # mảng các bộ từ vựng (name, words...)
├── ipa.json                  # từ điển phiên âm IPA Anh–Anh ("từ" hoặc "từ|pos" -> "/ipa/")
├── .claude/skills/ielts-vocab-csv/
│   ├── SKILL.md              # quy tắc tạo bộ từ vựng từ bài tập
│   └── scripts/build_csv.py  # JSON -> CSV đúng định dạng
└── output/                   # mỗi bộ một thư mục con, không đưa lên git
    └── <tên bộ>/<tên bộ>.csv
```

## Định dạng CSV

UTF-8 có BOM, không có dòng tiêu đề, 7 cột:

| Cột | Ý nghĩa |
|---|---|
| `en` | Từ / cụm từ (dạng gốc) |
| `ipa` | Phiên âm IPA Anh–Anh |
| `pos` | Loại từ: `n`, `v`, `adj`, `adv`, `phr v`, `idiom`... |
| `vi` | Nghĩa tiếng Việt. Nếu nghĩa trong bài khác nghĩa thông thường: `{nghĩa trong bài}, {các nghĩa thường dùng}` |
| `formula` | Cấu trúc ngữ pháp (`pay off`, `stash sth (away)`) |
| `colloc` | Collocation thông dụng |
| `note` | Giải thích + ví dụ, xuống dòng bằng `<br>` |

## Sử dụng

Yêu cầu Python 3.8+ (không cần thư viện ngoài).

### Xuất bộ từ theo tuần

```bash
python script.py
```

### Tạo bộ từ vựng từ một bài tập (Claude Code)

Mở thư mục này bằng Claude Code, gửi ảnh chụp bài tập có các từ bôi vàng và gõ:

```
/ielts-vocab-csv
```

Skill sẽ viết dữ liệu ra JSON rồi gọi:

```bash
python .claude/skills/ielts-vocab-csv/scripts/build_csv.py <input.json> "output/<Tên bộ>/<Tên bộ>.csv"
```

Script tự điền IPA từ `ipa.json` khi ô `ipa` để trống, chuẩn hoá `/.../`, đổi xuống dòng thành `<br>` và bỏ dòng trùng.

### Import vào Anki

**File → Import**, chọn file CSV, chọn dấu phân tách *Comma*, bật *Allow HTML in fields*, rồi gán 7 cột vào các field của note type.
