import os
import matplotlib.pyplot as plt
import numpy as np

# Set font for macOS
plt.rcParams['font.sans-serif'] = ['PingFang SC', 'Heiti SC', 'Arial Unicode MS', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

periods = ['2021', '2022', '2023', '2024', '2025', '2026\n(最新期)']
x = np.arange(len(periods))

# --- Data Series (100% SEC DEF 14A / 10-K / 10-Q / 8-K Ground Truth) ---
# Panel 1: Meta Control Wedge & Shareholder Proposal Voting Gap (%)
meta_econ_stake = [13.6, 13.6, 13.5, 13.4, 13.5, 13.4]
meta_vote_power = [57.7, 60.1, 61.1, 61.0, 61.0, 60.8]
outside_for_rate = [81.0, 82.5, 82.0, 81.8, 82.3, 82.3]
reported_for_rate = [27.5, 28.2, 27.8, 26.4, 25.8, 25.8]

# Panel 2: Capital Allocation Divergence (Shareholder Return = Buybacks + Dividends, 亿美元; CapEx / CFO %)
aapl_total_return = [1004.4, 1042.4, 925.8, 1101.8, 1061.3, 1021.1]  # AAPL Buybacks + Dividends (亿美元)
meta_total_return = [445.4, 279.6, 200.3, 348.2, 315.8, 40.6]        # META Buybacks + Dividends (2026前9月0回购+40.6亿分红)
aapl_capex_cfo = [10.7, 8.8, 9.9, 8.0, 11.4, 6.2]                    # AAPL CapEx / CFO (%)
meta_capex_cfo = [32.2, 62.3, 38.3, 40.8, 60.2, 87.9]                # META CapEx / CFO (%) (2026前9月 830.6 / 945.2 = 87.9%, Q3单季 103.5%)

# --- Canvas & Palette Setup ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 9.5), dpi=300)
fig.patch.set_facecolor('#0b0f17')

c_meta_vote = '#f59e0b'   # Amber 500
c_meta_econ = '#06b6d4'   # Cyan 500
c_out_line = '#34d399'    # Emerald 400
c_rep_line = '#f87171'    # Red 400
c_aapl = '#38bdf8'        # Sky 400
c_text = '#f8fafc'
c_muted = '#94a3b8'
c_grid = '#1e293b'
c_card = '#111827'

for ax in (ax1, ax2):
    ax.set_facecolor(c_card)
    ax.tick_params(colors=c_muted, labelsize=11)
    ax.grid(True, linestyle='--', alpha=0.35, color=c_grid)
    for spine in ax.spines.values():
        spine.set_color('#334155')

# ==========================================
# Subplot 1: 控制权与现金流权分离度 (Wedge) vs 同股同权提案投票鸿沟
# ==========================================
width = 0.35
rects1 = ax1.bar(x - width/2, meta_econ_stake, width, label='META 扎克伯格经济权益占比 (%)', color=c_meta_econ, alpha=0.65)
rects2 = ax1.bar(x + width/2, meta_vote_power, width, label='META 扎克伯格总投票权占比 (%) [10票/股]', color=c_meta_vote, alpha=0.65)

ax1.axhline(50.0, color='#fbbf24', linestyle='-.', linewidth=1.5, alpha=0.6, label='50% 绝对控制权法定红线 (Controlled Company)')
ax1.plot(x, outside_for_rate, color=c_out_line, marker='o', linewidth=2.8, label='同股同权提案：外部独立股东真实赞成率 (%)')
ax1.plot(x, reported_for_rate, color=c_rep_line, marker='s', linewidth=2.8, linestyle='--', label='同股同权提案：计入B类股后账面总赞成率 (%)')

ax1.set_ylabel('股权、投票权与股东大会提案赞成率 (%)', color=c_text, fontsize=12, fontweight='bold', labelpad=10)
ax1.set_xticks(x)
ax1.set_xticklabels(periods, fontsize=11, color=c_text)
ax1.set_ylim(0, 105)

for rect in rects1:
    h = rect.get_height()
    ax1.annotate(f"{h:.1f}%", (rect.get_x() + rect.get_width()/2, h + 1.5),
                 ha='center', va='bottom', color='#67e8f9', fontsize=9.5, weight='bold')
for rect in rects2:
    h = rect.get_height()
    ax1.annotate(f"{h:.1f}%", (rect.get_x() + rect.get_width()/2, h + 1.5),
                 ha='center', va='bottom', color='#fde68a', fontsize=9.5, weight='bold')

for i, txt in enumerate(outside_for_rate):
    ax1.annotate(f"{txt:.1f}%", (x[i], outside_for_rate[i] + 2.2),
                 ha='center', color=c_out_line, fontsize=9.5, weight='bold')
for i, txt in enumerate(reported_for_rate):
    ax1.annotate(f"{txt:.1f}%", (x[i], reported_for_rate[i] - 4.8),
                 ha='center', color=c_rep_line, fontsize=9.5, weight='bold')

ax1.set_title('图 1：META 双层股权楔子 (+47.4pct) 与外部股东否决权失灵实证\n13.4% 经济持股锁定 60.8% 投票权，外部股东 82% 赞成同股同权仍遭一票否决',
              fontsize=13.0, fontweight='bold', color=c_text, pad=16)

ax1.legend(loc='upper right', ncol=1, facecolor=c_card, edgecolor='#334155', labelcolor=c_text, fontsize=9.0)

# ==========================================
# Subplot 2: 股东现金回馈总额 (回购+分红) vs 资本开支消耗经营现金流比重 (CapEx / CFO %)
# ==========================================
rects3 = ax2.bar(x - width/2, aapl_total_return, width, label='AAPL 股东现金回馈总额：回购+分红 (亿美元)', color=c_aapl, alpha=0.55)
rects4 = ax2.bar(x + width/2, meta_total_return, width, label='META 股东现金回馈总额：回购+分红 (亿美元)', color=c_meta_vote, alpha=0.55)

ax2.set_ylabel('年度股东现金回馈总额：回购＋分红 (亿美元)', color=c_text, fontsize=12, fontweight='bold', labelpad=10)
ax2.set_xticks(x)
ax2.set_xticklabels(periods, fontsize=11, color=c_text)
ax2.set_ylim(0, 1450)

ax2_twin = ax2.twinx()
l1 = ax2_twin.plot(x, meta_capex_cfo, color='#f43f5e', marker='s', linewidth=2.8, label='META 资本开支占经营现金流比重 (CapEx/CFO %) [右轴]')
l2 = ax2_twin.plot(x, aapl_capex_cfo, color='#34d399', marker='o', linewidth=2.8, linestyle='--', label='AAPL 资本开支占经营现金流比重 (CapEx/CFO %) [右轴]')
ax2_twin.set_ylabel('资本开支占经营活动现金流比重 (CapEx / CFO %)', color=c_text, fontsize=12, fontweight='bold', labelpad=10)
ax2_twin.tick_params(colors=c_muted, labelsize=11)
ax2_twin.set_ylim(0, 115)
ax2_twin.grid(False)

for rect in rects3:
    h = rect.get_height()
    ax2.annotate(f"{h:.0f}", (rect.get_x() + rect.get_width()/2, h + 18),
                 ha='center', va='bottom', color='#7dd3fc', fontsize=9.5, weight='bold')
for rect in rects4:
    h = rect.get_height()
    ax2.annotate(f"{h:.1f}" if h < 100 else f"{h:.0f}", (rect.get_x() + rect.get_width()/2, h + 18),
                 ha='center', va='bottom', color='#fde68a', fontsize=9.5, weight='bold')

for i, txt in enumerate(meta_capex_cfo):
    ax2_twin.annotate(f"{txt:.1f}%", (x[i], meta_capex_cfo[i] + 3.0),
                      ha='center', color='#fb7185', fontsize=9.5, weight='bold')
for i, txt in enumerate(aapl_capex_cfo):
    ax2_twin.annotate(f"{txt:.1f}%", (x[i], aapl_capex_cfo[i] + 2.5),
                      ha='center', color='#34d399', fontsize=9.5, weight='bold')

ax2.set_title('图 2：控制权结构对资本配置与股东回馈的刚性映射 (2021~2026)\nAAPL 同股同权年均回馈千亿美元 vs META 创始人独断豪赌 AI 算力致 2026 停购',
              fontsize=13.0, fontweight='bold', color=c_text, pad=16)

handles1, labels1 = ax2.get_legend_handles_labels()
handles2, labels2 = ax2_twin.get_legend_handles_labels()
ax2.legend(handles1 + handles2, labels1 + labels2, loc='upper left', ncol=1,
           facecolor=c_card, edgecolor='#334155', labelcolor=c_text, fontsize=8.8)

plt.tight_layout(pad=2.0)
out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets')
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, 'meta_vs_aapl_control_trend.png')
plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
print(f"Saved chart to: {out_path}")

