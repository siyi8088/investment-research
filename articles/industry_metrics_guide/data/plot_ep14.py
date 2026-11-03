import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# Set matplotlib fonts for Mac
plt.rcParams['font.sans-serif'] = ['PingFang SC', 'Heiti SC', 'Arial Unicode MS', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

years = ['FY2021', 'FY2022', 'FY2023', 'FY2024', 'FY2025', 'FY2026']
x = np.arange(len(years))

# 1. Comparable Sales Growth (SSSG %)
cost_sssg = [16.0, 14.0, 5.0, 5.0, 6.0, 8.0]
cost_sssg_core = [13.0, 10.0, 7.0, 6.0, 8.0, 7.0]  # ex-gas/FX
sbux_sssg = [20.0, 8.0, 8.0, -2.0, -2.0, 6.2]

# 2. Operating Margin (%)
cost_op_margin = [3.42, 3.43, 3.35, 3.65, 3.77, 3.85]
sbux_op_margin = [16.76, 14.32, 16.32, 14.95, 7.90, 9.74]

# 3. Costco Membership Fee Coverage vs Renewal Rate
cost_fee_cover = [57.8, 54.2, 56.5, 52.0, 51.3, 50.6]  # Membership Fee / Operating Income (%)
cost_renewal = [91.0, 93.0, 92.7, 92.9, 92.3, 92.3]  # US & Canada Renewal Rate (%)

# 4. Costco AUV ($M) vs SBUX Global Stores
cost_auv = [239.2, 269.5, 279.8, 285.1, 299.2, 320.8]  # Average Sales per Warehouse ($M)
sbux_stores = [33833, 35711, 38038, 40199, 40990, 41607]

fig, axs = plt.subplots(2, 2, figsize=(16, 11), dpi=200)
fig.patch.set_facecolor('#0f172a')  # Slate 900 dark theme

# Theme colors
c_cost = '#38bdf8'       # Sky blue (Costco)
c_cost_sub = '#0284c7'   # Deep sky blue
c_sbux = '#10b981'       # Emerald green (Starbucks)
c_accent = '#f59e0b'     # Amber
c_text = '#f8fafc'       # Light text
c_muted = '#94a3b8'      # Slate 400
c_grid = '#334155'       # Slate 700

for ax in axs.flat:
    ax.set_facecolor('#1e293b')  # Slate 800
    ax.tick_params(colors=c_muted, labelsize=11)
    ax.grid(True, linestyle='--', alpha=0.3, color=c_grid)
    for spine in ax.spines.values():
        spine.set_color(c_grid)

# --- Subplot 1: SSSG Comparison ---
ax1 = axs[0, 0]
ax1.plot(x, cost_sssg, marker='o', linewidth=2.5, color=c_cost, label='Costco 全球同店增速 (SSSG, 含油价/汇率)')
ax1.plot(x, cost_sssg_core, marker='s', linewidth=2, linestyle=':', color='#7dd3fc', label='Costco 核心同店增速 (剔除油价与汇率)')
ax1.plot(x, sbux_sssg, marker='D', linewidth=2.5, color=c_sbux, label='星巴克 全球同店增速 (SSSG)')
ax1.axhline(0, color='#ef4444', linestyle='--', alpha=0.6, linewidth=1.2)
ax1.set_title('图 1：同店销售增长率 (SSSG) 跨周期对决：订阅飞轮 vs 体验溢价', fontsize=13, fontweight='bold', color=c_text, pad=12)
ax1.set_xticks(x)
ax1.set_xticklabels(years)
ax1.set_ylabel('同比增速 (%)', color=c_muted, fontsize=11)
ax1.legend(loc='upper right', facecolor='#0f172a', edgecolor=c_grid, labelcolor=c_text, fontsize=9.5)
for i, txt in enumerate(cost_sssg):
    ax1.annotate(f"{txt:.1f}%", (x[i], cost_sssg[i]+0.7), color=c_cost, fontsize=9, ha='center', weight='bold')
for i, txt in enumerate(sbux_sssg):
    offset = -1.6 if txt < 0 else 0.7
    ax1.annotate(f"{txt:.1f}%", (x[i], sbux_sssg[i]+offset), color=c_sbux, fontsize=9, ha='center', weight='bold')

# --- Subplot 2: Operating Margin Comparison ---
ax2 = axs[0, 1]
ax2.plot(x, cost_op_margin, marker='o', linewidth=2.5, color=c_cost, label='Costco 营业利润率 (压制暴利/极致薄利)')
ax2.plot(x, sbux_op_margin, marker='D', linewidth=2.5, color=c_sbux, label='星巴克 营业利润率 (高品牌溢价/重资产波动)')
ax2.set_title('图 2：营业利润率 (Operating Margin %)：3.5% 铁律 vs 周期落差', fontsize=13, fontweight='bold', color=c_text, pad=12)
ax2.set_xticks(x)
ax2.set_xticklabels(years)
ax2.set_ylabel('营业利润率 (%)', color=c_muted, fontsize=11)
ax2.legend(loc='upper right', facecolor='#0f172a', edgecolor=c_grid, labelcolor=c_text, fontsize=9.5)
for i, txt in enumerate(cost_op_margin):
    ax2.annotate(f"{txt:.2f}%", (x[i], cost_op_margin[i]+0.6), color=c_cost, fontsize=9, ha='center', weight='bold')
for i, txt in enumerate(sbux_op_margin):
    ax2.annotate(f"{txt:.1f}%", (x[i], sbux_op_margin[i]+0.6), color=c_sbux, fontsize=9, ha='center', weight='bold')

# --- Subplot 3: Costco Membership Moat ---
ax3 = axs[1, 0]
line1 = ax3.plot(x, cost_fee_cover, marker='o', linewidth=2.5, color=c_accent, label='会员费对营业利润覆盖率 (%) [左轴]')
ax3.set_ylabel('会员费覆盖率 (%)', color=c_accent, fontsize=11)
ax3.tick_params(axis='y', labelcolor=c_accent)
ax3.set_ylim(40, 70)

ax3_twin = ax3.twinx()
line2 = ax3_twin.plot(x, cost_renewal, marker='^', linewidth=2.5, linestyle='--', color='#a855f7', label='美加会员续费率 (%) [右轴]')
ax3_twin.set_ylabel('会员续费率 (%)', color='#a855f7', fontsize=11)
ax3_twin.tick_params(axis='y', labelcolor='#a855f7')
ax3_twin.set_ylim(85, 96)
ax3_twin.grid(False)

ax3.set_title('图 3：Costco 护城河：超 50% 利润源于会员费 + 92%+ 逆天续费率', fontsize=13, fontweight='bold', color=c_text, pad=12)
ax3.set_xticks(x)
ax3.set_xticklabels(years)
lines = line1 + line2
labels = [l.get_label() for l in lines]
ax3.legend(lines, labels, loc='lower left', facecolor='#0f172a', edgecolor=c_grid, labelcolor=c_text, fontsize=9.5)
for i, txt in enumerate(cost_fee_cover):
    ax3.annotate(f"{txt:.1f}%", (x[i], cost_fee_cover[i]+1.0), color=c_accent, fontsize=9, ha='center', weight='bold')
for i, txt in enumerate(cost_renewal):
    ax3_twin.annotate(f"{txt:.1f}%", (x[i], cost_renewal[i]+0.3), color='#a855f7', fontsize=9, ha='center', weight='bold')

# --- Subplot 4: Single Store AUV vs Store Scale Expansion ---
ax4 = axs[1, 1]
bars = ax4.bar(x - 0.2, cost_auv, width=0.4, color=c_cost_sub, alpha=0.85, label='Costco 单店年销售额 AUV ($M) [左轴]')
ax4.set_ylabel('Costco AUV ($ Millions)', color=c_cost, fontsize=11)
ax4.tick_params(axis='y', labelcolor=c_cost)
ax4.set_ylim(150, 360)

ax4_twin = ax4.twinx()
line_stores = ax4_twin.plot(x + 0.2, [s/1000 for s in sbux_stores], marker='o', linewidth=2.5, color=c_sbux, label='星巴克 全球门店总数 (千家) [右轴]')
ax4_twin.set_ylabel('星巴克门店总数 (千家)', color=c_sbux, fontsize=11)
ax4_twin.tick_params(axis='y', labelcolor=c_sbux)
ax4_twin.set_ylim(30, 46)
ax4_twin.grid(False)

ax4.set_title('图 4：单店生产力极限 vs 网络裂变：$3.2亿 AUV vs 4.1万家店', fontsize=13, fontweight='bold', color=c_text, pad=12)
ax4.set_xticks(x)
ax4.set_xticklabels(years)

lines4 = [bars, line_stores[0]]
labels4 = ['Costco AUV ($M) [左轴]', '星巴克 门店数 (千家) [右轴]']
ax4.legend(lines4, labels4, loc='upper left', facecolor='#0f172a', edgecolor=c_grid, labelcolor=c_text, fontsize=9.5)
for i, txt in enumerate(cost_auv):
    ax4.annotate(f"${txt:.0f}M", (x[i]-0.2, cost_auv[i]+5), color='#7dd3fc', fontsize=8.5, ha='center', weight='bold')
for i, txt in enumerate(sbux_stores):
    ax4_twin.annotate(f"{txt/1000:.1f}k", (x[i]+0.2, (txt/1000)+0.4), color=c_sbux, fontsize=8.5, ha='center', weight='bold')

plt.suptitle('好市多 (COST) vs 星巴克 (SBUX) 跨周期特异性财务与运营指标全景对决 (FY2021-FY2026)', fontsize=16, fontweight='bold', color=c_text, y=0.98)
plt.tight_layout(rect=[0, 0.03, 1, 0.96])

out_path = '../assets/cost_vs_sbux_metrics_trend.png'
plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', dpi=200)
print(f'Successfully generated {out_path}')

