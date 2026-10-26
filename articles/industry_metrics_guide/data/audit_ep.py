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

    # 3. Check for bold delimiter collisions
    for idx, line in enumerate(lines, 1):
        if line.strip().startswith("|"):
            continue # table cells may have specific syntax
        m_colon = re.findall(r"\*\*[^*]+\*\*[:：]", line)
        if m_colon:
            errors.append(f"Line {idx}: Bold touching colon outside: {m_colon}")
        m_period = re.findall(r"\*\*[^*]+\*\*。", line)
        if m_period:
            errors.append(f"Line {idx}: Bold touching period: {m_period}")
        m_bracket = re.findall(r"\*\*[^*]+\*\*[(（]", line)
        if m_bracket:
            errors.append(f"Line {idx}: Bold touching bracket: {m_bracket}")
        m_bracket_left = re.findall(r"[(（]\*\*[^*]+\*\*", line)
        if m_bracket_left:
            errors.append(f"Line {idx}: Bracket touching bold on left: {m_bracket_left}")

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

    # 7. Check 5-part anatomical skeleton for Section 一 core indicators:
    indicators = re.findall(r"^### 指标\s*[0-9]+", text, re.M)
    num_indicators = len(indicators)
    part1_defs = re.findall(r"^#### 1\.\s*深度定义与经济内涵", text, re.M)
    part2_formulas = re.findall(r"^#### 2\.\s*精确计算公式", text, re.M)
    rules_of_thumb = re.findall(r"^#### 3\.\s*买方实战判读法则", text, re.M)
    filing_guides = re.findall(r"\*\*10-K 定点检索指南：\*\*", text)
    misconceptions = re.findall(r"\*\*买方常见认知误区：\*\*", text)

    if num_indicators > 0:
        if len(part1_defs) < num_indicators:
            errors.append(f"Missing '#### 1. 深度定义与经济内涵': found {len(part1_defs)} of {num_indicators} indicators")
        if len(part2_formulas) < num_indicators:
            errors.append(f"Missing '#### 2. 精确计算公式': found {len(part2_formulas)} of {num_indicators} indicators")
        if len(rules_of_thumb) < num_indicators:
            errors.append(f"Missing '#### 3. 买方实战判读法则': found {len(rules_of_thumb)} of {num_indicators} indicators")
        if len(filing_guides) < num_indicators:
            errors.append(f"Missing '**10-K 定点检索指南：**': found {len(filing_guides)} of {num_indicators} indicators")
        if len(misconceptions) < num_indicators:
            errors.append(f"Missing '**买方常见认知误区：**': found {len(misconceptions)} of {num_indicators} indicators")

    # 8. Check Standard Chapter H2 Skeleton (Chapters 一 to 六)
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
    target = sys.argv[1] if len(sys.argv) > 1 else "10_无晶圆厂芯片设计与算力平台_NVDA与AMD.md"
    if not os.path.isabs(target):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        target = os.path.join(base_dir, target)
    audit_markdown_file(target)
