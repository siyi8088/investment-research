#!/usr/bin/env python3
"""
Institutional Buy-Side Investment Memo PDF Exporter
Converts Markdown memos into publication-quality executive PDF reports
using Pandoc, inlined Base64 graphics, and Headless Google Chrome with CSS Paged Media.
"""

import sys
import os
import re
import base64
import argparse
import subprocess
import shutil

CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

CSS_TEMPLATE = """
@page {
    size: A4;
    margin: 20mm 16mm 18mm 16mm;
    @top-left {
        content: "机构买方投研备忘录 · 深度估值与压力测试";
        font-size: 8.5pt;
        color: #94a3b8;
        font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Segoe UI", sans-serif;
        border-bottom: 0.5px solid #e2e8f0;
        padding-bottom: 4px;
    }
    @top-right {
        content: "__TICKER__ · 投资决策与风控自查";
        font-size: 8.5pt;
        color: #94a3b8;
        font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Segoe UI", sans-serif;
        border-bottom: 0.5px solid #e2e8f0;
        padding-bottom: 4px;
    }
    @bottom-center {
        content: "第 " counter(page) " 页 / 共 " counter(pages) " 页";
        font-size: 8.5pt;
        color: #94a3b8;
        font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Segoe UI", sans-serif;
    }
}

@page:first {
    @top-left { content: none; }
    @top-right { content: none; }
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "Segoe UI", Roboto, "Helvetica Neue", "Microsoft YaHei", sans-serif;
    color: #1e293b;
    line-height: 1.62;
    font-size: 10pt;
    margin: 0;
    padding: 0;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
}

h1 {
    font-size: 19pt;
    font-weight: 700;
    color: #0f172a;
    border-bottom: 2.5px solid #2563eb;
    padding-bottom: 8px;
    margin-top: 0;
    margin-bottom: 14px;
    letter-spacing: -0.3px;
}

h2 {
    font-size: 13.5pt;
    font-weight: 650;
    color: #1e3a8a;
    border-bottom: 1px solid #cbd5e1;
    padding-bottom: 5px;
    margin-top: 22px;
    margin-bottom: 10px;
    page-break-after: avoid;
    break-after: avoid;
}

h3 {
    font-size: 11.5pt;
    font-weight: 600;
    color: #334155;
    margin-top: 16px;
    margin-bottom: 8px;
    page-break-after: avoid;
    break-after: avoid;
}

p {
    margin-top: 0;
    margin-bottom: 9px;
    text-align: justify;
}

blockquote {
    margin: 10px 0 14px 0;
    padding: 10px 14px;
    background: #f8fafc;
    border-left: 3.5px solid #3b82f6;
    color: #334155;
    font-size: 9.5pt;
    border-radius: 0 4px 4px 0;
    page-break-inside: avoid;
    break-inside: avoid;
}

blockquote p {
    margin: 3px 0;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0 16px 0;
    font-size: 8.8pt;
    page-break-inside: auto;
}

thead {
    display: table-header-group;
}

tr {
    page-break-inside: avoid;
    break-inside: avoid;
}

th {
    background-color: #f1f5f9;
    color: #0f172a;
    font-weight: 600;
    text-align: left;
    padding: 7px 9px;
    border: 1px solid #cbd5e1;
}

td {
    padding: 6px 9px;
    border: 1px solid #e2e8f0;
    vertical-align: top;
    line-height: 1.45;
}

tr:nth-child(even) td {
    background-color: #f8fafc;
}

pre {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    padding: 9px 12px;
    font-family: "SF Mono", Menlo, Monaco, Consolas, monospace;
    font-size: 8.2pt;
    line-height: 1.42;
    overflow-x: hidden;
    page-break-inside: avoid;
    break-inside: avoid;
    white-space: pre-wrap;
    word-break: break-all;
}

code {
    font-family: "SF Mono", Menlo, Monaco, Consolas, monospace;
    font-size: 8.8pt;
    background: #f1f5f9;
    padding: 1.5px 3.5px;
    border-radius: 3px;
    color: #0f172a;
}

pre code {
    background: none;
    padding: 0;
    color: inherit;
}

hr {
    border: 0;
    height: 1px;
    background: #e2e8f0;
    margin: 16px 0;
}

ul, ol {
    margin-top: 0;
    margin-bottom: 9px;
    padding-left: 20px;
}

li {
    margin-bottom: 3.5px;
}

img {
    max-width: 480px;
    height: auto;
    display: block;
    margin: 12px auto;
    page-break-inside: avoid;
    break-inside: avoid;
}

.radar-wrap {
    page-break-inside: avoid;
    break-inside: avoid;
    text-align: center;
    margin: 14px 0;
}
"""

def export_memo_to_pdf(input_md_path, output_pdf_path=None, ticker=None):
    input_md_path = os.path.abspath(input_md_path)
    if not os.path.exists(input_md_path):
        raise FileNotFoundError(f"Input file not found: {input_md_path}")
    
    memo_dir = os.path.dirname(input_md_path)
    
    if not output_pdf_path:
        base_name = os.path.splitext(os.path.basename(input_md_path))[0]
        output_pdf_path = os.path.join(memo_dir, f"{base_name}.pdf")
    output_pdf_path = os.path.abspath(output_pdf_path)

    if not ticker:
        # Try to infer ticker from path: .../companies/<TICKER>/...
        match = re.search(r"/companies/([^/]+)/", input_md_path)
        if match:
            ticker = match.group(1)
        else:
            ticker = "EQUITY RESEARCH"

    print(f"[*] Processing: {input_md_path}")
    print(f"[*] Target PDF: {output_pdf_path}")
    print(f"[*] Ticker ID : {ticker}")

    with open(input_md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    # Find and inline relative image references: src="xxx.png" or ![alt](xxx.png)
    def inline_img_src(match):
        orig_attr = match.group(0)
        img_name = match.group(1)
        if img_name.startswith("data:") or img_name.startswith("http"):
            return orig_attr
        img_full_path = os.path.join(memo_dir, img_name)
        if os.path.exists(img_full_path):
            with open(img_full_path, "rb") as img_f:
                b64_data = base64.b64encode(img_f.read()).decode("utf-8")
            ext = os.path.splitext(img_name)[1].lower().replace(".", "")
            if ext == "jpg": ext = "jpeg"
            return f'src="data:image/{ext};base64,{b64_data}"'
        return orig_attr

    md_text = re.sub(r'src=["\']([^"\']+\.(?:png|jpg|jpeg|webp))["\']', inline_img_src, md_text)

    # Wrap images inside div for clean pagination
    md_text = re.sub(r'(<div align="center">[\s\S]*?<img [\s\S]*?</div>)', r'<div class="radar-wrap">\1</div>', md_text)

    temp_md = os.path.join("/tmp", f"memo_{ticker}_{os.getpid()}.md")
    temp_html = os.path.join("/tmp", f"memo_{ticker}_{os.getpid()}.html")

    try:
        with open(temp_md, "w", encoding="utf-8") as f:
            f.write(md_text)

        # Pandoc Markdown to HTML5
        pandoc_cmd = ["pandoc", temp_md, "-f", "markdown", "-t", "html5"]
        res = subprocess.run(pandoc_cmd, capture_output=True, text=True, check=True)
        body_html = res.stdout

        css = CSS_TEMPLATE.replace("__TICKER__", ticker)
        full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>{ticker} 买方投资备忘录</title>
<style>
{css}
</style>
</head>
<body>
{body_html}
</body>
</html>
"""
        with open(temp_html, "w", encoding="utf-8") as f:
            f.write(full_html)

        # Chrome headless print to PDF
        chrome_cmd = [
            CHROME_PATH,
            "--headless",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={output_pdf_path}",
            temp_html
        ]
        res = subprocess.run(chrome_cmd, capture_output=True, text=True)
        if not os.path.exists(output_pdf_path) or os.path.getsize(output_pdf_path) == 0:
            raise RuntimeError(f"Chrome PDF generation failed: {res.stderr}")

        size_kb = os.path.getsize(output_pdf_path) / 1024
        print(f"[✓] Success! PDF exported to: {output_pdf_path} ({size_kb:.1f} KB)")
        return output_pdf_path

    finally:
        if os.path.exists(temp_md): os.remove(temp_md)
        if os.path.exists(temp_html): os.remove(temp_html)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export Investment Memo to PDF")
    parser.add_argument("input", help="Path to markdown investment memo")
    parser.add_argument("-o", "--output", help="Output PDF file path", default=None)
    parser.add_argument("-t", "--ticker", help="Ticker symbol", default=None)
    args = parser.parse_args()

    export_memo_to_pdf(args.input, args.output, args.ticker)
