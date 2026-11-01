import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Set font family
plt.rcParams['font.sans-serif'] = ['STHeiti', 'Arial Unicode MS', 'PingFang HK', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

fig, axes = plt.subplots(2, 2, figsize=(14, 10), dpi=300)
fig.patch.set_facecolor('#F8FAFC')

years = ['2021', '2022', '2023', '2024', '2025', '26Q3(单季)']
x = np.arange(len(years))
width = 0.35

# Color Palette
c_isrg = '#0284C7'       # Intuitive Cyan/Sky Blue
c_isrg_dark = '#0369A1'
c_syk = '#D97706'        # Stryker Amber/Gold
c_syk_dark = '#B45309'

# 1. Total Revenue Comparison (亿美元)
ax1 = axes[0, 0]
ax1.set_facecolor('#FFFFFF')
isrg_rev = [57.1, 62.2, 71.2, 83.5, 100.6, 30.5]
syk_rev = [171.1, 184.5, 205.0, 226.0, 251.2, 65.2]

rects1 = ax1.bar(x - width/2, isrg_rev, width, label='直觉外科 (ISRG)', color=c_isrg, edgecolor='none', alpha=0.9)
rects2 = ax1.bar(x + width/2, syk_rev, width, label='史赛克 (SYK)', color=c_syk, edgecolor='none', alpha=0.9)

ax1.set_title('① 营业总收入走势与单季规模对比 (亿美元)', fontsize=13, fontweight='bold', pad=12, color='#1E293B')
ax1.set_xticks(x)
ax1.set_xticklabels(years, fontsize=10, color='#334155')
ax1.grid(axis='y', linestyle='--', alpha=0.3, color='#94A3B8')
ax1.legend(frameon=True, facecolor='#F8FAFC', edgecolor='none', fontsize=10)

for rect in rects1:
    h = rect.get_height()
    ax1.annotate(f'{h:.1f}', xy=(rect.get_x() + rect.get_width()/2, h),
                 xytext=(0, 3), textcoords='offset points', ha='center', va='bottom', fontsize=8, fontweight='bold', color=c_isrg_dark)
for rect in rects2:
    h = rect.get_height()
    ax1.annotate(f'{h:.1f}', xy=(rect.get_x() + rect.get_width()/2, h),
                 xytext=(0, 3), textcoords='offset points', ha='center', va='bottom', fontsize=8, fontweight='bold', color=c_syk_dark)

# 2. Installed Base (装机基座台数对比)
ax2 = axes[0, 1]
ax2.set_facecolor('#FFFFFF')
base_periods = ['2021', '2022', '2023', '2024', '2025', '2026Q3']
isrg_base = [6730, 7544, 8606, 9902, 11106, 12094]
syk_mako = [1500, 1800, 2100, 2500, 2950, 3300]

line1 = ax2.plot(base_periods, isrg_base, marker='o', linewidth=2.8, markersize=7.5, color=c_isrg, label='达芬奇在手总装机 (ISRG)')
line2 = ax2.plot(base_periods, syk_mako, marker='s', linewidth=2.8, markersize=7.5, color=c_syk, label='Mako骨科机器人装机 (SYK)')

ax2.set_title('② 手术机器人存量装机基座走势 (台)', fontsize=13, fontweight='bold', pad=12, color='#1E293B')
ax2.grid(True, linestyle='--', alpha=0.3, color='#94A3B8')
ax2.legend(frameon=True, facecolor='#F8FAFC', edgecolor='none', fontsize=10)

for i, txt in enumerate(isrg_base):
    ax2.annotate(f'{txt:,}', (base_periods[i], isrg_base[i]), textcoords='offset points', xytext=(0, 8), ha='center', fontsize=8.5, fontweight='bold', color=c_isrg_dark)
for i, txt in enumerate(syk_mako):
    ax2.annotate(f'{txt:,}', (base_periods[i], syk_mako[i]), textcoords='offset points', xytext=(0, -15), ha='center', fontsize=8.5, fontweight='bold', color=c_syk_dark)

# 3. Recurring Revenue Mix % (经常性收入占比)
ax3 = axes[1, 0]
ax3.set_facecolor('#FFFFFF')
rec_periods = ['2021', '2022', '2023', '2024', '2025', '26Q3']
isrg_rec = [75.0, 79.1, 83.4, 84.3, 84.2, 84.0]
syk_rec = [52.0, 54.0, 55.0, 56.0, 56.5, 57.0]

ax3.plot(rec_periods, isrg_rec, marker='o', linewidth=3, markersize=7.5, color=c_isrg, label='直觉外科经常性收入 % (耗材+维保+租赁)')
ax3.plot(rec_periods, syk_rec, marker='^', linewidth=2.5, markersize=7.5, color=c_syk, linestyle='--', label='史赛克植入假体/耗材复购占比估算 %')
ax3.axhline(y=80, color='#10B981', linestyle=':', alpha=0.8, label='高质量类SaaS年金阈值 (80%)')

ax3.set_title('③ 经常性耗材与年金收入占比走势 (%)', fontsize=13, fontweight='bold', pad=12, color='#1E293B')
ax3.set_ylim(40, 95)
ax3.grid(True, linestyle='--', alpha=0.3, color='#94A3B8')
ax3.legend(frameon=True, facecolor='#F8FAFC', edgecolor='none', fontsize=9.5)

for i, txt in enumerate(isrg_rec):
    ax3.annotate(f'{txt:.1f}%', (rec_periods[i], isrg_rec[i]), textcoords='offset points', xytext=(0, 8), ha='center', fontsize=9, fontweight='bold', color=c_isrg_dark)
for i, txt in enumerate(syk_rec):
    ax3.annotate(f'{txt:.1f}%', (rec_periods[i], syk_rec[i]), textcoords='offset points', xytext=(0, -15), ha='center', fontsize=9, fontweight='bold', color=c_syk_dark)

# 4. Capital Structure & Balance Sheet (最新Q3官方财报资产质量对决)
ax4 = axes[1, 1]
ax4.set_facecolor('#FFFFFF')

categories = ['现金与投资储备', '有息长短期负债', '商誉与无形资产']
isrg_bs = [68.0, 0.0, 3.5]
syk_bs = [32.7, 141.8, 190.0]
x_bs = np.arange(len(categories))

rects_bs1 = ax4.bar(x_bs - width/2, isrg_bs, width, label='直觉外科 (ISRG, 纯自研零负债)', color=c_isrg, alpha=0.9)
rects_bs2 = ax4.bar(x_bs + width/2, syk_bs, width, label='史赛克 (SYK, 杠杆并购重资产)', color=c_syk, alpha=0.9)

ax4.set_title('④ 最新资产负债表与资本结构对决 (2026Q3, 亿美元)', fontsize=13, fontweight='bold', pad=12, color='#1E293B')
ax4.set_xticks(x_bs)
ax4.set_xticklabels(categories, fontsize=10.5, color='#334155')
ax4.grid(axis='y', linestyle='--', alpha=0.3, color='#94A3B8')
ax4.legend(frameon=True, facecolor='#F8FAFC', edgecolor='none', fontsize=9.5)

for rect in rects_bs1:
    h = rect.get_height()
    ax4.annotate(f'{h:.1f}', xy=(rect.get_x() + rect.get_width()/2, h),
                 xytext=(0, 3), textcoords='offset points', ha='center', va='bottom', fontsize=9, fontweight='bold', color=c_isrg_dark)
for rect in rects2:
    h = rect.get_height()
    ax4.annotate(f'{h:.1f}', xy=(rect.get_x() + rect.get_width()/2, h),
                 xytext=(0, 3), textcoords='offset points', ha='center', va='bottom', fontsize=9, fontweight='bold', color=c_syk_dark)

plt.tight_layout(pad=3.0)
out_path = '/Users/siyi/Documents/code/investment-research/articles/industry_metrics_guide/assets/isrg_vs_syk_metrics_trend.png'
plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
print('Chart successfully generated and saved to:', out_path)
