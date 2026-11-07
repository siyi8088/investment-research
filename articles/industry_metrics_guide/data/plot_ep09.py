import os
import matplotlib.pyplot as plt
import numpy as np

# Set font for macOS
plt.rcParams['font.sans-serif'] = ['PingFang SC', 'Heiti SC', 'Arial Unicode MS', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

periods = ['2021', '2022', '2023', '2024', '2025', '2026 Q3\n(单季)']
x = np.arange(len(periods))

# --- Data Series (100% SEC 10-K / 20-F & Q3 2026 10-Q / 6-K Ground Truth) ---
# 1. 核心 GLP-1 专营权收入 (折合亿美元: LLY Tirzepatide vs NVO Semaglutide)
lly_fran_usd = [0.0, 4.8, 53.4, 164.7, 365.1, 160.8]
nvo_fran_usd = [63.2, 109.1, 211.6, 293.0, 344.8, 93.7]  # 对应 397.4 / 772.4 / 1458.1 / 2018.5 / 2282.9 / 604.5 亿 DKK

# 2. 核心专营权占总营收集中度 (%)
lly_conc = [0.0, 1.7, 15.6, 36.6, 56.0, 65.9]
nvo_conc = [28.2, 43.6, 62.8, 69.5, 73.9, 76.3]

# 3. 销售及行政管理费用率 (SG&A %)
lly_sga = [22.7, 22.6, 21.7, 19.1, 17.0, 12.8]
nvo_sga = [29.2, 28.6, 26.5, 23.2, 22.7, 20.5]

# 4. GAAP 报告营业利润率 (%)
lly_opm = [22.4, 25.0, 18.9, 28.6, 40.4, 35.3]  # Q3 2026 含 41.8 亿美元 Acquired IPR&D，剔除后核心利润率达 53.7%
nvo_opm = [41.6, 42.3, 44.2, 44.2, 41.3, 29.1]  # Q3 2026 含 87.1 亿 DKK 管线与产线减值，剔除后调整后利润率 40.1%

# --- Canvas & Palette Setup ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 9.5), dpi=300)
fig.patch.set_facecolor('#0b0f17')  # Deep Slate Navy

c_lly = '#ef4444'         # Crimson Red (Eli Lilly)
c_nvo = '#3b82f6'         # Royal Blue (Novo Nordisk)
c_lly_line = '#f87171'    # Light Red
c_nvo_line = '#60a5fa'    # Light Blue
c_sga_lly = '#fbbf24'     # Amber 400
c_sga_nvo = '#34d399'     # Emerald 400
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
# Subplot 1: 核心大单品专营权规模 (亿美元) vs 专营权集中度 (%)
# ==========================================
width = 0.35
rects1 = ax1.bar(x - width/2, lly_fran_usd, width, label='LLY 替尔泊肽专营权收入 (亿美元)', color=c_lly, alpha=0.55)
rects2 = ax1.bar(x + width/2, nvo_fran_usd, width, label='NVO 司美格鲁肽专营权收入 (折合亿美元)', color=c_nvo, alpha=0.55)

ax1.set_ylabel('核心专营权净销售额 (亿美元)', color=c_text, fontsize=12, fontweight='bold', labelpad=10)
ax1.set_xticks(x)
ax1.set_xticklabels(periods, fontsize=11, color=c_text)
ax1.set_ylim(0, 520)

ax1_twin = ax1.twinx()
l1 = ax1_twin.plot(x, nvo_conc, color=c_nvo_line, marker='s', linewidth=2.8, label='NVO 司美格鲁肽占总营收比重 (%) [右轴]')
l2 = ax1_twin.plot(x, lly_conc, color=c_lly_line, marker='o', linewidth=2.8, label='LLY 替尔泊肽占总营收比重 (%) [右轴]')
ax1_twin.set_ylabel('核心专营权占总营收集中度 (%)', color=c_text, fontsize=12, fontweight='bold', labelpad=10)
ax1_twin.tick_params(colors=c_muted, labelsize=11)
ax1_twin.set_ylim(0, 95)
ax1_twin.grid(False)

for i, rect in enumerate(rects1):
    h = rect.get_height()
    if h > 0:
        x_pos = rect.get_x() + rect.get_width()/2
        if i == 1:
            ax1.annotate(f"{h:.1f}", (x_pos - 0.08, h + 10),
                         ha='center', va='bottom', color='#fca5a5', fontsize=9.2, weight='bold')
        elif i in (2, 3):
            ax1.annotate(f"{h:.1f}", (x_pos, h - 22),
                         ha='center', va='top', color='#fecaca', fontsize=9.2, weight='bold')
        else:
            ax1.annotate(f"{h:.1f}", (x_pos, h + 6),
                         ha='center', va='bottom', color='#fca5a5', fontsize=9.5, weight='bold')
for i, rect in enumerate(rects2):
    h = rect.get_height()
    ax1.annotate(f"{h:.1f}", (rect.get_x() + rect.get_width()/2, h + 6),
                 ha='center', va='bottom', color='#93c5fd', fontsize=9.5, weight='bold')

for i, txt in enumerate(nvo_conc):
    ax1_twin.annotate(f"{txt:.1f}%", (x[i], nvo_conc[i] + 2.4),
                      ha='center', color=c_nvo_line, fontsize=9.5, weight='bold')
for i, txt in enumerate(lly_conc):
    if i == 0:
        ax1_twin.annotate(f"{txt:.1f}%", (x[i] - 0.15, lly_conc[i] + 2.2),
                          ha='center', color=c_lly_line, fontsize=9.2, weight='bold')
    elif i == 1:
        ax1_twin.annotate(f"{txt:.1f}%", (x[i] + 0.14, lly_conc[i] + 2.5),
                          ha='center', color=c_lly_line, fontsize=9.2, weight='bold')
    elif i in (2, 3):
        ax1_twin.annotate(f"{txt:.1f}%", (x[i] - 0.14, lly_conc[i] + 3.0),
                          ha='center', color=c_lly_line, fontsize=9.5, weight='bold')
    else:
        ax1_twin.annotate(f"{txt:.1f}%", (x[i], lly_conc[i] - 4.5),
                          ha='center', color=c_lly_line, fontsize=9.5, weight='bold')

ax1.set_title('图 1：【指标 1】核心大单品爆发与专营权集中度演变\nLLY 替尔泊肽 2025 达 365 亿美元反超 vs NVO 单分子依赖度升至 76.3%',
              fontsize=13.5, fontweight='bold', color=c_text, pad=16)

handles1, labels1 = ax1.get_legend_handles_labels()
handles2, labels2 = ax1_twin.get_legend_handles_labels()
ax1.legend(handles1 + handles2, labels1 + labels2, loc='upper left', ncol=1,
           facecolor=c_card, edgecolor='#334155', labelcolor=c_text, fontsize=9.0)

# ==========================================
# Subplot 2: 销售管理费用率 (SG&A %) 摊薄 vs GAAP 营业利润率 (%)
# ==========================================
l3 = ax2.plot(x, lly_sga, color=c_sga_lly, marker='^', linewidth=2.6, linestyle='--', label='LLY 销售及行政费用率 (SG&A %)')
l4 = ax2.plot(x, nvo_sga, color=c_sga_nvo, marker='d', linewidth=2.6, linestyle='--', label='NVO 销售及行政费用率 (SG&A %)')
l5 = ax2.plot(x, lly_opm, color=c_lly_line, marker='o', linewidth=3.0, label='LLY GAAP 营业利润率 (%) [26Q3 剔除 IPR&D 达 53.7%]')
l6 = ax2.plot(x, nvo_opm, color=c_nvo_line, marker='s', linewidth=3.0, label='NVO 报告营业利润率 (%) [26Q3 受 87 亿 DKK 减值拖累]')

ax2.set_ylabel('占营业总收入比重 (%)', color=c_text, fontsize=12, fontweight='bold', labelpad=10)
ax2.set_xticks(x)
ax2.set_xticklabels(periods, fontsize=11, color=c_text)
ax2.set_ylim(5, 58)

for i, txt in enumerate(lly_sga):
    if i == 0:
        ax2.annotate(f"{txt:.1f}%", (x[i] + 0.16, lly_sga[i] + 1.5),
                     ha='center', color=c_sga_lly, fontsize=9.5, weight='bold')
    elif i == 2:
        ax2.annotate(f"{txt:.1f}%", (x[i] + 0.18, lly_sga[i] + 1.2),
                     ha='center', color=c_sga_lly, fontsize=9.5, weight='bold')
    else:
        ax2.annotate(f"{txt:.1f}%", (x[i], lly_sga[i] - 2.5),
                     ha='center', color=c_sga_lly, fontsize=9.5, weight='bold')

for i, txt in enumerate(nvo_sga):
    y_off = 1.6 if i != 5 else -2.5
    ax2.annotate(f"{txt:.1f}%", (x[i], nvo_sga[i] + y_off),
                 ha='center', color=c_sga_nvo, fontsize=9.5, weight='bold')

for i, txt in enumerate(lly_opm):
    if i == 0:
        ax2.annotate(f"{txt:.1f}%", (x[i] - 0.10, lly_opm[i] - 2.6),
                     ha='center', color=c_lly_line, fontsize=9.5, weight='bold')
    elif i == 1:
        ax2.annotate(f"{txt:.1f}%", (x[i], lly_opm[i] + 1.6),
                     ha='center', color=c_lly_line, fontsize=9.5, weight='bold')
    elif i == 2:
        ax2.annotate(f"{txt:.1f}%", (x[i], lly_opm[i] - 2.6),
                     ha='center', color=c_lly_line, fontsize=9.5, weight='bold')
    elif i == 4:
        ax2.annotate(f"{txt:.1f}%", (x[i] - 0.18, lly_opm[i] - 2.6),
                     ha='center', color=c_lly_line, fontsize=9.5, weight='bold')
    else:
        ax2.annotate(f"{txt:.1f}%", (x[i], lly_opm[i] + 1.8),
                     ha='center', color=c_lly_line, fontsize=9.5, weight='bold')

for i, txt in enumerate(nvo_opm):
    if i == 4:
        ax2.annotate(f"{txt:.1f}%", (x[i] + 0.14, nvo_opm[i] + 1.8),
                     ha='center', color=c_nvo_line, fontsize=9.5, weight='bold')
    elif i == 5:
        ax2.annotate(f"{txt:.1f}%", (x[i], nvo_opm[i] - 2.6),
                     ha='center', color=c_nvo_line, fontsize=9.5, weight='bold')
    else:
        ax2.annotate(f"{txt:.1f}%", (x[i], nvo_opm[i] + 1.8),
                     ha='center', color=c_nvo_line, fontsize=9.5, weight='bold')

ax2.set_title('图 2：【指标 3 & 4】SG&A 规模效应摊薄与 GAAP 营业利润率交锋\nLLY SG&A 摊薄至 12.8% 驱动利润率跃升 vs NVO 26Q3 计提大额减值回落',
              fontsize=13.5, fontweight='bold', color=c_text, pad=16)

ax2.legend(loc='upper left', ncol=1,
           facecolor=c_card, edgecolor='#334155', labelcolor=c_text, fontsize=9.0)

plt.suptitle('跨国大药企双雄财务对决：礼来 (LLY) vs 诺和诺德 (NVO) (2021 ~ 2026 Q3 原生财报对账)',
             fontsize=16, fontweight='bold', color=c_text, y=0.98)

plt.tight_layout(rect=[0, 0.02, 1, 0.94])

out_dir = os.path.join(os.path.dirname(__file__), '..', 'assets')
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, 'lly_vs_nvo_metrics_trend.png')
plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor())
print(f"Saved chart to: {out_path}")
