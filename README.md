# pe-vi

Bản dịch tiếng Việt của [Project Euler](https://projecteuler.net) -- 994 bài toán toán học và lập trình.

Trang web: https://tamnd.github.io/pe-vi

## Về dự án

Project Euler là một chuỗi bài toán toán học và lập trình máy tính đầy thử thách. Trang này dịch đề bài sang tiếng Việt để người đọc dễ tiếp cận hơn. Mỗi bài giữ nguyên phần tiếng Anh gốc bên cạnh bản dịch.

## Cấu trúc

```
source/_posts/      # 994 bài toán (Hexo post files)
scripts/
  translate.py      # công cụ quản lý bản dịch
  data/
    en/             # đề bài tiếng Anh
    vi/             # bản dịch tiếng Việt
    zh_CN/          # bản dịch tiếng Trung (tham khảo)
```

## Chạy local

Cần Node.js >= 16 và [uv](https://github.com/astral-sh/uv).

```bash
npm install
npx hexo server
```

Mở trình duyệt tại http://localhost:4000/pe-vi/

## Quản lý bản dịch

```bash
# kiểm tra trạng thái
uv run scripts/translate.py status

# áp dụng bản dịch vào source/_posts/
uv run scripts/translate.py apply

# xem song ngữ
uv run scripts/translate.py export --start 1 --end 10
```

Xem thêm tại [scripts/README.md](scripts/README.md).

## Giấy phép

Nội dung bài toán thuộc về [Project Euler](https://projecteuler.net). Bản dịch tiếng Việt theo giấy phép [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).
