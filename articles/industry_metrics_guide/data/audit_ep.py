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

    if re.match(r"^\s*#{1,4}\s+", line_no_code) and dollars:
        errors.append(
            f"Line {idx}: Heading (#..####) must not contain '$...$' math: {line_no_code.strip()[:70]}"
        )

    stripped = line_no_code.strip()
    if stripped.startswith("|") and not re.match(r"^\|[\s:|-]+\|?$", stripped):
        cells = stripped.strip("|").split("|")
        for col_i, cell in enumerate(cells, 1):
            cell_dollars = UNESCAPED_DOLLAR_RE.findall(cell)
            if len(cell_dollars) % 2 != 0:
                errors.append(
                    f"Line {idx} Col {col_i}: Odd '$' count inside table cell (unclosed formula or bare currency '$'): {cell.strip()[:50]}"
                )

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


def audit_markdown_file(file_path: str) -> bool:
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

    # 1. Line-by-line format checks ($/LaTeX, bold delimiters, ASCII boxes, timestamps)
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
                errors.append(f"Line {idx}: Found {len(ascii_boxes)} ASCII box characters")
            continue

        unquoted = re.sub(r"^[>\s]+", "", stripped)
        if unquoted.startswith("$$"):
            if unquoted == "$$" or not unquoted.endswith("$$") or len(unquoted) == 2:
                in_display_math = not in_display_math
            continue
        if in_display_math:
            continue

        outside_code_lines.append(line)

        line_no_code = _mask_inline_code(line)
        line_masked = _check_dollar_and_math_line(idx, line_no_code, errors)

        ascii_boxes_line = re.findall(r"[┌─│└├┬┴┼]", line_no_code)
        if ascii_boxes_line:
            errors.append(f"Line {idx}: Found {len(ascii_boxes_line)} ASCII box characters")

        if re.search(r"\*\*<sup\b", line_no_code):
            errors.append(f"Line {idx}: '**' directly touching '<sup>' without a separating space")

        for m in re.finditer(r"\*\*([^*]+)\*\*", line_no_code):
            inner_raw = m.group(1)
            if "MONEYCODE" in inner_raw or UNESCAPED_DOLLAR_RE.search(inner_raw):
                errors.append(
                    f"Line {idx}: Bold '**...**' must not wrap '$' prices or '$...$' math: '**{inner_raw}**'"
                )

        for m in re.finditer(r"\*\*([^*]+)\*\*", line_masked):
            inner = m.group(1)
            start, end = m.start(), m.end()
            prev_ch = line_masked[start - 1] if start > 0 else " "
            next_ch = line_masked[end] if end < len(line_masked) else " "

            first_inner = inner[0]
            last_inner = inner[-1]

            if re.match(r"^\s*[≥≤<>≈~]", inner):
                errors.append(
                    f"Line {idx}: Comparison/approx symbol inside bold '**{inner}**' (move ≥/≤/</>/≈/~ outside **)"
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

        # Table unit cleanup check (bare $ outside code/math)
        if stripped.startswith("|") and not stripped.startswith("| :"):
            if re.search(r"\|\s*\$[0-9]", line_masked):
                errors.append(f"Line {idx}: Table data cell contains bare '$': {stripped[:60]}")

        # Check for unnecessary specific day-level timestamps
        if re.search(r"今天是\s*\*{0,2}[0-9]{4}\s*年", line):
            errors.append(
                f"Line {idx}: Unnecessary specific day timestamp found: '{stripped[:60]}'. Use evergreen reporting phrasing instead."
            )

    # 2. Check blockquotes length (< 300 characters each)
    text_outside_code = "\n".join(outside_code_lines)
    blockquotes = re.findall(r"(?:^>.*$\n?)+", text_outside_code, re.M)
    for i, bq in enumerate(blockquotes):
        clean_bq = re.sub(r"^>\s*", "", bq, flags=re.M).strip()
        rendered_bq = re.sub(r"</?sup[^>]*>|\*\*|`|\\text\{([^}]*)\}|\$", r"\1", clean_bq)
        if len(rendered_bq) > 300:
            errors.append(
                f"Blockquote {i+1} length {len(rendered_bq)} exceeds WeChat limit of 300 chars"
            )

    # 3. Column-specific structural checks for industry_metrics_guide
    is_capstone = os.path.basename(file_path).startswith("20_")

    if not is_capstone:
        indicators = re.findall(r"^### 指标\s*[0-9]+", text, re.M)
        if len(indicators) == 0:
            errors.append("Missing '### 指标 N' sections in Chapter 1")

    m_summary = re.search(r"^>\s*\*\*摘要：\*\*\s*(.+)$", text, re.M)
    if not m_summary:
        errors.append("Missing '> **摘要：** ...' block in the header section")
    else:
        summary_text = m_summary.group(1).strip()
        if len(summary_text) > 120:
            errors.append(
                f"WeChat summary length {len(summary_text)} exceeds 120 chars limit: '{summary_text[:40]}...'"
            )

    if is_capstone:
        for ch_idx, cn_num in enumerate(["一", "二", "三", "四", "五"], 1):
            if not re.search(rf"^## {cn_num}、\s*", text, re.M):
                errors.append(f"Capstone Part {ch_idx} missing (expected '## {cn_num}、 ...')")
    else:
        ch1 = re.search(r"^## 一、\s*.*核心指标深度解剖", text, re.M)
        ch2 = re.search(r"^## 二、\s*.*(核心特异性指标全景速查对照表|核心指标全景速查对照表)", text, re.M)
        ch3 = re.search(r"^## 三、\s*标杆实例深度实战：", text, re.M)
        ch4 = re.search(r"^## 四、\s*标杆实例镜像对照：", text, re.M)
        ch5 = re.search(r"^## 五、\s*实战对账自查表：", text, re.M)
        ch6 = re.search(r"^## 六、\s*本讲买方总结与下讲预告", text, re.M)

        if not ch1:
            errors.append("Chapter 1 missing or incorrectly formatted (expected '## 一、 ...核心指标深度解剖')")
        if not ch2:
            errors.append("Chapter 2 missing or incorrectly formatted (expected '## 二、 ...核心特异性指标全景速查对照表')")
        if not ch3:
            errors.append("Chapter 3 missing or incorrectly formatted (expected '## 三、 标杆实例深度实战：...')")
        if not ch4:
            errors.append("Chapter 4 missing or incorrectly formatted (expected '## 四、 标杆实例镜像对照：...')")
        if not ch5:
            errors.append("Chapter 5 missing or incorrectly formatted (expected '## 五、 实战对账自查表：...')")
        if not ch6:
            errors.append("Chapter 6 missing or incorrectly formatted (expected '## 六、 本讲买方总结与下讲预告')")

    if not errors:
        print(f"✅ {os.path.basename(file_path)}: 100% Passed all audits!")
        return True
    else:
        print(f"❌ {os.path.basename(file_path)}: Found {len(errors)} issues:")
        for err in errors:
            print(f"  - {err}")
        return False


if __name__ == "__main__":
    targets = sys.argv[1:] if len(sys.argv) > 1 else ["16_电力与公用事业_NEE与VST.md"]
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    all_ok = True
    for target in targets:
        if not os.path.exists(target):
            target = os.path.join(base_dir, target)
        if not audit_markdown_file(target):
            all_ok = False
    if not all_ok:
        sys.exit(1)
