import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# Set font for macOS
plt.rcParams['font.sans-serif'] = ['PingFang SC', 'Heiti SC', 'Arial Unicode MS', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets')
os.makedirs(out_dir, exist_ok=True)


def draw_box(ax, x, y, w, h, title, body, facecolor='#111827', edgecolor='#38bdf8',
             title_color='#f8fafc', body_color='#cbd5e1', title_size=11.5, body_size=9.3,
             lw=1.8, title_y_ratio=0.76, body_y_ratio=0.35, zorder=3):
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.0,rounding_size=0.012",
        facecolor=facecolor, edgecolor=edgecolor, linewidth=lw, zorder=zorder
    )
    ax.add_patch(box)
    if body:
        ax.text(x + w / 2, y + h * title_y_ratio, title, ha='center', va='center',
                color=title_color, fontsize=title_size, fontweight='bold', zorder=zorder + 1)
        ax.text(x + w / 2, y + h * body_y_ratio, body, ha='center', va='center',
                color=body_color, fontsize=body_size, linespacing=1.45, zorder=zorder + 1)
    else:
        ax.text(x + w / 2, y + h / 2, title, ha='center', va='center',
                color=title_color, fontsize=title_size, fontweight='bold', zorder=zorder + 1)


def draw_tray(ax, x, y, w, h, facecolor='#0e1525', edgecolor='#1e293b', lw=1.5, ls='-', zorder=1):
    tray = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.0,rounding_size=0.016",
        facecolor=facecolor, edgecolor=edgecolor, linewidth=lw, linestyle=ls, zorder=zorder
    )
    ax.add_patch(tray)


def draw_arrow(ax, x1, y1, x2, y2, color='#64748b', lw=1.9, rad=0.0, ls='-', zorder=5):
    arrow = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle='-|>', mutation_scale=13.5,
        color=color, linewidth=lw, linestyle=ls,
        connectionstyle=f"arc3,rad={rad}", zorder=zorder
    )
    ax.add_patch(arrow)


# ==============================================================================
# CHART 1: 四阶代表样本“经济持股 vs 实际控制权”剪刀差 ＋ 美股股票分类四阶演化
# ==============================================================================
def create_chart_1():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16.8, 9.4), dpi=300, gridspec_kw={'width_ratios': [1.04, 1.0]})
    fig.patch.set_facecolor('#0b0f17')

    c_card = '#111827'
    c_grid = '#1e293b'
    c_text = '#f8fafc'
    c_muted = '#94a3b8'

    # --- Left Panel: Clean 5-Bar Scissor Comparison (Focused Anchor Companies Only) ---
    ax1.set_facecolor(c_card)
    ax1.tick_params(colors=c_muted, labelsize=11.0)
    ax1.tick_params(axis='y', pad=8)
    ax1.grid(True, axis='x', linestyle='--', alpha=0.35, color=c_grid)
    for spine in ax1.spines.values():
        spine.set_color('#334155')
        spine.set_linewidth(1.5)

    companies = [
        '英伟达 NVDA\n(黄仁勋｜单一普通股)',
        'Meta META\n(扎克伯格｜AB双层＋拟发C股)',
        '谷歌 Alphabet\n(佩奇＋布林｜A/B/C 三类股)',
        'Anthropic 创始人\n(7位创始人｜Class F 单股)',
        'Anthropic 信托 (LTBT)\n(伯南克等｜Class T 黄金股)'
    ]
    econ_vals = [3.58, 13.4, 6.0, 12.7, 0.0]
    ctrl_vals = [3.58, 60.8, 52.7, 50.1, 57.1]
    ctrl_notes = [
        '3.58% 选票 (完全对等)',
        '60.8% 选票 (放大约 4.5 倍)',
        '52.7% 选票 (放大近 9 倍)',
        '50.1% 股东票 (增发永不稀释)',
        '57.1% 董事席位 (4/7 过半席)'
    ]

    y = np.arange(len(companies))
    bar_h = 0.34

    b1 = ax1.barh(y + bar_h / 2, econ_vals, bar_h, label='实际经济持股占比 (%)', color='#06b6d4', alpha=0.86)
    b2 = ax1.barh(y - bar_h / 2, ctrl_vals, bar_h, label='股东投票权 / 董事会控制权 (%)', color='#f59e0b', alpha=0.90)

    ax1.axvline(50.0, color='#f43f5e', linestyle='--', linewidth=1.8, alpha=0.85, label='50% 绝对控制红线')
    ax1.set_yticks(y)
    ax1.set_yticklabels(companies, color=c_text, fontsize=11.2, fontweight='bold')
    ax1.invert_yaxis()
    ax1.set_xlim(0, 102)
    ax1.set_ylim(len(companies) - 0.35, -0.65)
    ax1.set_xlabel('占比百分比 (%)', color=c_text, fontsize=12.0, fontweight='bold', labelpad=10)
    ax1.set_title('左图：四大样本“经济出资 vs 实际控制权”剪刀差\n从 1 股 1 票到 0% 出资控制过半董事会，杠杆一路飙升',
                  color=c_text, fontsize=14.4, fontweight='bold', pad=14)

    for i, rect in enumerate(b1):
        w = rect.get_width()
        if i == 0:
            lbl = f"{w:.2f}%"
        elif i == 2:
            lbl = f"~{w:.1f}%"
        else:
            lbl = f"{w:.1f}%"
        ax1.text(w + 1.2, rect.get_y() + rect.get_height() / 2, lbl,
                 va='center', ha='left', color='#67e8f9', fontsize=10.8, fontweight='bold')

    for i, rect in enumerate(b2):
        w = rect.get_width()
        ax1.text(w + 1.2, rect.get_y() + rect.get_height() / 2, ctrl_notes[i],
                 va='center', ha='left', color='#fde68a', fontsize=10.8, fontweight='bold')

    ax1.legend(loc='lower right', facecolor='#0f172a', edgecolor='#475569', labelcolor=c_text, fontsize=10.5, framealpha=0.95)

    # --- Right Panel: Four Generations Evolution Ladder (Roomy & Large Font) ---
    ax2.set_facecolor(c_card)
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.axis('off')

    panel2_border = FancyBboxPatch(
        (0.01, 0.01), 0.98, 0.98,
        boxstyle="round,pad=0.004,rounding_size=0.016",
        facecolor=c_card, edgecolor='#334155', linewidth=1.6, zorder=1
    )
    ax2.add_patch(panel2_border)

    ax2.text(0.5, 0.952, '右图：美股股票分类四阶演化——从 1 股 1 票到五类积木',
             ha='center', va='center', color=c_text, fontsize=14.8, fontweight='bold', zorder=3)
    ax2.text(0.5, 0.905, '特拉华州契约自由下，创始人防稀释与锁死控盘的四次升级',
             ha='center', va='center', color=c_muted, fontsize=11.4, zorder=3)

    gens = [
        (0.685, '#38bdf8', '第一阶｜古典单一普通股（1 股 ＝ 1 票）',
         '• 样本：英伟达 (NVDA)｜出多少钱拿多少票，权责严格对称\n'
         '• 特点：外部股东制衡力强，但创始人无股权防弹衣'),
        (0.468, '#f59e0b', '第二阶｜AB 双层超级投票股（1 股 10 票）',
         '• 样本：Meta (META)｜公众 A 股 1 票，创始人 B 股 10 票\n'
         '• 痛点：持续增发融资或发员工股权激励会慢慢摊薄选票'),
        (0.252, '#fb7185', '第三阶｜零投票权 C 类股（0 票分红双代码）',
         '• 样本：谷歌 (GOOGL 1票 / GOOG 0票)，Meta 2026.10 跟进\n'
         '• 威力：激励与融资全发 0 票股，标普 500 于 2023 撤销禁令'),
        (0.036, '#a855f7', '第四阶｜五类积木与无分红黄金股（权钱分离）',
         '• 样本：Anthropic (ANT)｜1 股锁 50.1% 票 ＋ 1 股掌 4/7 董事\n'
         '• 跃迁：无需算倍率防稀释，把分红权与掌舵权彻底拆给不同人')
    ]

    for y_pos, col, t_str, b_str in gens:
        card = FancyBboxPatch(
            (0.028, y_pos), 0.944, 0.182,
            boxstyle="round,pad=0.005,rounding_size=0.014",
            facecolor='#161e2e', edgecolor=col, linewidth=1.9, zorder=2
        )
        ax2.add_patch(card)
        ax2.text(0.046, y_pos + 0.142, t_str, ha='left', va='center',
                 color=col, fontsize=13.6, fontweight='bold', zorder=3)
        ax2.text(0.046, y_pos + 0.062, b_str, ha='left', va='center',
                 color='#e2e8f0', fontsize=12.1, linespacing=1.78, zorder=3)

    for y_top in (0.685, 0.468, 0.252):
        draw_arrow(ax2, 0.50, y_top - 0.005, 0.50, y_top - 0.029, color='#94a3b8', lw=2.2)

    plt.tight_layout(pad=1.6)
    out_path = os.path.join(out_dir, 'ep02_us_share_classes_spectrum.png')
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight', pad_inches=0.25)
    plt.close(fig)
    print(f"Saved Chart 1 to: {out_path}")


# ==============================================================================
# CHART 2: Anthropic 五类普通股三权切分架构解剖图（等距四层母线版）
# ==============================================================================
def create_chart_2():
    fig, ax = plt.subplots(figsize=(17.2, 13.4), dpi=300)
    fig.patch.set_facecolor('#0b0f17')
    ax.set_facecolor('#0b0f17')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Main Header
    ax.text(0.51, 0.964, 'Anthropic (ANT) 五类普通股三权切分架构解剖图',
            ha='center', va='center', color='#f8fafc', fontsize=19.2, fontweight='bold')
    ax.text(0.51, 0.932, '基于 SEC Form S-1 招股书（2026年11月19日上市，发行价 $83.00，估值约 1.5 万亿美元）：收益、表决与董事会席位彻底拆装',
            ha='center', va='center', color='#94a3b8', fontsize=11.0)

    # Left margin layer badges aligned to exact midpoints of the 4 trays
    layer_labels = [
        (0.835, '第一层\n核心持有人\n(角色分工)'),
        (0.608, '第二层\n五类普通股\n(权利载体)'),
        (0.363, '第三层\n三权切分池\n(权责边界)'),
        (0.123, '第四层\n制度与日落锁\n(防失控机制)')
    ]
    for ly, ltxt in layer_labels:
        ax.text(0.038, ly, ltxt, ha='center', va='center', color='#cbd5e1',
                fontsize=9.9, fontweight='bold', linespacing=1.38,
                bbox=dict(boxstyle='round,pad=0.40', facecolor='#111827', edgecolor='#334155', lw=1.4))

    # ==========================================================================
    # TIER 1: Entities Tray [0.774 -> 0.896] (h = 0.122, mid = 0.835)
    # ==========================================================================
    draw_tray(ax, 0.080, 0.774, 0.900, 0.122, facecolor='#0d1422', edgecolor='#1e3a5f', lw=1.5)

    draw_box(ax, 0.092, 0.784, 0.195, 0.102,
             '长期利益信托 (LTBT)',
             '伯南克等外部独立受托人\n依法严禁持有公司经济股份',
             facecolor='#17192b', edgecolor='#a855f7', title_color='#e9d5ff', title_size=11.4, body_size=9.2)

    draw_box(ax, 0.300, 0.784, 0.220, 0.102,
             '7 位创始人 (Founder LLC)',
             'Dario Amodei 等创始人实体\n另合持约 12.7% 经济普通股',
             facecolor='#1c1917', edgecolor='#f59e0b', title_color='#fde68a', title_size=11.4, body_size=9.2)

    draw_box(ax, 0.533, 0.784, 0.435, 0.102,
             '公众投资者、战略巨头（亚马逊 / 谷歌等）与普通员工',
             'IPO 募资 813 亿美元｜亚马逊 (~15%) 与谷歌 (~14%) 属最主要外部金主\n在二级市场与私募配售中承担绝大部分真金白银资本投入',
             facecolor='#0f1d2b', edgecolor='#06b6d4', title_color='#a5f3fc', title_size=11.4, body_size=9.2)

    # --- Gap 1 -> 2 [0.680 -> 0.774] (EXACT gap = 0.094) ---
    # 5 clean non-crossing downward arrows into Tier 2 cards (centers: 0.174, 0.352, 0.530, 0.708, 0.886)
    draw_arrow(ax, 0.174, 0.784, 0.174, 0.682, color='#c084fc', lw=2.0, zorder=4)
    draw_arrow(ax, 0.352, 0.784, 0.352, 0.682, color='#fbbf24', lw=2.0, zorder=4)
    # Public/Strategic/Employees -> E (0.530), A (0.708), N (0.886) via clean bus at y=0.752
    bus1_y = 0.752
    ax.plot([0.750, 0.750], [0.784, bus1_y], color='#38bdf8', lw=2.0, zorder=4)
    ax.plot([0.530, 0.886], [bus1_y, bus1_y], color='#38bdf8', lw=2.0, zorder=4)
    draw_arrow(ax, 0.530, bus1_y, 0.530, 0.682, color='#34d399', lw=1.9, zorder=4)
    draw_arrow(ax, 0.708, bus1_y, 0.708, 0.682, color='#38bdf8', lw=2.0, zorder=4)
    draw_arrow(ax, 0.886, bus1_y, 0.886, 0.682, color='#fb7185', lw=2.0, zorder=4)

    ax.text(0.530, 0.722, '依 DGCL § 151(a) 契约自由：定向切分为五类权利各异的普通股',
            ha='center', va='center', color='#f1f5f9', fontsize=9.7, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.28', facecolor='#162032', edgecolor='#475569', lw=1.3), zorder=6)

    # ==========================================================================
    # TIER 2: 5 Share Classes Tray [0.536 -> 0.680] (h = 0.144, mid = 0.608)
    # ==========================================================================
    draw_tray(ax, 0.080, 0.536, 0.900, 0.144, facecolor='#0e1525', edgecolor='#334155', lw=1.6)

    draw_box(ax, 0.092, 0.546, 0.164, 0.124,
             'Class T (仅 1 股)',
             '面值 $0.00001｜0 分红\n独家任免 4/7 席董事\n(安全刹车黄金股)',
             facecolor='#1e1b33', edgecolor='#c084fc', title_color='#f3e8ff', title_size=11.0, body_size=8.9)

    draw_box(ax, 0.270, 0.546, 0.164, 0.124,
             'Class F (仅 1 股)',
             '面值 $0.00001｜0 分红\n恒定锁死 50.1% 选票\n(增发永不稀释锁)',
             facecolor='#241c13', edgecolor='#fbbf24', title_color='#fef3c7', title_size=11.0, body_size=8.9)

    draw_box(ax, 0.448, 0.546, 0.164, 0.124,
             'Class E 员工股',
             '0 分红｜0 日常票\n专享第 4 席 T 董事\n及信托修改制衡票',
             facecolor='#132220', edgecolor='#34d399', title_color='#d1fae5', title_size=11.0, body_size=8.9)

    draw_box(ax, 0.626, 0.546, 0.164, 0.124,
             'Class A (代码 ANT)',
             '1 票/股｜享全额分红\n总投票权封顶 49.9%\n无法左右常规表决',
             facecolor='#0c2333', edgecolor='#38bdf8', title_color='#e0f2fe', title_size=11.0, body_size=8.9)

    draw_box(ax, 0.804, 0.546, 0.164, 0.124,
             'Class N 战略零票股',
             '0 投票权｜享全额分红\n隔离亚马逊/谷歌插手\n转售公众后转为 A 股',
             facecolor='#231520', edgecolor='#fb7185', title_color='#ffe4e6', title_size=11.0, body_size=8.9)

    # --- Gap 2 -> 3 [0.442 -> 0.536] (EXACT gap = 0.094) ---
    # Orthogonal routing where NO vertical arrow passes behind any pill badge:
    # Pool 1: [0.092 -> 0.370] | Pool 2: [0.388 -> 0.672] | Pool 3: [0.690 -> 0.968]
    # 1) Class T (left side at x=0.125) straight down -> Pool 1
    draw_arrow(ax, 0.125, 0.546, 0.125, 0.444, color='#c084fc', lw=2.2, zorder=4)
    # 2) Class E (0.530) thin dashed orthogonal detour along dedicated upper lane y=0.520 -> x=0.312 -> Pool 1
    ax.plot([0.530, 0.530], [0.546, 0.520], color='#34d399', lw=1.6, ls='--', zorder=4)
    ax.plot([0.530, 0.312], [0.520, 0.520], color='#34d399', lw=1.6, ls='--', zorder=4)
    draw_arrow(ax, 0.312, 0.520, 0.312, 0.444, color='#34d399', lw=1.6, ls='--', zorder=4)
    # 3) Class F left helper (x=0.352) straight down -> Pool 1 (co-elects 3 seats)
    draw_arrow(ax, 0.352, 0.546, 0.352, 0.444, color='#fbbf24', lw=1.7, ls='--', zorder=4)

    # 4) Class F right main (x=0.412) straight down -> Pool 2
    draw_arrow(ax, 0.412, 0.546, 0.412, 0.444, color='#fbbf24', lw=2.2, zorder=4)
    # 5) Class A left branch (x=0.648) straight down -> Pool 2; right branch (x=0.720) straight down -> Pool 3
    draw_arrow(ax, 0.648, 0.546, 0.648, 0.444, color='#38bdf8', lw=2.0, zorder=4)
    draw_arrow(ax, 0.720, 0.546, 0.720, 0.444, color='#38bdf8', lw=2.1, zorder=4)
    # 6) Class N (x=0.938) straight down -> Pool 3
    draw_arrow(ax, 0.938, 0.546, 0.938, 0.444, color='#fb7185', lw=2.2, zorder=4)

    # Three centered pills in completely arrow-free corridors at y = 0.484
    ax.text(0.219, 0.484, 'T 任免 4 席 ｜ F+A 选 3 席',
            ha='center', va='center', color='#e9d5ff', fontsize=9.0, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.22', facecolor='#151624', edgecolor='#9333ea', lw=1.1), zorder=6)
    ax.text(0.530, 0.484, 'F 恒锁 50.1% vs A ≤ 49.9%',
            ha='center', va='center', color='#fde68a', fontsize=9.0, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.22', facecolor='#1c1914', edgecolor='#d97706', lw=1.1), zorder=6)
    ax.text(0.829, 0.484, 'A + N 共享 100% 经济收益',
            ha='center', va='center', color='#a5f3fc', fontsize=9.0, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.22', facecolor='#0d1f26', edgecolor='#0891b2', lw=1.1), zorder=6)

    # ==========================================================================
    # TIER 3: Three Power & Economic Pools Tray [0.284 -> 0.442] (h = 0.158, mid = 0.363)
    # ==========================================================================
    draw_tray(ax, 0.080, 0.284, 0.900, 0.158, facecolor='#0d1422', edgecolor='#1e3a5f', lw=1.5)

    draw_box(ax, 0.092, 0.294, 0.278, 0.138,
             '权力池 ①：董事会 7 席组阁权',
             '• Class T 董事 (4 席 / 57.1% 过半)：\n  由 LTBT 独家任免，无须理由可撤换\n• 普通/创始人董事 (3 席 / 42.9%)：\n  由 Class F 与 Class A 共选产生',
             facecolor='#151624', edgecolor='#a855f7', title_color='#e9d5ff', title_size=11.3, body_size=9.1, title_y_ratio=0.81, body_y_ratio=0.38)

    draw_box(ax, 0.388, 0.294, 0.284, 0.138,
             '权力池 ②：股东大会日常表决权',
             '• Class F (仅 1 股)：自动锁定 50.1%\n• Class A (公众＋机构)：集体封顶 49.9%\n• Class N / T / E：日常表决权 0.0%\n→ 招股书明示公众股东无法左右表决结果',
             facecolor='#1c1914', edgecolor='#f59e0b', title_color='#fde68a', title_size=11.3, body_size=9.1, title_y_ratio=0.81, body_y_ratio=0.38)

    draw_box(ax, 0.690, 0.294, 0.278, 0.138,
             '收益池 ③：1.5 万亿美元收益池',
             '• Class A ＋ Class N：按股数共享 100%\n  分红权与剩余资产清算权\n• Class T / Class F / Class E：\n  分红权为 0%（仅按 $0.00001 面值清算）',
             facecolor='#0d1f26', edgecolor='#06b6d4', title_color='#a5f3fc', title_size=11.0, body_size=9.1, title_y_ratio=0.81, body_y_ratio=0.38)

    # --- Gap 3 -> 4 [0.190 -> 0.284] (EXACT gap = 0.094) ---
    draw_arrow(ax, 0.295, 0.284, 0.295, 0.192, color='#10b981', lw=2.1, zorder=4)
    draw_arrow(ax, 0.765, 0.284, 0.765, 0.192, color='#94a3b8', lw=2.1, zorder=4)

    ax.text(0.530, 0.237, '底层公司章程护盾与创始人特权退场约束机制',
            ha='center', va='center', color='#e2e8f0', fontsize=9.7, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.28', facecolor='#111827', edgecolor='#475569', lw=1.3), zorder=6)

    # ==========================================================================
    # TIER 4: Governance Safeguards & Sunset Tray [0.056 -> 0.190] (h = 0.134, mid = 0.123)
    # ==========================================================================
    draw_tray(ax, 0.080, 0.056, 0.900, 0.134, facecolor='#0e1320', edgecolor='#334155', lw=1.5)

    draw_box(ax, 0.092, 0.066, 0.432, 0.114,
             '特拉华州 PBC 公益公司法盾 (DGCL § 362 & § 365)',
             '• 章程法定平衡“股东财务回报”与“负责任开发 AI 公共使命”\n• 豁免传统短期盈利最大化诉讼压力，给足顶层安全刹车合法依据',
             facecolor='#111827', edgecolor='#10b981', title_color='#6ee7b7', title_size=11.3, body_size=9.3)

    draw_box(ax, 0.538, 0.066, 0.430, 0.114,
             '防篡改双锁与创始人日落条款 (Sunset Provision)',
             '• 防反悔重锁：修改信托条款须 80% 全体董事赞成 ＋ Class T 信托明确同意\n• Class F 日落倒计时：在职创始人连续 90 天少于 3 人，50.1% 特权即消亡',
             facecolor='#111827', edgecolor='#64748b', title_color='#e2e8f0', title_size=11.3, body_size=9.3)

    # Footer note
    ax.text(0.51, 0.022, '注：所有比例与条款依据 Anthropic, PBC 于 2026 年 11 月提交 SEC 之 Form S-1 招股书整理；7 位创始人另持有约 12.7% 经济普通股。',
            ha='center', va='center', color='#64748b', fontsize=9.0)

    out_path = os.path.join(out_dir, 'ep02_anthropic_five_class_architecture.png')
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight', pad_inches=0.25)
    plt.close(fig)
    print(f"Saved Chart 2 to: {out_path}")


if __name__ == "__main__":
    create_chart_1()
    create_chart_2()
