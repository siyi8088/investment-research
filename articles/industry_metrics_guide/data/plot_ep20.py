import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# Dark Institutional Theme
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang SC', 'Heiti TC', 'STHeiti']
plt.rcParams['axes.unicode_minus'] = False

BG = '#0B111E'
PANEL_BG = '#111827'
GRID = '#1F2937'
TEXT = '#F3F4F6'
MUTED = '#9CA3AF'

C_FIN = '#38BDF8'     # Cluster 1: Finance & Insurance
C_TECH = '#A78BFA'    # Cluster 2: SaaS & Platforms
C_MED = '#34D399'     # Cluster 3: MedTech & Pharma
C_SEMI = '#F59E0B'    # Cluster 4: Semiconductors
C_CYC = '#FB7185'     # Cluster 5: Consumer, Energy & Shipping

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16.5, 7.4), dpi=300, gridspec_kw={'width_ratios': [1.22, 1.0]})
fig.patch.set_facecolor(BG)

# ==============================================================================
# LEFT PANEL: 19 Industries Commercial Gene Coordinates
# X = Asset / CapEx Intensity (1 Ultra-Light -> 10 Ultra-Heavy)
# Y = Earnings Cyclicality & Event Volatility (1 Ultra-Steady -> 10 Ultra-Volatile)
# ==============================================================================
ax1.set_facecolor(PANEL_BG)

clusters = [
    ('金融杠杆与久期错配族 (01-05)', C_FIN, 'o', [
        ('01 商业银行', 3.5, 4.8, (-12, -16)),
        ('02 投行做市', 3.0, 7.2, (-12, 10)),
        ('03 资管另类', 1.5, 4.2, (8, -4)),
        ('04 财险 P&C', 2.5, 5.5, (-14, 10)),
        ('05 寿险 EV',  4.0, 4.0, (8, -5)),
    ]),
    ('数字飞轮与轻资产网络族 (06-07)', C_TECH, '^', [
        ('06 SaaS 云',  1.6, 2.5, (8, -6)),
        ('07 平台网络', 2.2, 3.5, (8, 6)),
    ]),
    ('专利壁垒与研发临床族 (08-10)', C_MED, 'D', [
        ('08 医疗器械', 3.2, 1.8, (8, -6)),
        ('09 跨国大药', 4.6, 2.6, (8, -12)),
        ('10 临床 Biotech', 2.8, 8.5, (8, 5)),
    ]),
    ('硬核制造与算力链条族 (11-13)', C_SEMI, 's', [
        ('11 半导体设备', 5.6, 6.2, (8, -6)),
        ('12 晶圆代工',   8.8, 6.8, (-12, -16)),
        ('13 芯片设计',   2.6, 6.5, (8, -6)),
    ]),
    ('实体消费与重资产周期族 (14-19)', C_CYC, 'P', [
        ('14 商超零售', 5.2, 2.2, (8, -6)),
        ('15 连锁餐饮', 4.4, 2.9, (-16, 10)),
        ('16 电力公用', 8.4, 4.1, (-22, 10)),
        ('17 金属矿业', 8.5, 8.4, (8, 4)),
        ('18 上游油气', 9.0, 7.6, (-16, -17)),
        ('19 全球航运', 8.0, 9.2, (-26, 9)),
    ]),
]

# Quadrant dividers & subtle zone hints
ax1.axvline(5.0, color='#334155', linestyle='--', linewidth=1.2, zorder=1)
ax1.axhline(5.0, color='#334155', linestyle='--', linewidth=1.2, zorder=1)
ax1.text(0.95, 9.95, '轻资产高弹性区 (投行/芯片设计/Biotech)', color='#64748B', fontsize=8.4, fontweight='bold', va='top')
ax1.text(5.2, 9.95, '重资产强周期风暴区 (代工/矿业/油气/航运)', color='#64748B', fontsize=8.4, fontweight='bold', va='top')
ax1.text(0.95, 0.92, '轻资产现金复利区 (SaaS/平台/器械/大药)', color='#64748B', fontsize=8.4, fontweight='bold', va='bottom')
ax1.text(5.2, 0.92, '重资产基建与周转区', color='#64748B', fontsize=8.4, fontweight='bold', va='bottom')

for label, col, marker, pts in clusters:
    xs = [p[1] for p in pts]
    ys = [p[2] for p in pts]
    ax1.scatter(xs, ys, c=col, marker=marker, s=95, edgecolors='#0B111E', linewidths=0.9, label=label, zorder=5)
    for name, px, py, off in pts:
        ax1.annotate(name, (px, py), textcoords='offset points', xytext=off,
                     color=TEXT, fontsize=8.8, fontweight='bold', zorder=6,
                     bbox=dict(boxstyle='round,pad=0.14', facecolor='#0F172A', edgecolor='none', alpha=0.65))

ax1.set_xlim(0.7, 10.2)
ax1.set_ylim(0.7, 10.3)
ax1.set_xlabel('资产与资本开支重度 (1 极轻资产 → 10 超重资产)', color=TEXT, fontsize=10.8, fontweight='bold')
ax1.set_ylabel('盈利周期波动与事件弹性 (1 极稳健 → 10 极剧烈)', color=TEXT, fontsize=10.8, fontweight='bold')
ax1.tick_params(colors=MUTED, labelsize=9.5)
ax1.grid(True, color=GRID, linestyle='--', linewidth=0.7, zorder=0)
for sp in ['top', 'right']:
    ax1.spines[sp].set_visible(False)
for sp in ['left', 'bottom']:
    ax1.spines[sp].set_color('#374151')

ax1.set_title('19 大行业商业基因坐标：资本重度 vs 周期弹性', color=TEXT, fontsize=12.8, fontweight='bold', pad=12)
ax1.legend(loc='lower right', bbox_to_anchor=(0.99, 0.015), facecolor='#0F172A', edgecolor='#374151',
           labelcolor=TEXT, fontsize=7.8, framealpha=0.95, ncol=1)

# ==============================================================================
# RIGHT PANEL: 6 Universal Cross-Industry Traps x 5 Clusters Heatmap
# ==============================================================================
ax2.set_facecolor(PANEL_BG)

traps = [
    '并购商誉 / 摊销注水',
    'SBC / 股本与权益截流',
    '表外 / 监管隐性杠杆',
    '折旧悬崖 / 供给订单周期',
    '单品 / 大客户 / 地缘集中',
    '量纲 / 非GAAP 口径幻觉',
]
cols = ['金融保险\n(01-05)', '软件平台\n(06-07)', '医药器械\n(08-10)', '半导体链\n(11-13)', '消费能源\n航运(14-19)']

# Matrix: 0=低(常规关注), 1=中(重点核验), 2=高危(一票否决核心区)
mat = np.array([
    [1, 1, 2, 1, 1],  # Goodwill / Amort / M&A reserves bloat
    [0, 2, 2, 1, 2],  # SBC (SNOW) / Dilution (CRSP) / NCI截留 (FCX 57% / SCCO 0.3%)
    [2, 0, 0, 2, 2],  # Bank HTM/AOCI (BAC) / Fabless Purchase Oblig (NVDA) / Shipping IFRS16 Leases (Maersk 72%)
    [0, 0, 1, 2, 2],  # Foundry Depreciation Cliff (SMIC) / Shipping Orderbook 54% (COSCO) & Upstream DD&A
    [1, 1, 2, 2, 2],  # Single-Drug LOE (NVO) / Fabless Geopolitics (NVDA) / Grasberg Resource Nationalism (FCX)
    [2, 2, 2, 1, 2],  # Non-GAAP Carry / ARR / GTN Rebates / Energy BOE 6:1 & FFE vs TEU
])

cmap = ListedColormap(['#1E293B', '#92400E', '#991B1B'])
ax2.imshow(mat, cmap=cmap, aspect='auto', vmin=0, vmax=2, zorder=2)

# Gridlines between cells
ax2.set_xticks(np.arange(len(cols)))
ax2.set_xticklabels(cols, color=TEXT, fontsize=9.3, fontweight='bold')
ax2.set_yticks(np.arange(len(traps)))
ax2.set_yticklabels(traps, color=TEXT, fontsize=9.5, fontweight='bold')
ax2.set_xticks(np.arange(-0.5, len(cols), 1), minor=True)
ax2.set_yticks(np.arange(-0.5, len(traps), 1), minor=True)
ax2.grid(which='minor', color='#0B111E', linestyle='-', linewidth=2.5, zorder=4)
ax2.tick_params(which='minor', bottom=False, left=False)
for sp in ax2.spines.values():
    sp.set_color('#374151')

cell_txt = {0: '常规', 1: '重点核验', 2: '高危暗门'}
cell_col = {0: '#94A3B8', 1: '#FDE68A', 2: '#FEE2E2'}
for i in range(mat.shape[0]):
    for j in range(mat.shape[1]):
        v = mat[i, j]
        ax2.text(j, i, cell_txt[v], ha='center', va='center',
                 color=cell_col[v], fontsize=9.8, fontweight='bold', zorder=5)

ax2.set_title('跨行业六大财报暗门：高危排雷触发矩阵', color=TEXT, fontsize=12.8, fontweight='bold', pad=12)

fig.suptitle('《买方级行业财报解剖与特异性指标图谱》收官全景：商业基因坐标与跨赛道排雷矩阵',
             color=TEXT, fontsize=15.0, fontweight='bold', y=0.97)
fig.text(0.5, 0.015,
         '数据与结构来源：本专栏第 01–19 讲 38 家全球核心龙头 10-K/20-F/年报及 2026 Q3 最新财报交叉归因总结（左图坐标代表行业商业基因相对分位）。',
         ha='center', color=MUTED, fontsize=9)

plt.tight_layout(rect=[0.01, 0.04, 0.99, 0.92])
out_png = '/Users/siyi/Documents/code/investment-research/articles/industry_metrics_guide/assets/ep20_all_industries_panorama.png'
plt.savefig(out_png, dpi=300, facecolor=BG)
print(f'Saved panorama chart to {out_png}')
