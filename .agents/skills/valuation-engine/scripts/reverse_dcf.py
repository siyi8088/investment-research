#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reverse DCF Solver (Expectations Investing Engine)
Solves for the 10-year implied compound annual growth rate (CAGR) of Free Cash Flow (FCF)
required to justify current market Enterprise Value (EV).

Usage:
    python3 reverse_dcf.py --price 333.69 --shares 15100 --net_debt -40000 --wacc 0.085 --g 0.025 --base_fcf 108000
    python3 reverse_dcf.py --ticker GLW --price 149.79 --shares 888 --net_debt 4920 --wacc 0.085 --g 0.025 --base_fcf 1450 --hist_cagr 0.03
"""

import argparse
import sys

def solve_reverse_dcf(implied_ev, base_fcf, wacc, g, years=10):
    """
    Solves for the constant annual FCF growth rate 'r' over explicit forecast period (default 10 years)
    such that PV(explicit) + PV(terminal) = implied_ev.
    Uses robust bisection algorithm (pure python, zero external dependencies).
    """
    if wacc <= g:
        raise ValueError(f"WACC ({wacc*100:.2f}%) must be strictly greater than perpetual growth rate g ({g*100:.2f}%).")
    
    def calc_ev_for_growth(r):
        pv_explicit = 0.0
        current_fcf = base_fcf
        for t in range(1, years + 1):
            current_fcf *= (1.0 + r)
            pv_explicit += current_fcf / ((1.0 + wacc) ** t)
        
        # Terminal value at year 10
        terminal_val = (current_fcf * (1.0 + g)) / (wacc - g)
        pv_terminal = terminal_val / ((1.0 + wacc) ** years)
        return pv_explicit + pv_terminal, current_fcf

    # Bisection search range: -50% to +200% growth
    low = -0.50
    high = 2.00
    
    ev_low, _ = calc_ev_for_growth(low)
    ev_high, _ = calc_ev_for_growth(high)
    
    if ev_low > implied_ev:
        return low, ev_low, calc_ev_for_growth(low)[1]
    if ev_high < implied_ev:
        return high, ev_high, calc_ev_for_growth(high)[1]
        
    for _ in range(100):
        mid = (low + high) / 2.0
        ev_mid, fcf_end = calc_ev_for_growth(mid)
        if abs(ev_mid - implied_ev) < 1e-4 * implied_ev:
            return mid, ev_mid, fcf_end
        if ev_mid < implied_ev:
            low = mid
        else:
            high = mid
            
    return mid, ev_mid, fcf_end

def main():
    parser = argparse.ArgumentParser(description="Reverse DCF Expectations Solver")
    parser.add_argument("--ticker", type=str, default="TARGET", help="Stock ticker symbol")
    parser.add_argument("--price", type=float, required=True, help="Current stock price ($)")
    parser.add_argument("--shares", type=float, required=True, help="Fully diluted shares (Millions)")
    parser.add_argument("--net_debt", type=float, default=0.0, help="Net debt in $M (Positive = net debt, Negative = net cash)")
    parser.add_argument("--wacc", type=float, default=0.085, help="Weighted Average Cost of Capital (e.g., 0.085 for 8.5%)")
    parser.add_argument("--g", type=float, default=0.025, help="Perpetual growth rate (e.g., 0.025 for 2.5%)")
    parser.add_argument("--base_fcf", type=float, required=True, help="Normalized base year FCF ($M)")
    parser.add_argument("--hist_cagr", type=float, default=None, help="Historical 5-year FCF CAGR (e.g. 0.05 for 5%)")
    parser.add_argument("--mgmt_guidance", type=float, default=None, help="Management guided revenue/FCF growth rate")

    args = parser.parse_args()

    market_cap = args.price * args.shares
    implied_ev = market_cap + args.net_debt

    try:
        implied_r, calculated_ev, fcf_year10 = solve_reverse_dcf(
            implied_ev=implied_ev,
            base_fcf=args.base_fcf,
            wacc=args.wacc,
            g=args.g,
            years=10
        )
    except Exception as e:
        print(f"Error solving reverse DCF: {e}", file=sys.stderr)
        sys.exit(1)

    # Output formatted report
    print("\n" + "="*80)
    print(f"       【买方预期投资学·反向 DCF 逆向解算报告】 标的: {args.ticker.upper()}")
    print("="*80)
    print(f"• 当前股票市价: ${args.price:,.2f}")
    print(f"• 完全稀释股本: {args.shares:,.2f} M 股")
    print(f"• 股票总市值:   ${market_cap:,.2f} M (${market_cap/1000:,.2f} B)")
    print(f"• 综合净负债:   ${args.net_debt:,.2f} M ({'净负债' if args.net_debt >= 0 else '净现金'})")
    print(f"• 隐含企业价值: ${implied_ev:,.2f} M (${implied_ev/1000:,.2f} B)")
    print(f"• 基准折现率:   WACC = {args.wacc*100:.1f}%, 永续增长率 g = {args.g*100:.1f}%")
    print(f"• 基准年度 FCF: ${args.base_fcf:,.2f} M")
    print("-" * 80)
    print(f"★ 核心解算结论：市场当前价格隐含未来 10 年 FCF 年化复合增速必须达到: 【 {implied_r*100:+.2f}% 】")
    print(f"• 对应第 10 年自由现金流需达到: ${fcf_year10:,.2f} M (${fcf_year10/1000:,.2f} B，较当前扩大 {fcf_year10/args.base_fcf:.1f} 倍)")
    print("-" * 80)

    # Comparison and Expectations Matrix Mapping
    print("【预期差诊断与莫布森 2×2 决战矩阵定位】")
    if args.hist_cagr is not None:
        diff_hist = (implied_r - args.hist_cagr) * 100
        print(f"• 历史 5 年实际 FCF 增速: {args.hist_cagr*100:.1f}%")
        print(f"• 市场预期 vs 历史增速剪刀差: {diff_hist:+.1f} 个百分点")

    if args.mgmt_guidance is not None:
        diff_mgmt = (implied_r - args.mgmt_guidance) * 100
        print(f"• 管理层官方指引增速: {args.mgmt_guidance*100:.1f}%")
        print(f"• 市场预期 vs 管理层指引剪刀差: {diff_mgmt:+.1f} 个百分点")

    # Quadrant Classification
    print("\n【象限研判结果】:")
    if implied_r > 0.20:
        quadrant = "【象限 A：定价完美 (Priced for Perfection)】"
        desc = "当前市价已经全额折现了未来十年的高爆发奇迹，容错率极低，任何细微不及预期极易引发剧烈杀估值。"
    elif implied_r < 0.05:
        quadrant = "【象限 B / C：低预期区间 (Low Expectations)】"
        desc = "市场预期极度保守或悲观。若公司真实造血稳定或有潜在催化剂，可能蕴含戴维斯双击机会；若商业模式衰退，则需警惕价值陷阱。"
    else:
        quadrant = "【中性合理预期区间 (Balanced Expectations)】"
        desc = "市场定价基本符合中性成长路径，胜率取决于扎实跟踪公司季度基本面是否持续超越基准指引。"

    print(f"• 当前归属: {quadrant}")
    print(f"• 策略启示: {desc}")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
