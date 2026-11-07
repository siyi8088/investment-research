import os
import re
import sys

def audit_markdown_file(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    errors = []

    # 1. Check for raw LaTeX math $
    lines = text.split("\n")
    for idx, line in enumerate(lines, 1):
        unescaped_dollars = [m.start() for m in re.finditer(r"(?<!\\)\$", line)]
        if len(unescaped_dollars) >= 2:
            errors.append(f"Line {idx}: potential LaTeX math pair in line: {line.strip()[:60]}")

    # 2. Check blockquotes length (< 300 characters each)
    blockquotes = re.findall(r"(?:^>.*$\n?)+", text, re.M)
    for i, bq in enumerate(blockquotes):
        clean_bq = re.sub(r"^>\s*", "", bq, flags=re.M).strip()
        if len(clean_bq) > 300:
            errors.append(f"Blockquote {i+1} length {len(clean_bq)} exceeds WeChat limit of 300 chars")

    # 3. Check for mdnice bold delimiter collisions (across ALL lines, including tables!)
    ascii_punct = set("!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")
    white_space = set(" \t\n\r\u00a0")

    for idx, line in enumerate(lines, 1):
        for m in re.finditer(r"\*\*([^*]+)\*\*", line):
            inner = m.group(1)
            start, end = m.start(), m.end()
            prev_ch = line[start - 1] if start > 0 else " "
            next_ch = line[end] if end < len(line) else " "

            first_inner = inner[0]
            last_inner = inner[-1]

            # A. Leading comparison / approx symbol inside bold (军规 2)
            if re.match(r"^\s*[≥≤<>≈~]", inner):
                errors.append(
                    f"Line {idx}: Comparison/approx symbol inside bold '**{inner}**' (move ≥/≤/</>/≈/~ outside **)"
                )

            # B. mdnice left-flanking check: if inner starts with ASCII punct, prev_ch must be whitespace or ASCII punct
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

            # C. mdnice right-flanking check: if inner ends with ASCII punct (e.g. %, )), next_ch must be whitespace or ASCII punct (like <br>)
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

            # D. Outer punctuation collision check (brackets, colons, periods, semicolons touching **)
            if prev_ch in "（(":
                errors.append(
                    f"Line {idx}: Left bracket touching bold at {prev_ch!r}'**{inner}**' (add a space after bracket)"
                )
            if next_ch in "（）():：。；":
                errors.append(
                    f"Line {idx}: Bold touching outer punctuation at '**{inner}**'{next_ch!r} (add a space after **)"
                )

    # 4. Check for ASCII tree box characters
    ascii_boxes = re.findall(r"[┌─│└├┬┴┼]", text)
    if ascii_boxes:
        errors.append(f"Found {len(ascii_boxes)} ASCII box characters")

    # 5. Table unit cleanup check:
    for idx, line in enumerate(lines, 1):
        if line.strip().startswith("|") and not line.strip().startswith("| :"):
            if re.search(r"\|\s*\$[0-9]", line):
                errors.append(f"Line {idx}: Table data cell contains '$': {line.strip()[:60]}")

    # 6. Check for unnecessary specific day-level timestamps
    for idx, line in enumerate(lines, 1):
        if re.search(r"今天是\s*\*{0,2}[0-9]{4}\s*年", line):
            errors.append(f"Line {idx}: Unnecessary specific day timestamp found: '{line.strip()[:60]}'. Use evergreen reporting phrasing instead.")

    # 7. Check core indicators presence in Section 一:
    indicators = re.findall(r"^### 指标\s*[0-9]+", text, re.M)
    if len(indicators) == 0:
        errors.append("Missing '### 指标 N' sections in Chapter 1")

    # 8. Check WeChat Summary (> **摘要：**) presence and <= 120 char limit
    m_summary = re.search(r"^>\s*\*\*摘要：\*\*\s*(.+)$", text, re.M)
    if not m_summary:
        errors.append("Missing '> **摘要：** ...' block in the header section")
    else:
        summary_text = m_summary.group(1).strip()
        if len(summary_text) > 120:
            errors.append(
                f"WeChat summary length {len(summary_text)} exceeds 120 chars limit: '{summary_text[:40]}...'"
            )

    # 9. Check Standard Chapter H2 Skeleton (Chapters 一 to 六)
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
    targets = sys.argv[1:] if len(sys.argv) > 1 else ["10_无晶圆厂芯片设计与算力平台_NVDA与AMD.md"]
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    all_ok = True
    for target in targets:
        if not os.path.isabs(target):
            target = os.path.join(base_dir, target)
        if not audit_markdown_file(target):
            all_ok = False
    if not all_ok:
        sys.exit(1)
