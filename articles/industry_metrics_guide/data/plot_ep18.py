import os
import numpy as np
import matplotlib.pyplot as plt

# Dark Institutional Theme
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang SC', 'Heiti TC', 'STHeiti']
plt.rcParams['axes.unicode_minus'] = False

BG = '#0B111E'
PANEL_BG = '#111827'
GRID = '#1F2937'
TEXT = '#F3F4F6'
MUTED = '#9CA3AF'

XOM_BLUE = '#38BDF8'      # XOM Upstream / Prod
XOM_AMBER = '#F59E0B'     # XOM Downstream (Refining/Chem/Spec)
XOM_LINE = '#7DD3FC'      # XOM Lifting Cost line
COP_TEAL = '#10B981'      # COP Pure Upstream / Prod
COP_CORAL = '#FB7185'     # COP Lifting Cost line

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6.8), dpi=300)
fig.patch.set_facecolor(BG)

# ==============================================================================
# LEFT PANEL: Daily Production (MBOE/d) Bars + ASC 932 Consolidated Lifting Cost ($/BOE)
# ==============================================================================
years_l = ['2021', '2022', '2023', '2024', '2025']
x_l = np.arange(len(years_l))
w_l = 0.34

xom_prod = [3712, 3737, 3738, 4333, 4736]
cop_prod = [1567, 1738, 1826, 1987, 2375]

xom_lift = [12.15, 13.09, 12.05, 11.70, 11.29]
cop_lift = [9.99, 11.27, 11.87, 12.26, 12.01]

ax1.set_facecolor(PANEL_BG)
b1 = ax1.bar(x_l - w_l/2, xom_prod, width=w_l, color=XOM_BLUE, alpha=0.82, label='XOM 油气当量日产量 (左轴)', zorder=3)
b2 = ax1.bar(x_l + w_l/2, cop_prod, width=w_l, color=COP_TEAL, alpha=0.82, label='COP 油气当量日产量 (左轴)', zorder=3)

ax1.set_ylim(0, 8500)
ax1.set_xticks(x_l)
ax1.set_xticklabels(years_l, color=TEXT, fontsize=11, fontweight='bold')
ax1.set_ylabel('油气当量日产量 (千桶/日, MBOE/d)', color=TEXT, fontsize=11, fontweight='bold')
ax1.tick_params(axis='y', colors=MUTED, labelsize=10)
ax1.grid(axis='y', color=GRID, linestyle='--', linewidth=0.8, zorder=0)
for sp in ['top', 'right']:
    ax1.spines[sp].set_visible(False)
for sp in ['left', 'bottom']:
    ax1.spines[sp].set_color('#374151')

# Bar labels placed cleanly at vertical center of each bar (zero collision with upper lines)
for rect, val in zip(b1, xom_prod):
    ax1.text(rect.get_x() + rect.get_width()/2, val * 0.52, f'{val:,}',
             ha='center', va='center', color='#0B111E', fontsize=9.2, fontweight='bold', zorder=5)
for rect, val in zip(b2, cop_prod):
    ax1.text(rect.get_x() + rect.get_width()/2, val * 0.52, f'{val:,}',
             ha='center', va='center', color='#0B111E', fontsize=9.2, fontweight='bold', zorder=5)

# Twin axis for Lifting Cost ($/BOE) — floats cleanly in upper half above all bars
ax1_r = ax1.twinx()
ax1_r.set_ylim(1.0, 17.2)
l1 = ax1_r.plot(x_l, xom_lift, color=XOM_LINE, marker='o', linewidth=2.6, markersize=7,
                label='XOM 并表单桶开采成本 $/BOE (右轴)', zorder=6)
l2 = ax1_r.plot(x_l, cop_lift, color=COP_CORAL, marker='s', linewidth=2.6, markersize=7,
                label='COP 并表单桶开采成本 $/BOE (右轴)', zorder=6)

ax1_r.set_ylabel('ASC 932 并表单桶开采成本 (美元/桶油当量)', color=TEXT, fontsize=11, fontweight='bold')
ax1_r.tick_params(axis='y', colors=MUTED, labelsize=10)
ax1_r.spines['top'].set_visible(False)
ax1_r.spines['left'].set_visible(False)
ax1_r.spines['bottom'].set_visible(False)
ax1_r.spines['right'].set_color('#374151')

# Cost point labels with explicit non-overlapping offsets around the 2023-2024 crossover
xom_off = [(0, 11), (0, 11), (0, 12), (0, -16), (0, -16)]
cop_off = [(0, -16), (0, -16), (0, -16), (0, 11), (0, 11)]
for i, (xv, cv) in enumerate(zip(xom_lift, cop_lift)):
    ax1_r.annotate(f'${xv:.2f}', (x_l[i], xv), textcoords='offset points', xytext=xom_off[i],
                   ha='center', color=XOM_LINE, fontsize=9.5, fontweight='bold', zorder=7)
    ax1_r.annotate(f'${cv:.2f}', (x_l[i], cv), textcoords='offset points', xytext=cop_off[i],
                   ha='center', color=COP_CORAL, fontsize=9.5, fontweight='bold', zorder=7)

# Crossover callout — points cleanly to exact 2023-2024 line intersection with zero text overlap
ax1_r.annotate('成本曲线倒挂\nXOM 跌破 COP', xy=(2.22, 11.98), xytext=(2.55, 15.4),
               color='#FDE68A', fontsize=9.5, fontweight='bold', ha='center',
               bbox=dict(boxstyle='round,pad=0.32', facecolor='#1E293B', edgecolor='#F59E0B', lw=1),
               arrowprops=dict(arrowstyle='->', color='#F59E0B', lw=1.4), zorder=8)

ax1.set_title('产量规模扩张与单桶开采成本倒挂 (2021–2025)', color=TEXT, fontsize=13, fontweight='bold', pad=14)

handles1 = [b1, b2, l1[0], l2[0]]
labels1 = [h.get_label() for h in handles1]
ax1.legend(handles1, labels1, loc='upper left', facecolor='#0F172A', edgecolor='#374151',
           labelcolor=TEXT, fontsize=8.6, framealpha=0.92)

# ==============================================================================
# RIGHT PANEL: XOM Integrated Earnings (Upstream vs Downstream/Chem) vs COP Pure E&P
# ==============================================================================
periods_r = ['2021', '2022', '2023', '2024', '2025', '2026 Q3\n(单季)']
x_r = np.arange(len(periods_r))
w_r = 0.36

xom_up = np.array([15775, 36479, 21308, 25390, 21354, 7088]) / 100.0   # $100M (亿美元)
xom_ds = np.array([9901, 20924, 16493, 9662, 11080, 9189]) / 100.0     # Energy+Chem+Specialty ($100M)
cop_ni = np.array([8079, 18680, 10957, 9245, 7988, 4001]) / 100.0      # COP Net Income ($100M)

ax2.set_facecolor(PANEL_BG)
r1 = ax2.bar(x_r - w_r/2, xom_up, width=w_r, color=XOM_BLUE, alpha=0.88, label='XOM 上游税后盈利', zorder=3)
r2 = ax2.bar(x_r - w_r/2, xom_ds, width=w_r, bottom=xom_up, color=XOM_AMBER, alpha=0.90,
             label='XOM 炼化/化工/特种盈利', zorder=3)
r3 = ax2.bar(x_r + w_r/2, cop_ni, width=w_r, color=COP_TEAL, alpha=0.88, label='COP 纯上游归母净利', zorder=3)

ax2.set_ylim(0, 665)
ax2.set_xticks(x_r)
ax2.set_xticklabels(periods_r, color=TEXT, fontsize=10.5, fontweight='bold')
ax2.set_ylabel('税后分部盈利 / 归母净利润 (亿美元)', color=TEXT, fontsize=11, fontweight='bold')
ax2.tick_params(axis='y', colors=MUTED, labelsize=10)
ax2.grid(axis='y', color=GRID, linestyle='--', linewidth=0.8, zorder=0)
for sp in ['top', 'right']:
    ax2.spines[sp].set_visible(False)
for sp in ['left', 'bottom']:
    ax2.spines[sp].set_color('#374151')

# Labels for XOM stacked bars (Downstream share % above bar, and Upstream/Downstream inside if tall enough)
for i in range(len(periods_r)):
    tot = xom_up[i] + xom_ds[i]
    ds_pct = xom_ds[i] / tot * 100
    ax2.text(x_r[i] - w_r/2, tot + 10, f'下游\n{ds_pct:.1f}%',
             ha='center', va='bottom', color='#FCD34D', fontsize=8.6, fontweight='bold', zorder=6)
    if xom_up[i] >= 120:
        ax2.text(x_r[i] - w_r/2, xom_up[i]/2, f'{xom_up[i]:.0f}',
                 ha='center', va='center', color='#0B111E', fontsize=8.5, fontweight='bold', zorder=5)
    if xom_ds[i] >= 85:
        ax2.text(x_r[i] - w_r/2, xom_up[i] + xom_ds[i]/2, f'{xom_ds[i]:.0f}',
                 ha='center', va='center', color='#0B111E', fontsize=8.5, fontweight='bold', zorder=5)
    ax2.text(x_r[i] + w_r/2, cop_ni[i] + 10, f'{cop_ni[i]:.1f}',
             ha='center', va='bottom', color='#6EE7B7', fontsize=9, fontweight='bold', zorder=6)

# Callout for 2026 Q3 Downstream > Upstream (arrow terminates cleanly ABOVE the label)
ax2.annotate('2026 Q3 炼化大爆发\nXOM 炼化+化工占 56.5%', xy=(5 - w_r/2, 232), xytext=(3.9, 495),
             color='#FDE68A', fontsize=9.5, fontweight='bold', ha='center',
             bbox=dict(boxstyle='round,pad=0.32', facecolor='#1E293B', edgecolor='#F59E0B', lw=1),
             arrowprops=dict(arrowstyle='->', color='#F59E0B', lw=1.4), zorder=8)

ax2.set_title('一体化炼化对冲 vs 纯上游油价弹性 (2021–2026 Q3)', color=TEXT, fontsize=13, fontweight='bold', pad=14)
ax2.legend(loc='upper right', facecolor='#0F172A', edgecolor='#374151', labelcolor=TEXT, fontsize=8.8, framealpha=0.92)

fig.suptitle('埃克森美孚 (XOM) vs 康菲石油 (COP)：成本曲线倒挂与一体化盈利对冲全景',
             color=TEXT, fontsize=15.5, fontweight='bold', y=0.97)
fig.text(0.5, 0.015,
         '数据来源：XOM 与 COP 2021–2025 年 Form 10-K（ASC 932 油气补充披露及分部报告）及 2026 Q3 Form 10-Q；右图 XOM 为各经营分部税后盈利加总（不含总部融资费用）。',
         ha='center', color=MUTED, fontsize=9)

plt.tight_layout(rect=[0.01, 0.04, 0.99, 0.92])
out_png = '/Users/siyi/Documents/code/investment-research/articles/industry_metrics_guide/assets/xom_vs_cop_metrics_trend.png'
plt.savefig(out_png, dpi=300, facecolor=BG)
print(f'Chart saved to {out_png}')
