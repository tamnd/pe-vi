# scripts/

Translation tools for pe-vi.

## translate.py

Manages Vietnamese translations for all 994 Project Euler problems.

Translation data lives in markdown files under `scripts/data/`:

- `data/en/` -- English problem statements (extracted from source posts)
- `data/vi/` -- Vietnamese translations
- `data/zh_CN/` -- Chinese translations (reference, problems 301-994)

Each folder contains files named `NNNN-NNNN.md` with the format:

```markdown
## Problem N: Title
Body text...
```

### Run with uv

```sh
# Show translation progress
uv run scripts/translate.py status

# Apply all available VI translations (dry-run first)
uv run scripts/translate.py apply --dry-run --verbose
uv run scripts/translate.py apply

# Apply a range
uv run scripts/translate.py apply --start 1 --end 100

# Extract EN content from source files in data format
uv run scripts/translate.py extract --start 129 --end 200

# Show bilingual export
uv run scripts/translate.py export --start 1 --end 10
```

### Adding translations

Edit the appropriate `data/vi/NNNN-NNNN.md` file directly:

```markdown
## Problem N: Tiêu đề tiếng Việt
Nội dung tiếng Việt...
```

Then run `apply` to push changes into `source/_posts/`.

### Glossary

| EN | VI |
|----|----|
| prime | số nguyên tố |
| divisor / factor | ước số / thừa số |
| multiple | bội số |
| factorial | giai thừa |
| permutation | hoán vị |
| combination | tổ hợp |
| palindrome | số đối xứng |
| Fibonacci sequence | dãy Fibonacci |
| square number | số chính phương |
| triangular number | số tam giác |
| pentagonal number | số ngũ giác |
| amicable number | số thân thiện |
| totient | hàm Euler Totient / hàm phi |
| radical | căn số |
| pandigital | toàn chữ số |
| continued fraction | phân số liên tiếp |
| convergent | hội tụ (phân số) |
| modulo | modulo (giữ nguyên) |
