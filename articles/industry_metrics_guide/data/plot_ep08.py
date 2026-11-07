import os
import matplotlib.pyplot as plt
import numpy as np

# Set font for macOS
plt.rcParams['font.sans-serif'] = ['PingFang SC', 'Heiti SC', 'Arial Unicode MS', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

periods = ['2021', '2022', '2023', '2024', '2025', '2026 Q3\n(单季)']
x = np.arange(len(periods))

# --- Data Series (100% SEC 10-K / 10-Q Ground Truth, 统一单位：亿美元 / %) ---
# 1. Total Revenue (亿美元)
isrg_rev = [57.1, 62.2, 71.2, 83.5, 100.6, 30.5]
syk_rev = [171.1, 184.5, 205.0, 226.0, 251.2, 65.2]

# 2. SG&A Intensity (%) & R&D Intensity (%)
isrg_sga = [25.7, 28.0, 27.6, 25.6, 23.7, 20.8]
syk_sga = [36.6, 34.6, 34.7, 34.0, 34.4, 35.5]
isrg_rd = [11.8, 14.1, 14.0, 13.7, 13.0, 13.4]
syk_rd = [7.2, 7.9, 6.8, 6.5, 6.5, 6.6]

# 3. Goodwill & Intangibles Net (商誉及并购无形资产净值, 亿美元)
isrg_gw_int = [9.8, 10.6, 9.9, 11.2, 12.2, 17.7]
syk_gw_int = [177.6, 197.7, 198.4, 202.5, 249.7, 248.7]

# 4. GAAP Operating Margin (%)
isrg_opm = [31.9, 25.3, 24.8, 28.1, 29.3, 19.4]  # Q3 2026 含 4.5 亿反垄断诉讼和解，剔除后为 34.2%
syk_opm = [15.1, 15.4, 19.0, 16.3, 19.5, 15.9]   # Q3 2026 含 2.93 亿商誉减值与 1.75 亿无形资产摊销

# --- Canvas & Palette Setup ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 9.5), dpi=300)
fig.patch.set_facecolor('#0b0f17')  # Deep Slate Navy

c_isrg = '#06b6d4'        # Cyan 500 (ISRG)
c_syk = '#f59e0b'         # Amber 500 (SYK)
c_isrg_line = '#38bdf8'   # Light Cyan
c_syk_line = '#fbbf24'    # Light Amber
c_rd_isrg = '#34d399'     # Emerald 400
c_rd_syk = '#f87171'      # Red 400
c_text = '#f8fafc'        # Slate 50
c_muted = '#94a3b8'       # Slate 400
c_grid = '#1e293b'        # Slate 800
c_card = '#111827'        # Gray 900

for ax in (ax1, ax2):
    ax.set_facecolor(c_card)
    ax.tick_params(colors=c_muted, labelsize=11)
    ax.grid(True, linestyle='--', alpha=0.35, color=c_grid)
    for spine in ax.spines.values():
        spine.set_color('#334155')

# ==========================================
# Subplot 1: 营业总收入 vs 销售管理费率 (SG&A %) & 研发费率 (R&D %)
# ==========================================
width = 0.35
rects1 = ax1.bar(x - width/2, isrg_rev, width, label='ISRG 营业总收入 (亿美元)', color=c_isrg, alpha=0.50)
rects2 = ax1.bar(x + width/2, syk_rev, width, label='SYK 营业总收入 (亿美元)', color=c_syk, alpha=0.50)

ax1.set_ylabel('营业总收入 (亿美元)', color=c_text, fontsize=12, fontweight='bold', labelpad=10)
ax1.set_xticks(x)
ax1.set_xticklabels(periods, fontsize=11, color=c_text)
ax1.set_ylim(0, 500)

ax1_twin = ax1.twinx()
l1 = ax1_twin.plot(x, syk_sga, color=c_syk_line, marker='s', linewidth=2.8, label='SYK 销售及管理费率 (SG&A %) [右轴]')
l2 = ax1_twin.plot(x, isrg_sga, color=c_isrg_line, marker='o', linewidth=2.8, label='ISRG 销售及管理费率 (SG&A %) [右轴]')
l3 = ax1_twin.plot(x, isrg_rd, color=c_rd_isrg, marker='^', linewidth=2.4, linestyle='--', label='ISRG 研发费用率 (R&D %) [右轴]')
l4 = ax1_twin.plot(x, syk_rd, color=c_rd_syk, marker='d', linewidth=2.4, linestyle=':', label='SYK 研发费用率 (R&D %) [右轴]')
ax1_twin.set_ylabel('期间费用占总营收比重 (%)', color=c_text, fontsize=12, fontweight='bold', labelpad=10)
ax1_twin.tick_params(colors=c_muted, labelsize=11)
ax1_twin.set_ylim(0, 46)
ax1_twin.grid(False)

for i, rect in enumerate(rects1):
    h = rect.get_height()
    y_pos = h + 5 if i != 1 else h - 22
    ax1.annotate(f"{h:.1f}", (rect.get_x() + rect.get_width()/2, y_pos),
                 ha='center', va='bottom', color='#67e8f9', fontsize=9.5, weight='bold')
for rect in rects2:
    h = rect.get_height()
    ax1.annotate(f"{h:.1f}", (rect.get_x() + rect.get_width()/2, h + 5),
                 ha='center', va='bottom', color='#fde68a', fontsize=9.5, weight='bold')

for i, txt in enumerate(syk_sga):
    ax1_twin.annotate(f"{txt:.1f}%", (x[i], syk_sga[i] + 1.1),
                      ha='center', color=c_syk_line, fontsize=9.5, weight='bold')
for i, txt in enumerate(isrg_sga):
    ax1_twin.annotate(f"{txt:.1f}%", (x[i], isrg_sga[i] + 1.1),
                      ha='center', color=c_isrg_line, fontsize=9.5, weight='bold')
for i, txt in enumerate(isrg_rd):
    ax1_twin.annotate(f"{txt:.1f}%", (x[i], isrg_rd[i] + 1.0),
                      ha='center', color=c_rd_isrg, fontsize=9, weight='bold')
for i, txt in enumerate(syk_rd):
    x_off = 0.16 if i == 5 else 0.0
    ax1_twin.annotate(f"{txt:.1f}%", (x[i] + x_off, syk_rd[i] - 2.3),
                      ha='center', color=c_rd_syk, fontsize=9, weight='bold')

ax1.set_title('图 1：营收规模 vs 销售跟台 (SG&A) 与内生研发 (R&D) 剪刀差\nISRG 装机规模效应摊薄 SG&A 至 20.8% vs SYK 重度临床跟台 SG&A 常年 34%+',
              fontsize=13.5, fontweight='bold', color=c_text, pad=16)

handles1, labels1 = ax1.get_legend_handles_labels()
handles2, labels2 = ax1_twin.get_legend_handles_labels()
ax1.legend(handles1 + handles2, labels1 + labels2, loc='upper right', ncol=2,
           facecolor=c_card, edgecolor='#334155', labelcolor=c_text, fontsize=8.8)

# ==========================================
# Subplot 2: 商誉与无形资产净值 vs GAAP 营业利润率 (%)
# ==========================================
rects3 = ax2.bar(x - width/2, isrg_gw_int, width, label='ISRG 商誉及无形资产净值 (亿美元)', color=c_isrg, alpha=0.55)
rects4 = ax2.bar(x + width/2, syk_gw_int, width, label='SYK 商誉及无形资产净值 (亿美元)', color='#f43f5e', alpha=0.55)

ax2.set_ylabel('期末商誉及并购无形资产净值 (亿美元)', color=c_text, fontsize=12, fontweight='bold', labelpad=10)
ax2.set_xticks(x)
ax2.set_xticklabels(periods, fontsize=11, color=c_text)
ax2.set_ylim(0, 440)

ax2_twin = ax2.twinx()
l5 = ax2_twin.plot(x, isrg_opm, color=c_isrg_line, marker='o', linewidth=2.8, label='ISRG GAAP 营业利润率 (%) [右轴]')
l6 = ax2_twin.plot(x, syk_opm, color='#fb7185', marker='s', linewidth=2.8, linestyle='--', label='SYK GAAP 营业利润率 (%) [右轴]')
ax2_twin.set_ylabel('GAAP 营业利润率 (%)', color=c_text, fontsize=12, fontweight='bold', labelpad=10)
ax2_twin.tick_params(colors=c_muted, labelsize=11)
ax2_twin.set_ylim(6, 40)
ax2_twin.grid(False)

for rect in rects3:
    h = rect.get_height()
    ax2.annotate(f"{h:.1f}", (rect.get_x() + rect.get_width()/2, h + 5),
                 ha='center', va='bottom', color='#67e8f9', fontsize=9.5, weight='bold')
for rect in rects4:
    h = rect.get_height()
    ax2.annotate(f"{h:.1f}", (rect.get_x() + rect.get_width()/2, h + 5),
                 ha='center', va='bottom', color='#fda4af', fontsize=9.5, weight='bold')

for i, txt in enumerate(isrg_opm):
    if i == 5:
        ax2_twin.annotate("19.4%\n(剔除和解34.2%)", (x[i] - 0.18, isrg_opm[i] + 1.3),
                          ha='center', color=c_isrg_line, fontsize=9, weight='bold')
    else:
        ax2_twin.annotate(f"{txt:.1f}%", (x[i], isrg_opm[i] + 1.2),
                          ha='center', color=c_isrg_line, fontsize=9.5, weight='bold')

for i, txt in enumerate(syk_opm):
    ax2_twin.annotate(f"{txt:.1f}%", (x[i], syk_opm[i] - 2.2),
                      ha='center', color='#fb7185', fontsize=9.5, weight='bold')

ax2.set_title('图 2：并购商誉无形资产重担 vs GAAP 真实营业利润率成色\nISRG 纯内生轻装高利润率 vs SYK 249亿商誉无形资产受摊销与减值侵蚀',
              fontsize=13.5, fontweight='bold', color=c_text, pad=16)

handles3, labels3 = ax2.get_legend_handles_labels()
handles4, labels4 = ax2_twin.get_legend_handles_labels()
ax2.legend(handles3 + handles4, labels3 + labels4, loc='upper left',
           facecolor=c_card, edgecolor='#334155', labelcolor=c_text, fontsize=9)

plt.tight_layout(pad=3.0)

output_path = 'articles/industry_metrics_guide/assets/isrg_vs_syk_metrics_trend.png'
plt.savefig(output_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
print(f"Chart successfully saved to {output_path}")
