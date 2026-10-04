#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Radar Due Diligence Evaluator & Visualizer
Evaluates a target company against the 6 objective buy-side dimensions based on SEC empirical rubrics,
checks pass/fail thresholds (Total >= 45/60, min 6.0 each), and renders an institutional radar chart.

Usage:
    python3 radar_evaluator.py --ticker AAPL --scores 9.2 9.5 8.8 8.5 8.0 9.0 --output_png ./aapl_radar.png
"""

import argparse
import sys
import math

def evaluate_and_plot(ticker, scores, output_png=None):
    categories = [
        '① 真实造血质量\n(Cash Flow Quality)',
        '② 商业护城河深度\n(Economic Moat)',
        '③ 资本分配纪律\n(Capital Discipline)',
        '④ 估值安全边际\n(Margin of Safety)',
        '⑤ 非对称盈亏比\n(Risk/Reward Asymmetry)',
        '⑥ 前置证伪明确度\n(Invalidation Triggers)'
    ]
    
    if len(scores) != 6:
        raise ValueError(f"Exactly 6 scores required, got {len(scores)}")

    for s in scores:
        if not (0.0 <= s <= 10.0):
            raise ValueError(f"Score {s} out of bounds (must be between 0.0 and 10.0)")

    total_score = sum(scores)
    all_passed_min = all(s >= 6.0 for s in scores)
    passed_total = total_score >= 45.0
    overall_pass = all_passed_min and passed_total

    print("\n" + "="*80)
    print(f"       【买方投资备忘录·六维客观量规自查评估】 标的: {ticker.upper()}")
    print("="*80)
    for cat, score in zip(categories, scores):
        clean_cat = cat.replace('\n', ' ')
        status = "✅ 达标" if score >= 6.0 else "❌ 不及格"
        print(f"• {clean_cat:<38}: {score:4.1f} / 10.0 分  [{status}]")
    print("-" * 80)
    print(f"• 六维累计总分: {total_score:.1f} / 60.0 分 (基准及格线: 45.0 分)")
    print(f"• 单项最低底线: {'全部项 >= 6.0分 (符合要求)' if all_passed_min else '存在单项 < 6.0分的不及格缺陷'}")
    print(f"★ 投委会风控综合判定: 【 {'通过审核 (PROCEED)' if overall_pass else '未通过审核 (REJECT / WAIT)'} 】")
    print("="*80 + "\n")

    if output_png:
        try:
            import numpy as np
            import matplotlib.pyplot as plt
            import matplotlib.font_manager as fm
            
            font_path = '/System/Library/Fonts/Hiragino Sans GB.ttc'
            prop = fm.FontProperties(fname=font_path)
            bold_prop = fm.FontProperties(fname=font_path, weight='bold')

            plt.style.use('dark_background')
            plt.rcParams['font.sans-serif'] = ['Hiragino Sans GB', 'Songti SC', 'STHeiti', 'DejaVu Sans']
            plt.rcParams['axes.unicode_minus'] = False

            N = len(categories)
            angles = [n / float(N) * 2 * np.pi for n in range(N)]
            angles += angles[:1]
            plot_scores = scores + scores[:1]

            fig, ax = plt.subplots(figsize=(6.8, 6.0), subplot_kw=dict(polar=True), dpi=160)
            fig.patch.set_facecolor('#0d1117')
            ax.set_facecolor('#161b22')

            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(categories, fontproperties=bold_prop, fontsize=9.2, color='#c9d1d9')

            ax.set_ylim(0, 10)
            ax.set_yticks([2, 4, 6, 8, 10])
            ax.set_yticklabels(['2', '4', '6 (及格线)', '8', '10分'], fontproperties=prop, fontsize=8, color='#8b949e')
            ax.set_rlabel_position(75)
            ax.grid(color='#30363d', linestyle='--', alpha=0.5)

            # Passing threshold ring at score 6.0
            theta_ring = np.linspace(0, 2*np.pi, 200)
            ax.plot(theta_ring, [6.0]*200, color='#8b949e', linestyle=':', linewidth=1.2, label='最低单项及格底线 (6.0分)')

            line_color = '#3fb950' if overall_pass else '#f85149'
            ax.plot(angles, plot_scores, color=line_color, linewidth=2.8, linestyle='-', 
                    label=f'{ticker.upper()} 自查得分 (总分: {total_score:.1f}分 | {"综合表现稳健" if overall_pass else "存在结构性缺陷"})')
            ax.fill(angles, plot_scores, color=line_color, alpha=0.25)
            ax.spines['polar'].set_color('#30363d')

            ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.16), prop=prop, fontsize=9.2, 
                      frameon=True, facecolor='#161b22', edgecolor='#30363d', labelcolor='#f0f6fc')
            ax.set_title(f'{ticker.upper()} 投资备忘录六维雷达打分评估模型',
                         fontproperties=bold_prop, fontsize=12.5, pad=24, color='#f0f6fc')

            plt.tight_layout()
            plt.savefig(output_png, facecolor=fig.get_facecolor(), edgecolor='none')
            plt.close()
            print(f"Radar chart saved successfully to: {output_png}")
        except Exception as e:
            print(f"Warning: Could not render radar image ({e}), textual evaluation preserved.", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="Six-Dimension Radar Evaluator")
    parser.add_argument("--ticker", type=str, required=True, help="Stock ticker symbol")
    parser.add_argument("--scores", type=float, nargs=6, required=True, 
                        help="6 dimension scores: CashFlow Moat CapitalAlloc MarginOfSafety RiskReward Invalidation")
    parser.add_argument("--output_png", type=str, default=None, help="Optional output PNG path for radar chart")

    args = parser.parse_args()
    evaluate_and_plot(args.ticker, args.scores, args.output_png)

if __name__ == "__main__":
    main()
