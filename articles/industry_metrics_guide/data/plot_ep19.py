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

MAERSK_BLUE = '#38BDF8'     # Maersk Ocean / Line
MAERSK_AMBER = '#F59E0B'    # Maersk Terminals / Callout
COSCO_RED = '#FB7185'       # COSCO Shipping Line
COSCO_TEAL = '#10B981'      # COSCO Net Margin Bar

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6.8), dpi=300)
fig.patch.set_facecolor(BG)

periods = ['2021', '2022', '2023', '2024', '2025', '2026 Q3*']
x = np.arange(len(periods))

# ==============================================================================
# LEFT PANEL: Freight Rate Cycle (Unified to USD / TEU)
# Maersk Reported $/FFE divided by 2 -> $/TEU
# COSCO International Route Revenue per TEU (COSCO Shipping Lines caliber; 26Q3* = 9M26 $1,343)
# ==============================================================================
maersk_teu = [1659, 2314, 1157, 1349, 1119, 1644]
cosco_teu  = [2151, 2703, 1118, 1450, 1257, 1343]

ax1.set_facecolor(PANEL_BG)
ax1.plot(x, maersk_teu, color=MAERSK_BLUE, marker='o', linewidth=2.8, markersize=7.5,
         label='马士基单箱运价 (USD/FFE÷2 折算 USD/TEU)', zorder=5)
ax1.plot(x, cosco_teu, color=COSCO_RED, marker='s', linewidth=2.8, markersize=7.5,
         label='中远海控国际航线单箱收入 (USD/TEU)', zorder=5)
ax1.fill_between(x, maersk_teu, cosco_teu, color='#334155', alpha=0.22, zorder=2)

ax1.set_ylim(600, 3250)
ax1.set_xticks(x)
ax1.set_xticklabels(periods, color=TEXT, fontsize=10.5, fontweight='bold')
ax1.set_ylabel('单箱平均运价 / 国际单箱收入 (美元/TEU)', color=TEXT, fontsize=11, fontweight='bold')
ax1.tick_params(axis='y', colors=MUTED, labelsize=10)
ax1.grid(axis='y', color=GRID, linestyle='--', linewidth=0.8, zorder=0)
for sp in ['top', 'right']:
    ax1.spines[sp].set_visible(False)
for sp in ['left', 'bottom']:
    ax1.spines[sp].set_color('#374151')

# Non-overlapping point annotations
m_off = [(0, -18), (0, -22), (18, 12), (0, -18), (0, -18), (0, 14)]
c_off = [(0, 12),  (0, 12),  (0, -20), (0, 12),  (0, 12),  (0, -26)]
for i, (mv, cv) in enumerate(zip(maersk_teu, cosco_teu)):
    ax1.annotate(f'${mv:,}', (x[i], mv), textcoords='offset points', xytext=m_off[i],
                 ha='center', color=MAERSK_BLUE, fontsize=9.2, fontweight='bold', zorder=6)
    lbl_c = f'${cv:,}\n(前9月)' if i == 5 else f'${cv:,}'
    ax1.annotate(lbl_c, (x[i], cv), textcoords='offset points', xytext=c_off[i],
                 ha='center', color=COSCO_RED, fontsize=9.2, fontweight='bold', zorder=6)

ax1.annotate('2023 运价腰斩\n双雄跌回 $1,100 线', xy=(2.0, 1185), xytext=(2.85, 2580),
             color='#FDE68A', fontsize=9.3, fontweight='bold', ha='center',
             bbox=dict(boxstyle='round,pad=0.32', facecolor='#1E293B', edgecolor='#F59E0B', lw=1),
             arrowprops=dict(arrowstyle='->', color='#F59E0B', lw=1.4), zorder=7)

ax1.set_title('全球集运单箱运价大周期共振 (统一折算美元/TEU)', color=TEXT, fontsize=13, fontweight='bold', pad=14)
ax1.legend(loc='upper right', facecolor='#0F172A', edgecolor='#374151', labelcolor=TEXT, fontsize=8.8, framealpha=0.92)

# ==============================================================================
# RIGHT PANEL: Group Net Profit Margin (%) — Integrated Logistics Dilution vs Pure Trunk-Line
# ==============================================================================
maersk_nm = [29.2, 36.0, 7.7, 11.2, 5.4, 16.9]
cosco_nm  = [26.8, 28.0, 13.6, 21.0, 14.1, 22.8]
w = 0.36

ax2.set_facecolor(PANEL_BG)
b1 = ax2.bar(x - w/2, maersk_nm, width=w, color=MAERSK_BLUE, alpha=0.88, label='马士基集团净利率 (%)', zorder=3)
b2 = ax2.bar(x + w/2, cosco_nm, width=w, color=COSCO_TEAL, alpha=0.88, label='中远海控归母净利率 (%)', zorder=3)

ax2.set_ylim(0, 44)
ax2.set_xticks(x)
ax2.set_xticklabels(['2021', '2022', '2023', '2024', '2025', '2026 Q3\n(单季)'], color=TEXT, fontsize=10.5, fontweight='bold')
ax2.set_ylabel('集团净利率 / 归母净利率 (%)', color=TEXT, fontsize=11, fontweight='bold')
ax2.tick_params(axis='y', colors=MUTED, labelsize=10)
ax2.grid(axis='y', color=GRID, linestyle='--', linewidth=0.8, zorder=0)
for sp in ['top', 'right']:
    ax2.spines[sp].set_visible(False)
for sp in ['left', 'bottom']:
    ax2.spines[sp].set_color('#374151')

for rect, val in zip(b1, maersk_nm):
    ax2.text(rect.get_x() + rect.get_width()/2, val + 0.7, f'{val:.1f}%',
             ha='center', va='bottom', color=MAERSK_BLUE, fontsize=9, fontweight='bold', zorder=6)
for rect, val in zip(b2, cosco_nm):
    ax2.text(rect.get_x() + rect.get_width()/2, val + 0.7, f'{val:.1f}%',
             ha='center', va='bottom', color='#6EE7B7', fontsize=9, fontweight='bold', zorder=6)

ax2.annotate('2023 起盈利能力倒挂\n马士基受低毛利综合物流稀释\n中远海控凭干线+净现金连续领先',
             xy=(4 + w/2, 16.5), xytext=(3.55, 34.5),
             color='#FDE68A', fontsize=9.2, fontweight='bold', ha='center',
             bbox=dict(boxstyle='round,pad=0.35', facecolor='#1E293B', edgecolor='#F59E0B', lw=1),
             arrowprops=dict(arrowstyle='->', color='#F59E0B', lw=1.4), zorder=7)

ax2.set_title('模式分化验证：综合物流稀释 vs 纯干线+高现金利润率', color=TEXT, fontsize=13, fontweight='bold', pad=14)
ax2.legend(loc='upper right', facecolor='#0F172A', edgecolor='#374151', labelcolor=TEXT, fontsize=8.8, framealpha=0.92)

fig.suptitle('马士基 (Maersk) vs 中远海控 (1919.HK)：单箱运价周期共振与盈利模式分化全景',
             color=TEXT, fontsize=15.5, fontweight='bold', y=0.97)
fig.text(0.5, 0.015,
         '数据来源：马士基 2021–2025 年报及 2026 Q3 中报（美元）；中远海控 2021–2025 年报及 2026 三季报（人民币）。左图 2026 Q3* 马士基为单季 3,287 美元/FFE÷2，中远海控为前9月国际单箱 1,343 美元/TEU。',
         ha='center', color=MUTED, fontsize=8.8)

plt.tight_layout(rect=[0.01, 0.04, 0.99, 0.92])
out_png = '/Users/siyi/Documents/code/investment-research/articles/industry_metrics_guide/assets/maersk_vs_cosco_metrics_trend.png'
plt.savefig(out_png, dpi=300, facecolor=BG)
print(f'Chart saved to {out_png}')
