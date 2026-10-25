import urllib.request
import json
import os

headers = {"User-Agent": "investment-research personal-study contact@example.com"}

def get_company_facts(cik):
    cache_path = f"/tmp/cik_{cik}.json"
    if os.path.exists(cache_path):
        with open(cache_path, "r") as f:
            return json.load(f)
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik.zfill(10)}.json"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        content = resp.read().decode("utf-8")
        with open(cache_path, "w") as f:
            f.write(content)
        return json.loads(content)

print("Pulling JPM (0000019617)...")
jpm = get_company_facts("0000019617")
print("Pulling BAC (0000070858)...")
bac = get_company_facts("0000070858")

def inspect_bank(name, data):
    print(f"\n==================== {name} ====================")
    facts = data["facts"]["us-gaap"]
    
    # tags to inspect: Assets, InterestAndDividendIncomeOperating, InterestExpense, InterestIncomeExpenseNet, NetIncomeLoss
    metrics = {
        "Total Assets": ["Assets"],
        "Interest Income": ["InterestAndDividendIncomeOperating", "InterestIncomeOperating"],
        "Interest Expense": ["InterestExpense"],
        "Net Interest Income (NII)": ["InterestIncomeExpenseNet"],
        "Non-interest Income": ["NoninterestIncome"],
        "Non-interest Expense": ["NoninterestExpense"],
        "Net Income": ["NetIncomeLoss"],
        "Loans": ["LoansAndLeasesReceivableNetReported", "LoansAndLeasesReceivableGrossReported"],
        "Deposits": ["Deposits"],
        "Provision": ["ProvisionForCreditLosses", "ProvisionForLoanAndLeaseLosses"],
    }
    
    for label, tags in metrics.items():
        found = False
        for tag in tags:
            if tag in facts:
                print(f"\n[{label}] ({tag}):")
                units = facts[tag]["units"].get("USD", [])
                # filter 10-K for FY 2021-2025
                fy_vals = {}
                for u in units:
                    form = u.get("form")
                    fy = u.get("fy")
                    fp = u.get("fp")
                    val = u.get("val")
                    if form in ["10-K", "10-K/A"] and fy in [2021, 2022, 2023, 2024, 2025] and (fp == "FY" or "frame" in u):
                        fy_vals[fy] = val
                for fy in sorted(fy_vals.keys()):
                    # convert to billions USD
                    val_b = fy_vals[fy] / 1e9
                    print(f"  FY{fy}: {val_b:.2f} 十亿美元 ($B) / {val_b*10:.1f} 亿美元 (原始: {fy_vals[fy]:,})")
                found = True
                break
        if not found:
            print(f"[{label}]: tags not found in us-gaap")

inspect_bank("JPMorgan Chase (JPM)", jpm)
inspect_bank("Bank of America (BAC)", bac)
