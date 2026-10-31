import math

shares = 828.00
cur_price = 171.55
cur_net_debt = 29067.0
wacc = 0.085
discount_factor = 1.0 / (1.0 + wacc)**1.5  # 0.8847

scenarios = [
    {
        "name": "熊市情景 (Bear Case)",
        "prob": 0.20,
        "fcf_28": 4000.0,
        "eps_28": 7.50,
        "fwd_pe": 18.0,
        "fwd_pfcf": 25.0,
        "fwd_price": 136.00,  # $136.00
    },
    {
        "name": "基准情景 (Base Case)",
        "prob": 0.60,
        "fcf_28": 6000.0,
        "eps_28": 9.90,
        "fwd_pe": 22.0,
        "fwd_pfcf": 28.5,
        "fwd_price": 218.00,  # $218.00 (or $230 from SOTP)
    },
    {
        "name": "牛市情景 (Bull Case)",
        "prob": 0.20,
        "fcf_28": 9000.0,
        "eps_28": 13.00,
        "fwd_pe": 27.0,
        "fwd_pfcf": 32.3,
        "fwd_price": 351.00,  # $351.00
    }
]

print("="*85)
print(f"{'情景':<12} | {'2028E FCF':<10} | {'2028E EPS':<10} | {'2028远期目标':<12} | {'折现当期公允价':<14} | {'相对现价空间':<12}")
print("-"*85)
for s in scenarios:
    pv = s["fwd_price"] * discount_factor
    upside_fwd = (s["fwd_price"] - cur_price) / cur_price * 100
    upside_pv = (pv - cur_price) / cur_price * 100
    print(f"{s['name']:<12} | ${s['fcf_28']:<9,.0f}M | ${s['eps_28']:<9.2f} | ${s['fwd_price']:<11.2f} | ${pv:<13.2f} | {upside_fwd:<+11.1f}%")
print("="*85)

# Calculate Risk/Reward
fwd_base_rr = (218.00 - cur_price) / (cur_price - 136.00)
fwd_bull_rr = (351.00 - cur_price) / (cur_price - 136.00)
print(f"\n2028远期目标价对应的盈亏比:")
print(f"Base vs Bear: ({218.00:.2f} - {cur_price:.2f}) / ({cur_price:.2f} - 136.00) = {fwd_base_rr:.2f} : 1")
print(f"Bull vs Bear: ({351.00:.2f} - {cur_price:.2f}) / ({cur_price:.2f} - 136.00) = {fwd_bull_rr:.2f} : 1")

pv_base = 218.00 * discount_factor  # 192.87
pv_bear = 136.00 * discount_factor  # 120.32
pv_base_rr = (pv_base - cur_price) / (cur_price - pv_bear)
print(f"\n贴现到当期公允价对应的盈亏比 (严谨买方折现口径):")
print(f"Base PV vs Bear PV: ({pv_base:.2f} - {cur_price:.2f}) / ({cur_price:.2f} - {pv_bear:.2f}) = {pv_base_rr:.2f} : 1")

