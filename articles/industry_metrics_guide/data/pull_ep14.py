import os
import json
import urllib.request
import re

USER_AGENT = "investment-research personal-study contact@example.com"
HEADERS = {'User-Agent': USER_AGENT}

def get_company_facts(cik):
    cache_path = f".cache/CIK{cik}.json"
    if os.path.exists(cache_path):
        with open(cache_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    os.makedirs(".cache", exist_ok=True)
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(data, f)
            return data
    except Exception as e:
        print(f"Error fetching CIK{cik}: {e}")
        return None

print("Checking companyfacts fetch...")
cost_facts = get_company_facts("0000909832")
sbux_facts = get_company_facts("0000829224")
print("COST facts keys:", list(cost_facts['facts']['us-gaap'].keys())[:10] if cost_facts else None)
print("SBUX facts keys:", list(sbux_facts['facts']['us-gaap'].keys())[:10] if sbux_facts else None)

