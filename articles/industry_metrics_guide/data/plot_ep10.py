import os
import matplotlib.pyplot as plt
import numpy as np

# Set font for macOS
plt.rcParams['font.sans-serif'] = ['PingFang SC', 'Heiti SC', 'Arial Unicode MS', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

periods = ['2021', '2022', '2023', '2024', '2025', '2026 Q3\n(单季/期末)']
x = np.arange(len(periods))

# --- Data Series (100% SEC 20-F/10-K & Q3 2026 6-K/10-Q Ground Truth, $ in Millions) ---
# Subplot 1: 高流动性资金储备 (百万美元) vs 全口径股本较2021年累计扩张率 (%)
legn_cash = [887.1, 1025.6, 1313.1, 1122.6, 948.6, 852.5]
crsp_cash = [2379.1, 1868.4, 1695.7, 1903.8, 1975.8, 2276.6]

# 全口径稀释股本 (已发行普通股 + 期权/RSU/权证/可转债潜在股本):
# LEGN: 2021 (330.6M) -> 2022 (352.7M) -> 2023 (375.1M) -> 2024 (376.5M) -> 2025 (380.0M) -> 2026Q3 (400.3M)
# CRSP: 2021 (86.8M) -> 2022 (87.1M) -> 2023 (89.0M) -> 2024 (95.4M) -> 2025 (104.6M) -> 2026Q3 (113.3M)
legn_dil_growth = [0.0, 6.7, 13.5, 13.9, 14.9, 21.1]
crsp_dil_growth = [0.0, 0.3, 2.5, 9.9, 20.5, 30.5]

# Subplot 2: 营业总收入 (百万美元) vs 营业利润/亏损 (百万美元)
legn_rev = [68.8, 117.0, 285.1, 627.3, 1028.9, 359.5]
crsp_rev = [915.0, 1.2, 371.2, 37.3, 3.5, 12.7]

legn_opinc = [-406.3, -435.0, -528.1, -309.5, -136.5, 46.8]
crsp_opinc = [373.5, -673.2, -222.5, -466.6, -664.6, -130.0]

# --- Canvas & Palette Setup (One Company, One Primary Hue) ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 9.5), dpi=300)
fig.patch.set_facecolor('#0b0f17')  # Deep Slate Navy

c_legn = '#10b981'        # Emerald 500 (Legend Biotech)
c_crsp = '#3b82f6'        # Royal Blue 500 (CRISPR Therapeutics)
c_legn_line = '#34d399'   # Emerald 400
c_crsp_line = '#60a5fa'   # Blue 400
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
# Subplot 1: 高流动性资金储备 (百万美元) vs 全稀释股本累计扩张幅度 (%)
# ==========================================
width = 0.35
rects1 = ax1.bar(x - width/2, legn_cash, width, label='LEGN 现金及定期存款储备 (百万美元)', color=c_legn, alpha=0.55)
rects2 = ax1.bar(x + width/2, crsp_cash, width, label='CRSP 现金及有价证券储备 (百万美元)', color=c_crsp, alpha=0.55)

ax1.set_ylabel('期末高流动性资金储备 (百万美元)', color=c_text, fontsize=12, fontweight='bold', labelpad=10)
ax1.set_xticks(x)
ax1.set_xticklabels(periods, fontsize=11, color=c_text)
ax1.set_ylim(0, 2900)

ax1_twin = ax1.twinx()
l1 = ax1_twin.plot(x, crsp_dil_growth, color=c_crsp_line, marker='s', linewidth=2.8, linestyle='--',
                   label='CRSP 全稀释总股本较2021年累计增幅 (%) [右轴]')
l2 = ax1_twin.plot(x, legn_dil_growth, color=c_legn_line, marker='o', linewidth=2.8,
                   label='LEGN 全稀释总股本较2021年累计增幅 (%) [右轴]')
ax1_twin.set_ylabel('全稀释总股本较 2021 年累计扩张幅度 (%)', color=c_text, fontsize=12, fontweight='bold', labelpad=10)
ax1_twin.tick_params(colors=c_muted, labelsize=11)
ax1_twin.set_ylim(-5, 46)
ax1_twin.grid(False)

for i, rect in enumerate(rects1):
    h = rect.get_height()
    y_off = 35 if i != 3 else -95
    va_mode = 'bottom' if i != 3 else 'top'
    ax1.annotate(f"{h:.0f}", (rect.get_x() + rect.get_width()/2, h + y_off),
                 ha='center', va=va_mode, color='#6ee7b7', fontsize=9.2, weight='bold')

for i, rect in enumerate(rects2):
    h = rect.get_height()
    ax1.annotate(f"{h:.0f}", (rect.get_x() + rect.get_width()/2, h + 35),
                 ha='center', va='bottom', color='#93c5fd', fontsize=9.2, weight='bold')

for i, txt in enumerate(crsp_dil_growth):
    if i == 0:
        ax1_twin.annotate(f"{txt:.1f}%", (x[i] - 0.16, txt - 2.8),
                          ha='center', color=c_crsp_line, fontsize=9.2, weight='bold')
    elif i in (1, 2, 3):
        ax1_twin.annotate(f"+{txt:.1f}%", (x[i] + 0.14, txt - 2.8),
                          ha='center', color=c_crsp_line, fontsize=9.2, weight='bold')
    elif i == 5:
        ax1_twin.annotate(f"+{txt:.1f}%", (x[i] - 0.20, txt + 1.4),
                          ha='center', color=c_crsp_line, fontsize=9.5, weight='bold')
    else:
        ax1_twin.annotate(f"+{txt:.1f}%", (x[i] - 0.12, txt + 1.5),
                          ha='center', color=c_crsp_line, fontsize=9.5, weight='bold')

for i, txt in enumerate(legn_dil_growth):
    if i == 0:
        continue
    elif i in (1, 2):
        ax1_twin.annotate(f"+{txt:.1f}%", (x[i] - 0.12, txt + 1.6),
                          ha='center', color=c_legn_line, fontsize=9.2, weight='bold')
    elif i == 3:
        ax1_twin.annotate(f"+{txt:.1f}%", (x[i] - 0.12, txt + 1.8),
                          ha='center', color=c_legn_line, fontsize=9.2, weight='bold')
    elif i == 4:
        ax1_twin.annotate(f"+{txt:.1f}%", (x[i] + 0.16, txt - 2.6),
                          ha='center', color=c_legn_line, fontsize=9.5, weight='bold')
    else:
        ax1_twin.annotate(f"+{txt:.1f}%", (x[i] + 0.14, txt - 2.8),
                          ha='center', color=c_legn_line, fontsize=9.5, weight='bold')

ax1.set_title('图 1：【指标 1 & 4】高流动性现金堡垒与全稀释股本扩张轨迹\nCRSP 坐拥 22.8 亿美元现金但转债+ATM 推升稀释 vs LEGN 迈入造血自给',
              fontsize=13.5, fontweight='bold', color=c_text, pad=16)

handles1, labels1 = ax1.get_legend_handles_labels()
handles2, labels2 = ax1_twin.get_legend_handles_labels()
ax1.legend(handles1 + handles2, labels1 + labels2, loc='upper left', ncol=1,
           facecolor=c_card, edgecolor='#334155', labelcolor=c_text, fontsize=9.0)

# ==========================================
# Subplot 2: 营业总收入 (百万美元) vs 营业利润/亏损 (百万美元)
# ==========================================
rects3 = ax2.bar(x - width/2, legn_rev, width, label='LEGN 营业总收入 (CARVYKTI 分成驱动, 百万美元)', color=c_legn, alpha=0.55)
rects4 = ax2.bar(x + width/2, crsp_rev, width, label='CRSP 营业总收入 (里程碑脉冲驱动, 百万美元)', color=c_crsp, alpha=0.55)

l3 = ax2.plot(x, legn_opinc, color=c_legn_line, marker='o', linewidth=3.0,
              label='LEGN 营业利润/亏损 (百万美元) [26Q3 达 +46.8M 历史转正]')
l4 = ax2.plot(x, crsp_opinc, color=c_crsp_line, marker='s', linewidth=2.8, linestyle='--',
              label='CRSP 营业利润/亏损 (百万美元) [含 CASGEVY 40% 亏损分摊]')

ax2.axhline(0, color='#64748b', linewidth=1.2, linestyle='-')
ax2.set_ylabel('金额 (百万美元)', color=c_text, fontsize=12, fontweight='bold', labelpad=10)
ax2.set_xticks(x)
ax2.set_xticklabels(periods, fontsize=11, color=c_text)
ax2.set_ylim(-820, 1280)

for i, rect in enumerate(rects3):
    h = rect.get_height()
    y_pos = h + 22 if i != 5 else h + 25
    ax2.annotate(f"{h:.1f}", (rect.get_x() + rect.get_width()/2, y_pos),
                 ha='center', va='bottom', color='#6ee7b7', fontsize=9.2, weight='bold')

for i, rect in enumerate(rects4):
    h = rect.get_height()
    if i == 5:
        ax2.annotate(f"{h:.1f}", (rect.get_x() + rect.get_width()/2 + 0.14, h + 18),
                     ha='center', va='bottom', color='#93c5fd', fontsize=9.2, weight='bold')
    else:
        ax2.annotate(f"{h:.1f}", (rect.get_x() + rect.get_width()/2, h + 22),
                     ha='center', va='bottom', color='#93c5fd', fontsize=9.2, weight='bold')

for i, val in enumerate(legn_opinc):
    if i == 0:
        ax2.annotate(f"{val:.1f}", (x[i] - 0.12, val - 55),
                     ha='center', color=c_legn_line, fontsize=9.2, weight='bold')
    elif i == 1:
        ax2.annotate(f"{val:.1f}", (x[i], val + 35),
                     ha='center', color=c_legn_line, fontsize=9.2, weight='bold')
    elif i == 2:
        ax2.annotate(f"{val:.1f}", (x[i], val - 58),
                     ha='center', color=c_legn_line, fontsize=9.2, weight='bold')
    elif i == 5:
        ax2.annotate(f"+{val:.1f}", (x[i] - 0.18, val + 38),
                     ha='center', color=c_legn_line, fontsize=10.0, weight='bold')
    else:
        ax2.annotate(f"{val:.1f}", (x[i], val + 32),
                     ha='center', color=c_legn_line, fontsize=9.2, weight='bold')

for i, val in enumerate(crsp_opinc):
    if i == 0:
        ax2.annotate(f"+{val:.1f}", (x[i] - 0.16, val + 28),
                     ha='center', color=c_crsp_line, fontsize=9.2, weight='bold')
    elif i == 2:
        ax2.annotate(f"{val:.1f}", (x[i] + 0.12, val + 32),
                     ha='center', color=c_crsp_line, fontsize=9.2, weight='bold')
    elif i == 5:
        ax2.annotate(f"{val:.1f}", (x[i] + 0.12, val - 60),
                     ha='center', color=c_crsp_line, fontsize=9.2, weight='bold')
    else:
        ax2.annotate(f"{val:.1f}", (x[i], val - 58),
                     ha='center', color=c_crsp_line, fontsize=9.2, weight='bold')

ax2.set_title('图 2：【指标 2 & 3】合作商业化放量 vs 里程碑脉冲与营业损益分野\nLEGN 2025 营收破 10 亿美元并于 26Q3 营业转正 vs CRSP 仍处商业化爬坡亏损期',
              fontsize=13.5, fontweight='bold', color=c_text, pad=16)

ax2.legend(loc='upper left', ncol=1,
           facecolor=c_card, edgecolor='#334155', labelcolor=c_text, fontsize=9.0)

plt.suptitle('早期创新药与临床 Biotech 财务对决：传奇生物 (LEGN) vs CRISPR (CRSP) (2021 ~ 2026 Q3 原生财报对账)',
             fontsize=15.5, fontweight='bold', color=c_text, y=0.98)

plt.tight_layout(rect=[0, 0.02, 1, 0.94])

out_dir = os.path.join(os.path.dirname(__file__), '..', 'assets')
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, 'legn_vs_crsp_metrics_trend.png')
plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor())
print(f"Saved chart to: {out_path}")
