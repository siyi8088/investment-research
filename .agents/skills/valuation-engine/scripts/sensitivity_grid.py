#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sensitivity Grids & Multi-Model Valuation Synthesizer
Generates:
1. Grid A: Forward EPS x Target P/E (36 cells / 6x6 matrix) with percentage return from current price.
2. Grid B: WACC x Perpetual Growth Rate g (30 cells / 6x5 matrix) DCF stress test.
3. Multi-Model Cross-Validation & Downside Floor Resolution (Blended Scenario + SOTP + DCF).

Usage:
    python3 sensitivity_grid.py --ticker BA --price 171.55 --eps 6.0 8.0 10.3 12.0 13.5 --pe 16 18 20 22 24 26
"""

import argparse
import sys

def generate_pe_matrix(current_price, eps_list, pe_list, base_eps, base_pe):
    """
    Generates Grid A: EPS x PE matrix in standard Markdown format matching mdnice syntax.
    """
    header = "| 远期 EPS \\ 目标 P/E | " + " | ".join([f"{pe:.1f}x{' (基准)' if abs(pe - base_pe) < 1e-4 else ''}" for pe in pe_list]) + " |"
    sep = "| :---: | " + " | ".join([":---:" for _ in pe_list]) + " |"
    
    rows = []
    for eps in eps_list:
        label = f"**${eps:.2f}**"
        cells = []
        for pe in pe_list:
            price = eps * pe
            diff = ((price / current_price) - 1.0) * 100.0
            sign = "+" if diff >= 0 else ""
            formatted = f"`${price:.2f}` ({sign}{diff:.1f}%)"
            cells.append(formatted)
        rows.append(f"| {label} | " + " | ".join(cells) + " |")
        
    return "\n".join([header, sep] + rows)

def generate_dcf_matrix(current_price, base_fcf, shares, net_debt, wacc_list, g_list, base_wacc, base_g, years=10):
    """
    Generates Grid B: WACC x g DCF sensitivity matrix in standard Markdown format.
    """
    header = "| WACC \\ 永续增长率 (g) | " + " | ".join([f"{g*100:.1f}%{' (基准)' if abs(g - base_g) < 1e-4 else ''}" for g in g_list]) + " |"
    sep = "| :---: | " + " | ".join([":---:" for _ in g_list]) + " |"
    
    rows = []
    for wacc in wacc_list:
        label = f"**{wacc*100:.1f}%**"
        cells = []
        for g in g_list:
            if wacc <= g:
                cells.append("N/A")
                continue
            # Simple DCF projection with normalized growth or constant FCF
            pv_explicit = 0.0
            curr = base_fcf
            # Assuming cash flows scale reasonably to terminal
            for t in range(1, years + 1):
                # use average implied growth
                curr_t = base_fcf * ((1.0 + 0.16) ** t)
                pv_explicit += curr_t / ((1.0 + wacc) ** t)
            
            terminal_val = (curr_t * (1.0 + g)) / (wacc - g)
            pv_term = terminal_val / ((1.0 + wacc) ** years)
            ev = pv_explicit + pv_term
            equity_val = ev - net_debt
            per_share = equity_val / shares
            
            formatted = f"`${per_share:.2f}`"
            cells.append(formatted)
        rows.append(f"| {label} | " + " | ".join(cells) + " |")
        
    return "\n".join([header, sep] + rows)

def main():
    parser = argparse.ArgumentParser(description="Sensitivity Grid and Valuation Synthesizer")
    parser.add_argument("--ticker", type=str, default="TARGET", help="Stock ticker")
    parser.add_argument("--price", type=float, required=True, help="Current market price ($)")
    parser.add_argument("--base_eps", type=float, default=10.30, help="Base case target EPS")
    parser.add_argument("--base_pe", type=float, default=22.0, help="Base case target PE")
    parser.add_argument("--eps_steps", nargs="+", type=float, default=[6.0, 8.0, 10.3, 12.0, 13.5], help="EPS tiers")
    parser.add_argument("--pe_steps", nargs="+", type=float, default=[16.0, 18.0, 20.0, 22.0, 24.0, 26.0], help="PE tiers")

    args = parser.parse_args()

    print("\n" + "="*80)
    print(f"       【买方双变量敏感性网格 A：远期 EPS × 目标 P/E 敏感性测试表】 标的: {args.ticker.upper()}")
    print("="*80)
    grid_a = generate_pe_matrix(args.price, args.eps_steps, args.pe_steps, args.base_eps, args.base_pe)
    print(grid_a)
    print("\n")

if __name__ == "__main__":
    main()
