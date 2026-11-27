import os
import matplotlib.pyplot as plt
import numpy as np

# Set font for macOS
plt.rcParams['font.sans-serif'] = ['PingFang SC', 'Heiti SC', 'Arial Unicode MS', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

periods = ['FY22', 'FY23', 'FY24', 'FY25', 'FY26', 'FY27\n(最新单季)']
x = np.arange(len(periods))

# --- Data Series (100% SEC DEF 14A / 10-K / 10-Q / 8-K Ground Truth) ---
# Panel 1: NVDA Operating Profit & Shareholder Return vs Governance Milestones
nvda_op_inc = [100.4, 42.2, 329.7, 814.5, 1303.9, 775.2]        # GAAP 营业利润 (亿美元, FY27为Q3单季)
nvda_cap_ret = [4.0, 104.4, 99.3, 345.4, 410.6, 281.0]          # 回购+分红 (亿美元, FY27为Q3单季)
nvda_gaap_opm = [37.3, 15.7, 54.1, 62.4, 60.4, 66.9]            # GAAP 营业利润率 (%)
nvda_sbc_pct = [7.4, 10.0, 5.8, 3.6, 3.0, 1.8]                  # SBC 占营收比重 (%)

# Panel 2: CRM Activist Intervention (2023) -> Margin & Capital Return Transformation
crm_fcf = [53.0, 63.1, 95.0, 118.0, 144.0, 11.0]                # 自由现金流 FCF (亿美元, FY27为Q2淡季单季)
crm_cap_ret = [0.0, 40.0, 77.0, 93.0, 143.0, 38.6]              # 回购+分红 (亿美元, FY27Q2含ASR推进与3.64亿分红)
crm_gaap_opm = [2.1, 3.3, 14.4, 19.0, 20.1, 20.5]               # GAAP 营业利润率 (%)
crm_nongaap_opm = [18.7, 22.5, 30.5, 32.8, 34.1, 34.1]          # Non-GAAP 营业利润率 (%)
crm_sbc_pct = [10.3, 10.5, 8.5, 7.4, 8.4, 8.0]                  # SBC 占营收比重 (%)

# --- Canvas & Palette Setup ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 9.5), dpi=300)
fig.patch.set_facecolor('#0b0f17')

c_nvda = '#10b981'        # Emerald 500
c_nvda_ret = '#06b6d4'    # Cyan 500
c_crm_fcf = '#38bdf8'     # Sky 400
c_crm_ret = '#f59e0b'     # Amber 500
c_line_1 = '#fbbf24'      # Amber 400
c_line_2 = '#34d399'      # Emerald 400
c_line_sbc = '#f87171'    # Red 400
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
# Subplot 1: NVDA 经营造血与关键人制度护栏重构
# ==========================================
width = 0.35
rects1 = ax1.bar(x - width/2, nvda_op_inc, width, label='NVDA GAAP 营业利润 (亿美元)', color=c_nvda, alpha=0.55)
rects2 = ax1.bar(x + width/2, nvda_cap_ret, width, label='NVDA 股东现金回馈：回购+分红 (亿美元)', color=c_nvda_ret, alpha=0.65)

ax1.set_ylabel('营业利润与股东现金回馈 (亿美元)', color=c_text, fontsize=12, fontweight='bold', labelpad=10)
ax1.set_xticks(x)
ax1.set_xticklabels(periods, fontsize=11, color=c_text)
ax1.set_ylim(0, 1880)

ax1_twin = ax1.twinx()
l1 = ax1_twin.plot(x, nvda_gaap_opm, color=c_line_1, marker='o', linewidth=2.8, label='NVDA GAAP 营业利润率 (%) [右轴]')
l2 = ax1_twin.plot(x, nvda_sbc_pct, color=c_line_sbc, marker='s', linewidth=2.4, linestyle='--', label='NVDA 股权激励 SBC 占营收比重 (%) [右轴]')
ax1_twin.set_ylabel('利润率与股权激励占比 (%)', color=c_text, fontsize=12, fontweight='bold', labelpad=10)
ax1_twin.tick_params(colors=c_muted, labelsize=11)
ax1_twin.set_ylim(0, 92)
ax1_twin.grid(False)

for rect in rects1:
    h = rect.get_height()
    ax1.annotate(f"{h:.1f}" if h < 200 else f"{h:.0f}", (rect.get_x() + rect.get_width()/2, h + 20),
                 ha='center', va='bottom', color='#6ee7b7', fontsize=9.2, weight='bold')
for i, rect in enumerate(rects2):
    h = rect.get_height()
    y_off = 55 if i == 2 else 20
    ax1.annotate(f"{h:.1f}" if h < 100 else f"{h:.0f}", (rect.get_x() + rect.get_width()/2, h + y_off),
                 ha='center', va='bottom', color='#67e8f9', fontsize=9.2, weight='bold')

for i, txt in enumerate(nvda_gaap_opm):
    x_shift = 0.24 if i == 1 else (-0.18 if i == 2 else 0.0)
    y_delta = 1.8 if i == 1 else 2.5
    ax1_twin.annotate(f"{txt:.1f}%", (x[i] + x_shift, nvda_gaap_opm[i] + y_delta),
                      ha='center', color=c_line_1, fontsize=9.5, weight='bold')
for i, txt in enumerate(nvda_sbc_pct):
    y_delta = -3.6 if i == 2 else 2.2
    ax1_twin.annotate(f"{txt:.1f}%", (x[i], nvda_sbc_pct[i] + y_delta),
                      ha='center', color=c_line_sbc, fontsize=9.0, weight='bold')

# Milestone callout box on Panel 1 (cleanly in upper-right empty space above bars)
ax1.annotate('2026 治理双节点:\n• 6月: 86.8% 选票强拆超多数决\n• 11月: 11天换帅复职 → 首设独立董事长\n  +全独董国安专委会+CCO越级汇报',
             xy=(5.0, 840), xytext=(2.15, 1540),
             arrowprops=dict(arrowstyle='->', color='#fbbf24', lw=1.8, connectionstyle='arc3,rad=-0.18'),
             bbox=dict(boxstyle='round,pad=0.5', facecolor='#1e293b', edgecolor='#fbbf24', alpha=0.95),
             fontsize=9.2, color='#fde68a', weight='bold')

ax1.set_title('图 1：英伟达 (NVDA) 3.58% 创始人选票 vs 万亿关键人效应与护栏重构\n66.9% 营业利润率印钞机下，“留住灵魂统帅 + 焊死三道独立护栏”的制度均衡',
              fontsize=12.8, fontweight='bold', color=c_text, pad=16)

handles1, labels1 = ax1.get_legend_handles_labels()
handles2, labels2 = ax1_twin.get_legend_handles_labels()
ax1.legend(handles1 + handles2, labels1 + labels2, loc='upper left', ncol=1,
           facecolor=c_card, edgecolor='#334155', labelcolor=c_text, fontsize=8.8)

# ==========================================
# Subplot 2: CRM 外部 13D 激进基金围猎与解散并购委员会后的十倍利润率跃升
# ==========================================
rects3 = ax2.bar(x - width/2, crm_fcf, width, label='CRM 自由现金流 FCF (亿美元)', color=c_crm_fcf, alpha=0.55)
rects4 = ax2.bar(x + width/2, crm_cap_ret, width, label='CRM 股东现金回馈：回购+分红 (亿美元)', color=c_crm_ret, alpha=0.65)

ax2.axvline(1.5, color='#fbbf24', linestyle='-.', linewidth=1.8, alpha=0.75)
ax2.annotate('2023年初 五大激进基金围猎:\n• ValueAct掌门进董事会任薪酬主席\n• 正式解散董事会“并购委员会”\n• 裁员控费 + 开启百亿回购与分红',
             xy=(1.5, 165), xytext=(1.82, 162),
             arrowprops=dict(arrowstyle='->', color='#fbbf24', lw=1.8),
             bbox=dict(boxstyle='round,pad=0.5', facecolor='#1e293b', edgecolor='#fbbf24', alpha=0.95),
             fontsize=9.2, color='#fde68a', weight='bold')

ax2.set_ylabel('自由现金流与股东现金回馈 (亿美元)', color=c_text, fontsize=12, fontweight='bold', labelpad=10)
ax2.set_xticks(x)
ax2.set_xticklabels(periods, fontsize=11, color=c_text)
ax2.set_ylim(0, 215)

ax2_twin = ax2.twinx()
l3 = ax2_twin.plot(x, crm_nongaap_opm, color='#38bdf8', marker='^', linewidth=2.6, linestyle='--', label='CRM Non-GAAP 营业利润率 (%) [右轴]')
l4 = ax2_twin.plot(x, crm_gaap_opm, color=c_line_2, marker='o', linewidth=3.0, label='CRM GAAP 真实营业利润率 (%) [右轴]')
l5 = ax2_twin.plot(x, crm_sbc_pct, color=c_line_sbc, marker='d', linewidth=2.2, linestyle=':', label='CRM 股权激励 SBC 占营收比重 (%) [右轴]')
ax2_twin.set_ylabel('营业利润率与股权激励占比 (%)', color=c_text, fontsize=12, fontweight='bold', labelpad=10)
ax2_twin.tick_params(colors=c_muted, labelsize=11)
ax2_twin.set_ylim(0, 48)
ax2_twin.grid(False)

for rect in rects3:
    h = rect.get_height()
    ax2.annotate(f"{h:.1f}", (rect.get_x() + rect.get_width()/2, h + 2.5),
                 ha='center', va='bottom', color='#7dd3fc', fontsize=9.2, weight='bold')
for i, rect in enumerate(rects4):
    h = rect.get_height()
    y_pos = h + 11.0 if i == 1 else h + 2.5
    ax2.annotate(f"{h:.1f}", (rect.get_x() + rect.get_width()/2, y_pos),
                 ha='center', va='bottom', color='#fde68a', fontsize=9.2, weight='bold')

for i, txt in enumerate(crm_gaap_opm):
    ax2_twin.annotate(f"{txt:.1f}%", (x[i], crm_gaap_opm[i] + 1.2),
                      ha='center', color=c_line_2, fontsize=9.5, weight='bold')
for i, txt in enumerate(crm_nongaap_opm):
    ax2_twin.annotate(f"{txt:.1f}%", (x[i], crm_nongaap_opm[i] + 1.2),
                      ha='center', color='#7dd3fc', fontsize=9.0, weight='bold')

ax2.set_title('图 2：赛富时 (CRM) 无章程防弹衣下的外部激进股东纠偏兑现\n解散并购委员会后 GAAP 营业利润率从 2.1% 飙至 20.5%，FY26 返还 99% FCF',
              fontsize=12.8, fontweight='bold', color=c_text, pad=16)

handles3, labels3 = ax2.get_legend_handles_labels()
handles4, labels4 = ax2_twin.get_legend_handles_labels()
ax2.legend(handles3 + handles4, labels3 + labels4, loc='upper left', ncol=1,
           facecolor=c_card, edgecolor='#334155', labelcolor=c_text, fontsize=8.5)

plt.tight_layout(pad=2.0)
out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets')
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, 'nvda_vs_crm_governance_trend.png')
plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
print(f"Saved chart to: {out_path}")
