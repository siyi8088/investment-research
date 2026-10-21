"""
SEC XBRL 数据台账生成器（industry_metrics_guide 专栏用）

用途：
  从 SEC EDGAR 官方 companyfacts 接口拉取 10-K 主表科目，生成带出处的数据台账，
  并与文章中引用的数字逐项比对，输出差异清单。

数据出处：
  https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json
  每一个数值都记录：XBRL 标签、报告期截止日、10-K 申报编号（accn）、申报日期。
  拿 accn 可以在 EDGAR 上直接定位到原始 10-K 文件。

局限（需人工补充，见 *_manual.md）：
  - 分部收入（如 Data Center、Networking）多为公司自定义维度，不在标准 us-gaap 字段里；
  - 部分公司表外采购承诺的口径（是否含长期供应与产能协议）需要对照 10-K 附注原文；
  - 20-F / 港股公司（TSMC、ASML、SMIC 等）不适用本脚本。

用法：
  python3 sec_ledger.py ep10
"""

import csv
import json
import os
import sys
import time
import urllib.request
from datetime import date

USER_AGENT = "investment-research personal-study contact@example.com"  # SEC 要求提供 UA
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(HERE, ".cache")
YI = 1e8  # 1 亿


# ---------------------------------------------------------------------------
# 科目定义：每个科目给出候选 XBRL 标签（按优先级），以及是期间数还是时点数
# ---------------------------------------------------------------------------
METRICS = {
    "revenue": {"name": "营业收入", "kind": "duration",
                "tags": ["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax"]},
    "cogs": {"name": "营业成本", "kind": "duration",
             "tags": ["CostOfRevenue", "CostOfGoodsAndServicesSold"]},
    "gross_profit": {"name": "毛利润", "kind": "duration", "tags": ["GrossProfit"]},
    "rnd": {"name": "研发费用", "kind": "duration", "tags": ["ResearchAndDevelopmentExpense"]},
    "net_income": {"name": "净利润", "kind": "duration", "tags": ["NetIncomeLoss"]},
    "cfo": {"name": "经营现金流", "kind": "duration",
            "tags": ["NetCashProvidedByUsedInOperatingActivities"]},
    "capex": {"name": "资本开支", "kind": "duration",
              "tags": ["PaymentsToAcquireProductiveAssets", "PaymentsToAcquirePropertyPlantAndEquipment"]},
    "inventory": {"name": "存货净额", "kind": "instant", "tags": ["InventoryNet"]},
    "inv_raw": {"name": "存货-原材料", "kind": "instant",
                "tags": ["InventoryRawMaterialsNetOfReserves", "InventoryRawMaterials"]},
    "inv_wip": {"name": "存货-在产品", "kind": "instant",
                "tags": ["InventoryWorkInProcessNetOfReserves", "InventoryWorkInProcess"]},
    "inv_fg": {"name": "存货-产成品", "kind": "instant",
               "tags": ["InventoryFinishedGoodsNetOfReserves", "InventoryFinishedGoods"]},
    "inv_writedown": {"name": "存货减值", "kind": "duration", "tags": ["InventoryWriteDown"]},
    "purchase_obligation": {"name": "采购承诺", "kind": "instant",
                            "tags": ["PurchaseObligation",
                                     "UnrecordedUnconditionalPurchaseObligationBalanceSheetAmount"]},
}

# ---------------------------------------------------------------------------
# 各讲配置：公司、CIK、年份，以及文章中引用的数字（单位：亿美元 / % / 天）
# ---------------------------------------------------------------------------
EPISODES = {
    "ep10": {
        "article": "10_无晶圆厂芯片设计与算力平台_NVDA与AMD.md",
        "companies": {
            "NVDA": {
                "cik": "0001045810",
                "years": [2022, 2023, 2024, 2025, 2026],  # 财年（FY 截止于次年 1 月底）
                "article": {
                    "revenue": [269.1, 269.7, 609.2, 1305.0, 2160.0],
                    "gross_margin_pct": [64.9, 56.9, 72.7, 75.0, 72.4],
                    "rnd": [52.7, 73.4, 86.8, 135.0, 190.0],
                    "rnd_pct": [19.6, 27.2, 14.2, 10.3, 8.8],
                    "inventory": [26.1, 51.6, 52.8, 95.0, 148.0],
                    "dio": [89, 142, 92, 85, 98],
                    "inv_writedown": [1.8, 21.7, 5.2, 6.5, 8.5],
                    "purchase_obligation": [90.0, 49.2, 161.0, 308.0, 440.0],
                    "net_income": [97.5, 43.7, 297.6, 728.8, 1210.5],
                    "cfo": [91.1, 56.4, 280.9, 641.2, 998.0],
                    "fcf": [81.3, 38.1, 270.2, 608.5, 925.0],
                },
            },
            "AMD": {
                "cik": "0000002488",
                "years": [2021, 2022, 2023, 2024, 2025],
                "article": {
                    "revenue": [164.3, 236.0, 226.8, 257.8, 346.4],
                    "gross_margin_pct": [48.2, 45.0, 46.0, 49.0, 50.0],
                    "rnd_pct": [17.3, 21.2, 25.9, 24.5, 22.0],
                    "dio": [84, 115, 138, 125, 110],
                    "purchase_obligation": [86.8, 85.9, 45.8, 49.6, 122.0],
                    "fcf": [32.0, 31.1, 11.2, 36.0, 58.0],
                },
            },
        },
    },
}

DERIVED_NAMES = {
    "gross_margin_pct": "毛利率(%)",
    "rnd_pct": "研发费用率(%)",
    "dio": "存货周转天数(天)",
    "fcf": "自由现金流",
}


# ---------------------------------------------------------------------------
def fetch_companyfacts(cik):
    os.makedirs(CACHE_DIR, exist_ok=True)
    path = os.path.join(CACHE_DIR, f"CIK{cik}.json")
    if not os.path.exists(path) or time.time() - os.path.getmtime(path) > 86400:
        url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=60) as r, open(path, "wb") as f:
            f.write(r.read())
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _days(a, b):
    return (date.fromisoformat(b) - date.fromisoformat(a)).days


def pick_annual(facts, metric, year):
    """返回 (value, tag, end, accn, filed, restated_flag) ；找不到返回 None。
    规则：只取 10-K；期间数要求约 52/53 周；报告期截止日所在年份 == year；
    优先取“该财年自己那份 10-K”的原始披露值，若后续 10-K 对同一期间给出不同数值则标记重述。"""
    gaap = facts["facts"]["us-gaap"]
    spec = METRICS[metric]
    for tag in spec["tags"]:
        if tag not in gaap or "USD" not in gaap[tag]["units"]:
            continue
        rows = []
        for x in gaap[tag]["units"]["USD"]:
            if x.get("form") != "10-K":
                continue
            if int(x["end"][:4]) != year:
                continue
            if spec["kind"] == "duration":
                if "start" not in x or not (357 <= _days(x["start"], x["end"]) <= 372):
                    continue
            rows.append(x)
        if not rows:
            continue
        rows.sort(key=lambda x: x["filed"])
        original = rows[0]
        restated = any(abs(r["val"] - original["val"]) > 0.5e6 for r in rows[1:])
        return original["val"], tag, original["end"], original["accn"], original["filed"], restated
    return None


def build_ledger(ep_key):
    ep = EPISODES[ep_key]
    ledger_rows, diff_rows = [], []

    for ticker, cfg in ep["companies"].items():
        facts = fetch_companyfacts(cfg["cik"])
        years = cfg["years"]
        raw = {m: {} for m in METRICS}

        # 需要前一年存货来算平均存货
        for m in METRICS:
            for y in [years[0] - 1] + years:
                r = pick_annual(facts, m, y)
                if r:
                    raw[m][y] = r

        for m in METRICS:
            for y in years:
                if y in raw[m]:
                    val, tag, end, accn, filed, restated = raw[m][y]
                    ledger_rows.append([ticker, y, METRICS[m]["name"], m, round(val / YI, 2),
                                        tag, end, accn, filed, "是" if restated else "",
                                        "✓ 10-K 原值"])

        # 派生指标
        derived = {}
        for i, y in enumerate(years):
            g = lambda m, yy=y: raw[m][yy][0] if yy in raw[m] else None
            rev, cogs, gp, rnd, cfo, capex = g("revenue"), g("cogs"), g("gross_profit"), g("rnd"), g("cfo"), g("capex")
            inv, inv_prev = g("inventory"), g("inventory", y - 1)
            if gp is None and rev is not None and cogs is not None:
                gp = rev - cogs
            if cogs is None and rev is not None and gp is not None:
                cogs = rev - gp
            d = {}
            if rev and gp is not None:
                d["gross_margin_pct"] = round(gp / rev * 100, 1)
            if rev and rnd is not None:
                d["rnd_pct"] = round(rnd / rev * 100, 1)
            if cogs and inv is not None and inv_prev is not None:
                d["dio"] = round((inv + inv_prev) / 2 / cogs * 365)
            if cfo is not None and capex is not None:
                d["fcf"] = round((cfo - capex) / YI, 2)
            derived[y] = d
            for k, v in d.items():
                formula = {"gross_margin_pct": "毛利润 ÷ 营收",
                           "rnd_pct": "研发 ÷ 营收",
                           "dio": "(期初+期末存货)/2 ÷ 营业成本 × 365",
                           "fcf": "经营现金流 − 资本开支"}[k]
                ledger_rows.append([ticker, y, DERIVED_NAMES[k], k, v, formula, "", "", "", "",
                                    "✓ 由 10-K 原值计算"])

        # 与文章比对
        for m, art_vals in cfg["article"].items():
            for y, a in zip(years, art_vals):
                if m in derived.get(y, {}):
                    s = derived[y][m]
                elif m in raw and y in raw[m]:
                    s = round(raw[m][y][0] / YI, 2)
                else:
                    s = None
                name = METRICS[m]["name"] if m in METRICS else DERIVED_NAMES[m]
                if s is None:
                    status, dev = "SEC 无标准字段，需人工核对", ""
                else:
                    if m in ("gross_margin_pct", "rnd_pct"):
                        dev_abs = a - s
                        ok = abs(dev_abs) <= 0.15
                        dev = f"{dev_abs:+.1f} pct"
                    elif m == "dio":
                        dev_abs = a - s
                        ok = abs(dev_abs) <= 3
                        dev = f"{dev_abs:+.0f} 天"
                    else:
                        rel = (a - s) / s * 100 if s else 0
                        ok = abs(rel) <= 1.0
                        dev = f"{rel:+.1f}%"
                    status = "一致" if ok else "❌ 不一致"
                diff_rows.append([ticker, y, name, a, s if s is not None else "", dev, status])

    out_dir = os.path.join(HERE, ep_key)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "ledger.csv"), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["标的", "财年", "科目", "代码", "数值(亿美元/%/天)", "XBRL标签或公式",
                    "报告期截止日", "10-K申报编号(accn)", "申报日期", "后续被重述", "数据性质"])
        w.writerows(ledger_rows)
    with open(os.path.join(out_dir, "diff.csv"), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["标的", "财年", "科目", "文章数值", "SEC数值", "偏差", "结论"])
        w.writerows(diff_rows)
    return ledger_rows, diff_rows


if __name__ == "__main__":
    key = sys.argv[1] if len(sys.argv) > 1 else "ep10"
    ledger, diff = build_ledger(key)
    bad = [r for r in diff if r[-1].startswith("❌")]
    manual = [r for r in diff if r[-1].startswith("SEC 无")]
    print(f"台账 {len(ledger)} 行；比对 {len(diff)} 项：一致 {len(diff) - len(bad) - len(manual)}，"
          f"不一致 {len(bad)}，需人工 {len(manual)}")
    for r in bad + manual:
        print("  ", r)
