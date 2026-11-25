---
name: ielts-vocab-csv
description: Tạo bộ từ vựng (file CSV kiểu Anki) từ một bài tập IELTS Reading/Listening mà người dùng gửi (ảnh chụp hoặc text), chỉ lấy các từ được bôi màu vàng/highlight. Dùng khi người dùng gửi ảnh bài đọc có từ highlight và muốn "tạo bộ từ vựng", "làm flashcard", "xuất csv từ vựng".
---

# IELTS Vocab CSV

Biến các từ được **bôi màu vàng** trong một bài tập (ảnh chụp màn hình bài đọc + câu hỏi) thành file CSV có cùng cấu trúc với các bộ trong `output/<tên bộ>/<tên bộ>.csv` (được `script.py` tạo từ `base-vocab.json`).

## Định dạng đầu ra (bắt buộc giống bộ mẫu)

- Mã hoá **UTF-8 có BOM** (`utf-8-sig`), **không có dòng tiêu đề**, phân tách bằng dấu phẩy, quote kiểu tối thiểu (QUOTE_MINIMAL).
- 7 cột theo thứ tự: `en, ipa, pos, vi, formula, colloc, note`
- Xuống dòng trong `note` thay bằng `<br>` (đoạn mới = `<br><br>`).

| Cột | Nội dung |
|---|---|
| `en` | Dạng gốc (lemma) của từ: `pays off` → `pay off`, `falling` → `fall`, `supers` → `super`. Giữ dạng bài đọc nếu dạng đó là một tính từ có nghĩa riêng (`uncapped`, `adapted`). |
| `ipa` | Phiên âm IPA giọng **Anh–Anh (British, RP)**, có dấu `/.../`, ví dụ `crop /krɒp/`, `narrow /ˈnærəʊ/`, `particular /pəˈtɪkjələ/` (không đọc /r/ cuối âm tiết, dùng /əʊ/, /ɒ/), thống nhất với `ipa.json` của dự án. Ưu tiên tra `ipa.json` (khóa `từ|pos` hoặc `từ`), nếu không có thì tự viết theo giọng Anh–Anh. Nếu trong `note` có nhắc phát âm thì cũng dùng IPA Anh–Anh. |
| `pos` | Ký hiệu ngắn như bộ mẫu: `n`, `v`, `adj`, `adv`, `prep`, `phr v`, `idiom`, `prep phrase`, `determiner`. Dùng loại từ **theo đúng ngữ cảnh trong bài**. |
| `vi` | Nghĩa tiếng Việt (xem quy tắc nghĩa bên dưới). |
| `formula` | Cấu trúc ngữ pháp nếu có: `pay off`, `catch on (with sb)`, `stash sth (away)`. Để trống nếu không có. |
| `colloc` | 2–4 collocation thông dụng, cách nhau bởi `, `. |
| `note` | Giải thích + ví dụ (xem quy tắc note). |

## Quy tắc nghĩa (`vi`)

1. Nếu nghĩa trong bài **giống** nghĩa thông thường → ghi nghĩa thông thường như bộ mẫu, ví dụ `"cổ đại, cổ xưa"`.
2. Nếu nghĩa trong bài **khác** nghĩa thường gặp (nghĩa chuyên ngành, nghĩa ít gặp, phrasal verb nhiều nghĩa…) → ghi theo dạng
   `"{nghĩa trong bài tập}, {các nghĩa thường dùng khác...}"`
   tức là nghĩa trong bài **luôn đứng đầu**, sau đó mới tới các nghĩa phổ biến. Ví dụ `comb` trong bài nuôi ong: `"sáp tổ ong (honeycomb), cái lược, chải (tóc)"`.

## Quy tắc note

Viết bằng tiếng Việt, giọng văn giống bộ mẫu ("Ví dụ khi bạn nói là: ... - ..."). Mỗi note gồm:

1. Định nghĩa ngắn: `từ (pos): ...`
2. **Ví dụ trong bài tập**: trích câu (hoặc vế câu) chứa từ đó trong bài, kèm dịch nghĩa. Mở đầu bằng `Trong bài:`.
3. Nếu nghĩa trong bài khác nghĩa thông thường: giải thích nghĩa thông thường và **thêm ví dụ cho từng nghĩa thông thường** (đánh số `1.`, `2.`…), mỗi ví dụ có câu tiếng Anh và bản dịch.
4. Nếu nghĩa giống nghĩa thông thường: vẫn thêm 1–2 ví dụ khác ngoài bài.
5. Tuỳ chọn: lưu ý phát âm, từ cùng họ, mẹo nhớ, cách dùng trong IELTS Writing/Speaking.

## Quy trình

1. Đọc kỹ tất cả ảnh, liệt kê **mọi** từ/cụm được highlight vàng (cả ở bài đọc lẫn phần câu hỏi). Không lấy từ không được highlight.
2. Gộp trùng (cùng lemma + cùng pos, ví dụ `supers` xuất hiện 2 lần → 1 dòng).
3. Với mỗi từ, xác định nghĩa trong ngữ cảnh và so với nghĩa thông thường để áp dụng quy tắc nghĩa.
4. Ghi dữ liệu ra file JSON (mảng các object có đủ 7 khóa ở trên; `note` dùng `\n` để xuống dòng) trong scratchpad.
5. Đặt tên bộ theo tên bài, viết hoa chữ đầu như các bộ trong `base-vocab.json` (ví dụ `Migratory Beekeeping`). Tên không chứa `<>:"/\|?*`.
6. Chạy script để tạo CSV đúng định dạng, mỗi bộ nằm trong thư mục riêng:
   ```
   python .claude/skills/ielts-vocab-csv/scripts/build_csv.py <input.json> "output/<Tên bộ>/<Tên bộ>.csv"
   ```
   Ví dụ: `output/Migratory Beekeeping/Migratory Beekeeping.csv`. Script tự tạo thư mục, tự điền IPA từ `ipa.json` nếu ô `ipa` để trống, chuẩn hoá `/.../`, đổi `\n` → `<br>`, loại dòng trùng và báo những từ còn thiếu IPA (khi đó tự bổ sung IPA Anh–Anh vào JSON rồi chạy lại).
7. Báo lại cho người dùng: đường dẫn thư mục bộ, số từ, danh sách từ, những từ được ghi theo dạng "nghĩa trong bài, nghĩa thường dùng".
