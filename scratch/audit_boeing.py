# Integrated Boeing Financial & Valuation Audit Script
import math

shares = 828.00  # M shares
price = 171.55
mkt_cap = price * shares
total_debt = 48362.0
cash = 19295.0
net_debt = total_debt - cash
ev = mkt_cap + net_debt

print(f"--- 1. Market Baseline at $171.55 ---")
print(f"Price:      ${price:.2f}")
print(f"Shares:     {shares:.2f} M")
print(f"Market Cap: ${mkt_cap:,.2f} M (${mkt_cap/1e3:.2f} B)")
print(f"Net Debt:   ${net_debt:,.2f} M (${net_debt/1e3:.2f} B)")
print(f"EV:         ${ev:,.2f} M (${ev/1e3:.2f} B)")

print(f"\n--- 2. Reverse DCF Verification ---")
# Using bisection solver
def calc_ev(base_fcf, r, wacc, g, years=10):
    pv = 0.0
    fcf = base_fcf
    for t in range(1, years + 1):
        fcf *= (1.0 + r)
        pv += fcf / ((1.0 + wacc) ** t)
    terminal = (fcf * (1.0 + g)) / (wacc - g)
    pv += terminal / ((1.0 + wacc) ** years)
    return pv, fcf

wacc = 0.085
g = 0.025
base_fcf = 3500.0  # normalized

low, high = 0.0, 1.0
for _ in range(100):
    mid = (low + high) / 2.0
    est_ev, fcf_end = calc_ev(base_fcf, mid, wacc, g)
    if abs(est_ev - ev) < 1.0:
        break
    if est_ev < ev:
        low = mid
    else:
        high = mid

print(f"Base FCF:      ${base_fcf:,.2f} M")
print(f"WACC:          {wacc*100:.1f}%, g: {g*100:.1f}%")
print(f"Implied CAGR:  +{mid*100:.2f}%")
print(f"Terminal FCF:  ${fcf_end:,.2f} M (${fcf_end/1e3:.2f} B)")

print(f"\n--- 3. SOTP Verification ---")
# Forward Normalized Model (around 2028-2029)
bca_ebit = 5800.0
bca_mult = 18.0
bca_ev = bca_ebit * bca_mult

bgs_ebit = 4440.0
bgs_mult = 18.0
bgs_ev = bgs_ebit * bgs_mult

bds_ebit = 2400.0
bds_mult = 15.0
bds_ev = bds_ebit * bds_mult

total_ebit = bca_ebit + bgs_ebit + bds_ebit
total_sotp_ev = bca_ev + bgs_ev + bds_ev
implied_equity = total_sotp_ev - net_debt
forward_price = implied_equity / shares
discounted_price_1_5yr = forward_price / (1.085 ** 1.5)
discounted_price_2yr = forward_price / (1.085 ** 2.0)

print(f"Total SOTP EBIT: ${total_ebit:,.2f} M")
print(f"Total SOTP EV:   ${total_sotp_ev:,.2f} M (Weighted mult: {total_sotp_ev/total_ebit:.2f}x)")
print(f"Net Debt:        -${net_debt:,.2f} M")
print(f"Implied Equity:  ${implied_equity:,.2f} M")
print(f"Forward Share Price (at 2028):  ${forward_price:.2f}")
print(f"Discounted PV (1.5 yr at 8.5%): ${discounted_price_1_5yr:.2f}")
print(f"Discounted PV (2.0 yr at 8.5%): ${discounted_price_2yr:.2f}")

print(f"\n--- 4. Rigorous FY28E Three-Scenario Modeling ---")
# Connecting Operating metrics, FCF, EPS and Valuation
# In 2028, what are the realistic earnings and cash flow?
# Bear Case: 737 rate 40/mo, 787 6/mo, BDS struggles.
# Base Case: 737 rate 50/mo, 787 8/mo, BDS stabilized, matches mgmt FCF ~$6.0B.
# Bull Case: 737 rate 57/mo, 787 10/mo, 777X ramp, matches mgmt FCF ~$9.0B+.

scenarios = [
    {
        "name": "Bear Case (悲观)",
        "prob": 0.20,
        "fcf_2028": 4200.0,
        "ni_2028": 5800.0,
        "eps_2028": 7.00,
        "pe_mult": 18.0,
        "pfcf_mult": 24.0,
    },
    {
        "name": "Base Case (基准)",
        "prob": 0.60,
        "fcf_2028": 6000.0,
        "ni_2028": 8000.0,
        "eps_2028": 9.66,
        "pe_mult": 21.0,
        "pfcf_mult": 28.0,
    },
    {
        "name": "Bull Case (牛市)",
        "prob": 0.20,
        "fcf_2028": 9000.0,
        "ni_2028": 11000.0,
        "eps_2028": 13.28,
        "pe_mult": 25.0,
        "pfcf_mult": 32.0,
    }
]

for s in scenarios:
    price_by_pe = s["eps_2028"] * s["pe_mult"]
    price_by_fcf = (s["fcf_2028"] * s["pfcf_mult"]) / shares
    # blended fair value forward
    fwd_val = (price_by_pe + price_by_fcf) / 2.0
    # If discounted 1.5 years to current:
    pv_val = fwd_val / (1.085 ** 1.5)
    s["price_by_pe"] = price_by_pe
    s["price_by_fcf"] = price_by_fcf
    s["fwd_val"] = fwd_val
    s["pv_val"] = pv_val
    print(f"{s['name']}:")
    print(f"  FCF: ${s['fcf_2028']:,.0f}M | EPS: ${s['eps_2028']:.2f}")
    print(f"  2028 Value by P/E ({s['pe_mult']}x):   ${price_by_pe:.2f}")
    print(f"  2028 Value by P/FCF ({s['pfcf_mult']}x): ${price_by_fcf:.2f}")
    print(f"  2028 Forward Mean Value:       ${fwd_val:.2f}")
    print(f"  Discounted Present Value:      ${pv_val:.2f}")


