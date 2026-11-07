import os
import matplotlib.pyplot as plt
import numpy as np

# Set font for macOS
plt.rcParams['font.sans-serif'] = ['PingFang SC', 'Heiti SC', 'Arial Unicode MS', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

periods = ['2021', '2022', '2023', '2024', '2025', '2026 Q3\n(单季)']
x = np.arange(len(periods))

# --- Data Series (统一单位：亿美元) ---
# 1. Gross Volume (亿美元，与正文原生底表 100% 一一对应)
uber_gb = [904.0, 1153.0, 1379.0, 1625.0, 1880.0, 598.2]
abnb_gbv = [469.0, 632.0, 733.0, 815.0, 900.0, 277.0]

# 2. Take Rate (%)
uber_tr = [19.3, 27.6, 27.0, 27.0, 27.4, 24.7]
abnb_tr = [12.8, 13.3, 13.5, 13.6, 13.9, 17.6]

# 3. Free Cash Flow (亿美元)
uber_fcf = [-7.4, 3.9, 33.6, 53.0, 68.0, 25.4]
abnb_fcf = [21.6, 34.3, 38.4, 41.0, 47.0, 14.3]

# 4. Airbnb Customer Float (亿美元)
abnb_float = [36.0, 48.0, 61.0, 68.0, 75.0, 74.2]

# --- Canvas & Palette Setup ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 9), dpi=300)
fig.patch.set_facecolor('#0b0f17')  # Deep Slate Navy

c_uber = '#06b6d4'        # Cyan 500 (Uber)
c_uber_sub = '#0891b2'    # Cyan 600
c_abnb = '#f43f5e'        # Rose 500 (Airbnb)
c_abnb_sub = '#e11d48'    # Rose 600
c_float = '#f59e0b'       # Amber 500 (Float)
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
# Subplot 1: 交易总额 (GMV/GB) 与 变现抽成率 (Take Rate)
# ==========================================
width = 0.35
rects1 = ax1.bar(x - width/2, uber_gb, width, label='Uber 平台总预订额 (GB, 亿美元)', color=c_uber, alpha=0.85)
rects2 = ax1.bar(x + width/2, abnb_gbv, width, label='Airbnb 预订总价值 (GBV, 亿美元)', color=c_abnb, alpha=0.85)

ax1.set_ylabel('交易总流水 (亿美元)', color=c_text, fontsize=12, fontweight='bold', labelpad=10)
ax1.set_xticks(x)
ax1.set_xticklabels(periods, fontsize=11, color=c_text)
ax1.set_ylim(0, 2250)

# Secondary axis for Take Rate
ax1_twin = ax1.twinx()
line1 = ax1_twin.plot(x, uber_tr, color='#38bdf8', marker='o', linewidth=2.8, label='Uber 综合抽成率 (%) [右轴]')
line2 = ax1_twin.plot(x, abnb_tr, color='#fb7185', marker='s', linewidth=2.8, linestyle='--', label='Airbnb 综合变现率 (%) [右轴]')
ax1_twin.set_ylabel('综合抽成率 / 变现率 (%)', color=c_text, fontsize=12, fontweight='bold', labelpad=10)
ax1_twin.tick_params(colors=c_muted, labelsize=11)
ax1_twin.set_ylim(8, 35)
ax1_twin.grid(False)

# Data labels on bars
for rect in rects1:
    h = rect.get_height()
    label_txt = f"{h:.1f}" if h == 598.2 else f"{h:.0f}"
    ax1.annotate(label_txt, (rect.get_x() + rect.get_width()/2, h + 30),
                 ha='center', va='bottom', color=c_uber, fontsize=10, weight='bold')
for rect in rects2:
    h = rect.get_height()
    label_txt = f"{h:.1f}" if h == 277.0 else f"{h:.0f}"
    ax1.annotate(label_txt, (rect.get_x() + rect.get_width()/2, h + 30),
                 ha='center', va='bottom', color=c_abnb, fontsize=10, weight='bold')

# Data labels on lines
for i, txt in enumerate(uber_tr):
    ax1_twin.annotate(f"{txt:.1f}%", (x[i], uber_tr[i] + 0.9),
                      ha='center', color='#38bdf8', fontsize=10, weight='bold')
for i, txt in enumerate(abnb_tr):
    offset = 1.0 if i == 5 else -1.5
    ax1_twin.annotate(f"{txt:.1f}%", (x[i], abnb_tr[i] + offset),
                      ha='center', color='#fb7185', fontsize=10, weight='bold')

ax1.set_title('图 1：平台交易总盘 vs 变现抽成率 (2021 ~ 2026 Q3)\n本地双飞轮高抽成 vs 跨国轻资产极品变现',
              fontsize=14, fontweight='bold', color=c_text, pad=16)

# Combine legends
handles1, labels1 = ax1.get_legend_handles_labels()
handles2, labels2 = ax1_twin.get_legend_handles_labels()
ax1.legend(handles1 + handles2, labels1 + labels2, loc='upper left',
           facecolor=c_card, edgecolor='#334155', labelcolor=c_text, fontsize=9.5)

# ==========================================
# Subplot 2: 自由现金流 (FCF) 造血质变 vs Airbnb 免息客户浮存金 (Float)
# ==========================================
rects3 = ax2.bar(x - width/2, uber_fcf, width, label='Uber 自由现金流 (FCF, 亿美元)', color=c_uber, alpha=0.85)
rects4 = ax2.bar(x + width/2, abnb_fcf, width, label='Airbnb 自由现金流 (FCF, 亿美元)', color=c_abnb, alpha=0.85)

ax2.set_ylabel('自由现金流 (亿美元)', color=c_text, fontsize=12, fontweight='bold', labelpad=10)
ax2.set_xticks(x)
ax2.set_xticklabels(periods, fontsize=11, color=c_text)
ax2.set_ylim(-15, 85)
ax2.axhline(0, color='#64748b', linestyle='-', linewidth=1.2, alpha=0.7)

# Secondary axis for Airbnb Float
ax2_twin = ax2.twinx()
line3 = ax2_twin.plot(x, abnb_float, color=c_float, marker='^', linewidth=3, linestyle='-.',
                      label='Airbnb 客户预付免息浮存金 (Float, 亿美元) [右轴]')
ax2_twin.set_ylabel('Airbnb 客户未结预付浮存金 (亿美元)', color=c_float, fontsize=12, fontweight='bold', labelpad=10)
ax2_twin.tick_params(colors=c_float, labelsize=11)
ax2_twin.set_ylim(20, 140)
ax2_twin.grid(False)

# Data labels on bars
for rect in rects3:
    h = rect.get_height()
    offset = 2 if h >= 0 else -6
    ax2.annotate(f"{h:.1f}", (rect.get_x() + rect.get_width()/2, h + offset),
                 ha='center', va='bottom', color=c_uber, fontsize=10, weight='bold')
for rect in rects4:
    h = rect.get_height()
    ax2.annotate(f"{h:.1f}", (rect.get_x() + rect.get_width()/2, h + 2),
                 ha='center', va='bottom', color=c_abnb, fontsize=10, weight='bold')

# Data labels on Float line
for i, txt in enumerate(abnb_float):
    ax2_twin.annotate(f"{txt:.1f}", (x[i], abnb_float[i] + 3.5),
                      ha='center', color=c_float, fontsize=10, weight='bold')

ax2.set_title('图 2：自由现金流 (FCF) 造血质变 vs Airbnb 百亿免息浮存金\n从现金流焚尸炉到年造血百亿 vs 天生高 FCF 转化加持巨额利息',
              fontsize=14, fontweight='bold', color=c_text, pad=16)

# Combine legends
handles3, labels3 = ax2.get_legend_handles_labels()
handles4, labels4 = ax2_twin.get_legend_handles_labels()
ax2.legend(handles3 + handles4, labels3 + labels4, loc='upper left',
           facecolor=c_card, edgecolor='#334155', labelcolor=c_text, fontsize=9.5)

plt.tight_layout(pad=3.0)

output_path = 'articles/industry_metrics_guide/assets/uber_vs_abnb_metrics_trend.png'
plt.savefig(output_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
print(f"Chart successfully saved to {output_path}")
