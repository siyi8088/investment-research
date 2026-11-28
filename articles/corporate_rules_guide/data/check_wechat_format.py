import os
import re
import sys

CODE_SPAN_RE = re.compile(r"``[^`]*``|`[^`]*`")
UNESCAPED_DOLLAR_RE = re.compile(r"(?<!\\)\$")
CURRENCY_WORDS_RE = re.compile(r"[亿万]|美元|人民币")


def _mask_inline_code(line: str) -> str:
    """Replace inline code spans with neutral placeholders preserving $ detection rules."""
    def repl(match: re.Match) -> str:
        span = match.group(0)
        return "MONEYCODE" if UNESCAPED_DOLLAR_RE.search(span) else "CODE"

    return CODE_SPAN_RE.sub(repl, line)


def _check_dollar_and_math_line(idx: int, line_no_code: str, errors: list[str]) -> str:
    """Validate universal $ / LaTeX rules on a non-display-math line and return line with $...$ masked."""
    dollars = [m.start() for m in UNESCAPED_DOLLAR_RE.finditer(line_no_code)]
    if len(dollars) % 2 != 0:
        errors.append(
            f"Line {idx}: Odd count ({len(dollars)}) of unescaped '$' outside inline code: {line_no_code.strip()[:70]}"
        )
        return line_no_code

    # Check headings for any math $
    if re.match(r"^\s*#{1,4}\s+", line_no_code) and dollars:
        errors.append(
            f"Line {idx}: Heading (#..####) must not contain '$...$' math: {line_no_code.strip()[:70]}"
        )

    # Check table cell boundaries so a missing $ in cell A doesn't pair with cell B
    stripped = line_no_code.strip()
    if stripped.startswith("|") and not re.match(r"^\|[\s:|-]+\|?$", stripped):
        cells = stripped.strip("|").split("|")
        for col_i, cell in enumerate(cells, 1):
            cell_dollars = UNESCAPED_DOLLAR_RE.findall(cell)
            if len(cell_dollars) % 2 != 0:
                errors.append(
                    f"Line {idx} Col {col_i}: Odd '$' count inside table cell (unclosed formula or bare currency '$'): {cell.strip()[:50]}"
                )

    # Validate each $...$ pair and mask it for downstream bold delimiter checks
    parts = []
    last_end = 0
    for i in range(0, len(dollars), 2):
        s, e = dollars[i], dollars[i + 1]
        inner = line_no_code[s + 1 : e]
        if inner.startswith(" ") or inner.endswith(" "):
            errors.append(
                f"Line {idx}: Leading/trailing whitespace inside '$...$' (${inner}$)"
            )
        if inner and CURRENCY_WORDS_RE.search(inner) and "\\text" not in inner:
            errors.append(
                f"Line {idx}: Currency words inside bare '$...$' (${inner}$) — use pure Chinese units"
            )
        prev_two = line_no_code[max(0, s - 2) : s]
        next_two = line_no_code[e + 1 : e + 3]
        if prev_two == "**" or next_two == "**":
            errors.append(
                f"Line {idx}: '**' directly abutting '$...$' (${inner}$) — add a space"
            )
        parts.append(line_no_code[last_end:s])
        parts.append("MATH")
        last_end = e + 1
    parts.append(line_no_code[last_end:])
    return "".join(parts)


def check_markdown_file(file_path: str) -> bool:
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    errors = []
    lines = text.split("\n")

    ascii_punct = set("!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")
    white_space = set(" \t\n\r\u00a0")

    in_fence = False
    in_display_math = False
    outside_code_lines = []

    for idx, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("```"):
            if not in_fence and "```mermaid" in stripped.lower():
                errors.append(f"Line {idx}: Found forbidden ```mermaid block (unsupported by WeChat)")
            in_fence = not in_fence
            continue
        if in_fence:
            ascii_boxes = re.findall(r"[┌─│└├┬┴┼]", line)
            if ascii_boxes:
                errors.append(f"Line {idx}: Found {len(ascii_boxes)} ASCII box characters inside code block")
            continue

        # Handle standalone $$ display math blocks (including indented or quote-prefixed $$)
        unquoted = re.sub(r"^[>\s]+", "", stripped)
        if unquoted.startswith("$$"):
            if unquoted == "$$" or not unquoted.endswith("$$") or len(unquoted) == 2:
                in_display_math = not in_display_math
            continue
        if in_display_math:
            continue

        outside_code_lines.append(line)

        # Mask inline code spans (`...`) and validate $ / LaTeX math rules
        line_no_code = _mask_inline_code(line)
        line_masked = _check_dollar_and_math_line(idx, line_no_code, errors)

        # Check **<sup without separating space
        if re.search(r"\*\*<sup\b", line_no_code):
            errors.append(f"Line {idx}: '**' directly touching '<sup>' without a separating space")

        # Check bold wrapping $ quotes (MONEYCODE) or math ($)
        for m in re.finditer(r"\*\*([^*]+)\*\*", line_no_code):
            inner_raw = m.group(1)
            if "MONEYCODE" in inner_raw or UNESCAPED_DOLLAR_RE.search(inner_raw):
                errors.append(
                    f"Line {idx}: Bold '**...**' must not wrap '$' prices or '$...$' math: '**{inner_raw}**'"
                )

        # Check mdnice bold delimiter collisions on masked line (no * from code or math)
        for m in re.finditer(r"\*\*([^*]+)\*\*", line_masked):
            inner = m.group(1)
            start, end = m.start(), m.end()
            prev_ch = line_masked[start - 1] if start > 0 else " "
            next_ch = line_masked[end] if end < len(line_masked) else " "

            first_inner = inner[0]
            last_inner = inner[-1]

            if re.match(r"^\s*[≥≤<>≈~]", inner):
                errors.append(
                    f"Line {idx}: Comparison/approx symbol inside bold '**{inner}**' (move outside **)"
                )

            open_prev_white = prev_ch in white_space
            open_next_white = first_inner in white_space
            open_prev_punct = prev_ch in ascii_punct
            open_next_punct = first_inner in ascii_punct
            can_open = (not open_next_white) and (
                (not open_next_punct) or open_prev_white or open_prev_punct
            )
            if not can_open:
                errors.append(
                    f"Line {idx}: mdnice CANNOT OPEN bold at {prev_ch!r}'**{inner}**' (add a space before **)"
                )

            close_prev_white = last_inner in white_space
            close_next_white = next_ch in white_space
            close_prev_punct = last_inner in ascii_punct
            close_next_punct = next_ch in ascii_punct
            can_close = (not close_prev_white) and (
                (not close_prev_punct) or close_next_white or close_next_punct
            )
            if not can_close:
                errors.append(
                    f"Line {idx}: mdnice CANNOT CLOSE bold at '**{inner}**'{next_ch!r} (add a space after **)"
                )

            if prev_ch in "（(":
                errors.append(
                    f"Line {idx}: Left bracket touching bold at {prev_ch!r}'**{inner}**' (add a space after bracket)"
                )
            if next_ch in "（）():：。；":
                errors.append(
                    f"Line {idx}: Bold touching outer punctuation at '**{inner}**'{next_ch!r} (add a space after **)"
                )

        # Check for ASCII box characters on regular lines too
        ascii_boxes_line = re.findall(r"[┌─│└├┬┴┼]", line_no_code)
        if ascii_boxes_line:
            errors.append(f"Line {idx}: Found {len(ascii_boxes_line)} ASCII box characters")

        # Table cell sanity check (no bare $ in table cells outside math/inline code)
        if stripped.startswith("|") and not stripped.startswith("| :"):
            if re.search(r"\|\s*\$[0-9]", line_masked):
                errors.append(f"Line {idx}: Table data cell contains bare '$': {stripped[:60]}")

    # Check blockquotes length (<= 300 characters each for WeChat limit)
    text_outside_code = "\n".join(outside_code_lines)
    blockquotes = re.findall(r"(?:^>.*$\n?)+", text_outside_code, re.M)
    for i, bq in enumerate(blockquotes):
        clean_bq = re.sub(r"^>\s*", "", bq, flags=re.M).strip()
        rendered_bq = re.sub(r"</?sup[^>]*>|\*\*|`|\\text\{([^}]*)\}|\$", r"\1", clean_bq)
        if len(rendered_bq) > 300:
            errors.append(
                f"Blockquote {i+1} length {len(rendered_bq)} exceeds WeChat limit of 300 chars"
            )

    if not errors:
        print(f"✅ {os.path.basename(file_path)}: 100% Passed all WeChat/mdnice formatting checks!")
        return True
    else:
        print(f"❌ {os.path.basename(file_path)}: Found {len(errors)} issues:")
        for err in errors:
            print(f"  - {err}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 check_wechat_format.py <markdown_file> [...]")
        sys.exit(1)

    all_ok = True
    for target in sys.argv[1:]:
        if not os.path.exists(target):
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            target = os.path.join(base_dir, target)
        if not check_markdown_file(target):
            all_ok = False
    sys.exit(0 if all_ok else 1)
