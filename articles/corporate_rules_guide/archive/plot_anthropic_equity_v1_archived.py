import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# Set font for macOS
plt.rcParams['font.sans-serif'] = ['PingFang SC', 'Heiti SC', 'Arial Unicode MS', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets')
os.makedirs(out_dir, exist_ok=True)


def draw_box(ax, x, y, w, h, title, body, facecolor='#111827', edgecolor='#38bdf8',
             title_color='#f8fafc', body_color='#cbd5e1', title_size=11.5, body_size=9.5, lw=1.8):
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.005,rounding_size=0.014",
        facecolor=facecolor, edgecolor=edgecolor, linewidth=lw, zorder=2
    )
    ax.add_patch(box)
    if body:
        ax.text(x + w / 2, y + h * 0.72, title, ha='center', va='center',
                color=title_color, fontsize=title_size, fontweight='bold', zorder=3)
        ax.text(x + w / 2, y + h * 0.34, body, ha='center', va='center',
                color=body_color, fontsize=body_size, linespacing=1.42, zorder=3)
    else:
        ax.text(x + w / 2, y + h / 2, title, ha='center', va='center',
                color=title_color, fontsize=title_size, fontweight='bold', zorder=3)


def draw_arrow(ax, x1, y1, x2, y2, color='#64748b', lw=1.6, rad=0.0, ls='-'):
    arrow = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle='-|>', mutation_scale=13,
        color=color, linewidth=lw, linestyle=ls,
        connectionstyle=f"arc3,rad={rad}", zorder=4
    )
    ax.add_patch(arrow)


# ==============================================================================
# CHART 1: Anthropic (ANT) 五类股票与 PBC 三权分立控制权架构全景图 (100% Step 310 定稿原版)
# ==============================================================================
def create_chart_1():
    fig, ax = plt.subplots(figsize=(16, 11.5), dpi=300)
    fig.patch.set_facecolor('#0b0f17')
    ax.set_facecolor('#0b0f17')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Main Header
    ax.text(0.5, 0.962, 'Anthropic (ANT) 五类普通股与 PBC“三权分立”控制权架构全景图',
            ha='center', va='center', color='#f8fafc', fontsize=18.5, fontweight='bold')
    ax.text(0.5, 0.930, '基于 SEC Form S-1 招股书（2026年11月19日纳斯达克上市，发行价 $83.00，估值约 1.5 万亿美元）：收益权、日常表决权与董事会组阁权彻底分离',
            ha='center', va='center', color='#94a3b8', fontsize=10.8)

    # Layer labels on left margin
    layer_labels = [
        (0.825, '第一层\n核心主体'),
        (0.625, '第二层\n五类股票'),
        (0.375, '第三层\n三权切分'),
        (0.115, '第四层\n法理护盾')
    ]
    for ly, ltxt in layer_labels:
        ax.text(0.028, ly, ltxt, ha='center', va='center', color='#64748b',
                fontsize=9.5, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.35', facecolor='#111827', edgecolor='#1e293b'))

    # --- Tier 1: Entities (y: 0.76 -> 0.89) ---
    draw_box(ax, 0.075, 0.765, 0.25, 0.12,
             '长期利益信托 (LTBT)',
             '伯南克、Shah 等独立受托人\n依法严禁持有公司任何经济证券',
             facecolor='#17192b', edgecolor='#a855f7', title_color='#e9d5ff')
    draw_box(ax, 0.345, 0.765, 0.23, 0.12,
             '7 位联合创始人 (Founder LLC)',
             'Dario Amodei 等联合创始人载体\nIPO 后合计持有约 12.7% 经济股权',
             facecolor='#1c1917', edgecolor='#f59e0b', title_color='#fde68a')
    draw_box(ax, 0.595, 0.765, 0.365, 0.12,
             '公众股民、战略巨头与非创始人雇员',
             'IPO 募资 813 亿美元｜亚马逊 (~15%) 与谷歌 (~14%) 合计占近三成\n在二级市场与商业合作中承担绝大部分真金白银出资',
             facecolor='#0f1d2b', edgecolor='#06b6d4', title_color='#a5f3fc')

    # --- Tier 2: 5 Share Classes (y: 0.55 -> 0.70) ---
    draw_box(ax, 0.075, 0.555, 0.165, 0.14,
             'Class T 股 (仅 1 股)',
             '面值 $0.00001｜0 分红权\n专职任免 4/7 董事\n（信托治理黄金股）',
             facecolor='#1e1b33', edgecolor='#c084fc', title_color='#f3e8ff', body_size=8.8)
    draw_box(ax, 0.260, 0.555, 0.165, 0.14,
             'Class F 股 (仅 1 股)',
             '面值 $0.00001｜0 分红权\n动态锁定 50.1% 股东票\n（增发永不稀释）',
             facecolor='#241c13', edgecolor='#fbbf24', title_color='#fef3c7', body_size=8.8)
    draw_box(ax, 0.445, 0.555, 0.150, 0.14,
             'Class E 员工股',
             '0 分红权｜无日常表决权\n特定信托与第 4 席\nClass T 董事提名监督权',
             facecolor='#132220', edgecolor='#34d399', title_color='#d1fae5', body_size=8.8)
    draw_box(ax, 0.615, 0.555, 0.165, 0.14,
             'Class A 上市股 (ANT)',
             '1 票/股｜享全额经济收益\n总投票权被封顶在 49.9%\n无法左右任何常规表决',
             facecolor='#0c2333', edgecolor='#38bdf8', title_color='#e0f2fe', body_size=8.8)
    draw_box(ax, 0.800, 0.555, 0.160, 0.14,
             'Class N 战略零票股',
             '0 投票权｜享全额经济收益\n隔离亚马逊/谷歌同业控制\n转售外部公众后转为 A 股',
             facecolor='#231520', edgecolor='#fb7185', title_color='#ffe4e6', body_size=8.8)

    # Arrows Tier 1 -> Tier 2
    draw_arrow(ax, 0.165, 0.758, 0.157, 0.703, color='#c084fc', lw=1.8)
    draw_arrow(ax, 0.430, 0.758, 0.342, 0.703, color='#fbbf24', lw=1.8)
    draw_arrow(ax, 0.480, 0.758, 0.670, 0.703, color='#f59e0b', lw=1.3, ls='--')
    draw_arrow(ax, 0.640, 0.758, 0.520, 0.703, color='#34d399', lw=1.6)
    draw_arrow(ax, 0.760, 0.758, 0.697, 0.703, color='#38bdf8', lw=1.8)
    draw_arrow(ax, 0.880, 0.758, 0.880, 0.703, color='#fb7185', lw=1.8)

    # --- Tier 3: Three Power & Economic Pools (y: 0.28 -> 0.47) ---
    draw_box(ax, 0.075, 0.285, 0.280, 0.18,
             '权力池 ①：董事会 7 席任免权',
             '• Class T 董事 (4 席 / 57.1% 绝对多数)：\n  由 LTBT 单独任免，无须业绩理由即可撤换\n• 普通/创始人董事 (3 席 / 42.9%)：\n  由 Class F 与 Class A 共同投票选出',
             facecolor='#151624', edgecolor='#a855f7', title_color='#e9d5ff', body_size=8.8)

    draw_box(ax, 0.375, 0.285, 0.285, 0.18,
             '权力池 ②：股东大会日常表决权',
             '• Class F (创始人单股)：恒定 50.1%\n• Class A (公众＋创始人流通)：封顶 49.9%\n• Class N / T / E：日常常规表决 0.0%\n→ 招股书明示：公众股民无法左右表决结果',
             facecolor='#1c1914', edgecolor='#f59e0b', title_color='#fde68a', body_size=8.8)

    draw_box(ax, 0.680, 0.285, 0.280, 0.18,
             '收益池 ③：1.5 万亿美元经济收益池',
             '• Class A ＋ Class N：共享 100% 分红与清算权\n• Class T (1股)、Class F (1股)、Class E：\n  分红与剩余索取权为 0% (仅按面值清算)\n→ 彻底实现“出钱者分钱，信托与创始人掌舵”',
             facecolor='#0d1f26', edgecolor='#06b6d4', title_color='#a5f3fc', body_size=8.8)

    # Arrows Tier 2 -> Tier 3
    draw_arrow(ax, 0.157, 0.548, 0.195, 0.473, color='#c084fc', lw=2.2)
    draw_arrow(ax, 0.485, 0.548, 0.275, 0.473, color='#34d399', lw=1.4, ls='--')
    draw_arrow(ax, 0.342, 0.548, 0.495, 0.473, color='#fbbf24', lw=2.2)
    draw_arrow(ax, 0.310, 0.548, 0.255, 0.473, color='#fbbf24', lw=1.3, ls='--')
    draw_arrow(ax, 0.660, 0.548, 0.555, 0.473, color='#38bdf8', lw=1.6)
    draw_arrow(ax, 0.725, 0.548, 0.790, 0.473, color='#38bdf8', lw=2.0)
    draw_arrow(ax, 0.880, 0.548, 0.855, 0.473, color='#fb7185', lw=2.0)

    # --- Tier 4: Legal Foundation & Safeguards (y: 0.045 -> 0.20) ---
    draw_box(ax, 0.075, 0.055, 0.430, 0.15,
             '特拉华州公益公司法护盾 (DGCL § 362 & § 365)',
             '• 董事法定必须平衡“股东收益”与“为全人类负责任开发 AI”公益使命\n• 豁免传统 Revlon 最高价卖身铁律，保护管理层为 AI 安全牺牲短期利润免遭起诉',
             facecolor='#111827', edgecolor='#10b981', title_color='#6ee7b7', body_size=9.0)

    draw_box(ax, 0.530, 0.055, 0.430, 0.15,
             '防篡改重锁与创始人日落条款 (Sunset Provisions)',
             '• 修改信托及核心治理条款：须同时获 80% 董事赞成 ＋ Class T 信托明确同意\n• Class F 日落倒计时：在职创始人少于 3 人持续满 90 天即触发 50.1% 特权消亡',
             facecolor='#111827', edgecolor='#64748b', title_color='#e2e8f0', body_size=9.0)

    draw_arrow(ax, 0.215, 0.278, 0.260, 0.213, color='#10b981', lw=1.5)
    draw_arrow(ax, 0.515, 0.278, 0.720, 0.213, color='#94a3b8', lw=1.5)

    ax.text(0.5, 0.015, '注：所有结构与比例依据 Anthropic, PBC 提交 SEC 之 Form S-1 招股书及公开披露整理；Class F 经济权益列仅指该单股本身，7 位创始人另持有约 12.7% 经济普通股。',
            ha='center', va='center', color='#64748b', fontsize=8.8)

    out_path = os.path.join(out_dir, 'ep01_anthropic_five_class_architecture.png')
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight', pad_inches=0.25)
    plt.close(fig)
    print(f"Saved Chart 1 to: {out_path}")


# ==============================================================================
# CHART 2: 左图 100% 维持 Step 310 定稿原版，仅适度放大右图字号
# ==============================================================================
def create_chart_2():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18.5, 9.5), dpi=300, gridspec_kw={'width_ratios': [1.08, 1.0]})
    fig.patch.set_facecolor('#0b0f17')

    c_card = '#111827'
    c_grid = '#1e293b'
    c_text = '#f8fafc'
    c_muted = '#94a3b8'

    # --- Panel 1: Horizontal Grouped Bar Chart (100% Step 310 定稿原版) ---
    ax1.set_facecolor(c_card)
    ax1.tick_params(colors=c_muted, labelsize=10.5)
    ax1.grid(True, axis='x', linestyle='--', alpha=0.35, color=c_grid)
    for spine in ax1.spines.values():
        spine.set_color('#334155')

    companies = [
        '苹果 AAPL\n(全体高管及董事｜1股1票)',
        '英伟达 NVDA\n(黄仁勋｜1股1票)',
        '福特汽车 F\n(福特家族｜Class B 超级票)',
        'Alphabet GOOGL\n(佩奇＋布林｜B 10票＋C 0票)',
        'Meta META\n(扎克伯格｜B 10票＋拟推 C 0票)',
        'Anthropic 创始人\n(7位创始人｜Class F 恒定 50.1%)',
        'Anthropic 信托 (LTBT)\n(伯南克等｜Class T 任免董事)'
    ]
    econ_vals = [0.06, 3.58, 2.0, 12.0, 13.4, 12.7, 0.0]
    ctrl_vals = [0.06, 3.58, 40.0, 52.7, 60.8, 50.1, 57.1]
    ctrl_notes = [
        '0.06% 选票 (完全匹配)',
        '3.58% 选票 (完全匹配)',
        '40.0% 选票 (差 +38.0pct)',
        '52.7% 选票 (差 +40.7pct)',
        '60.8% 选票 (差 +47.4pct)',
        '50.1% 股东大会票 (永不稀释)',
        '57.1% 董事会席位 (4/7 席)'
    ]

    y = np.arange(len(companies))
    bar_h = 0.36

    b1 = ax1.barh(y + bar_h / 2, econ_vals, bar_h, label='实际经济出资 / 持股占比 (%)', color='#06b6d4', alpha=0.82)
    b2 = ax1.barh(y - bar_h / 2, ctrl_vals, bar_h, label='股东投票权 / 董事会控制权占比 (%)', color='#f59e0b', alpha=0.88)

    ax1.axvline(50.0, color='#f43f5e', linestyle='--', linewidth=1.6, alpha=0.8, label='50% 绝对控制红线 (Controlled Company)')
    ax1.set_yticks(y)
    ax1.set_yticklabels(companies, color=c_text, fontsize=10.0, fontweight='bold')
    ax1.invert_yaxis()
    ax1.set_xlim(0, 92)
    ax1.set_xlabel('占比百分比 (%)', color=c_text, fontsize=11.5, fontweight='bold', labelpad=10)
    ax1.set_title('图 1：典型美股巨头“经济出资 vs 实际控制权”剪刀差实证\n从 1 股 1 票到 0% 出资控制过半董事会，权责杠杆一路放大',
                  color=c_text, fontsize=13.0, fontweight='bold', pad=14)

    for i, rect in enumerate(b1):
        w = rect.get_width()
        lbl = f"{w:.2f}%" if w < 5 and w != 2.0 and w != 0.0 else (f"~{w:.1f}%" if i in (2, 3) else f"{w:.1f}%")
        ax1.text(w + 1.0, rect.get_y() + rect.get_height() / 2, lbl,
                 va='center', ha='left', color='#67e8f9', fontsize=9.2, fontweight='bold')

    for i, rect in enumerate(b2):
        w = rect.get_width()
        ax1.text(w + 1.0, rect.get_y() + rect.get_height() / 2, ctrl_notes[i],
                 va='center', ha='left', color='#fde68a', fontsize=9.2, fontweight='bold')

    ax1.legend(loc='lower right', facecolor='#0f172a', edgecolor='#334155', labelcolor=c_text, fontsize=9.0)

    # --- Panel 2: Four Generations Evolution Ladder (适度放大字号) ---
    ax2.set_facecolor(c_card)
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.axis('off')
    for spine in ax2.spines.values():
        spine.set_color('#334155')

    ax2.text(0.5, 0.96, '图 2：美股百年股权架构四代演化阶梯',
             ha='center', va='center', color=c_text, fontsize=13.8, fontweight='bold')
    ax2.text(0.5, 0.915, '特拉华州法律“契约自由”下，创始人防御华尔街的四次工具升级',
             ha='center', va='center', color=c_muted, fontsize=11.0)

    gens = [
        (0.695, '#38bdf8', '第一代｜古典同股同权（One-Share, One-Vote）',
         '• 代表：苹果 (AAPL)、英伟达 (NVDA)\n• 逻辑：出多少钱拿多少票，董事高管受制于机构股东表决\n• 特点：纠偏力极强，但遇低估或冲击时易遭恶意收购或内耗'),
        (0.480, '#f59e0b', '第二代｜AB 双层倍率制（1 股 10 票，1936–2010s）',
         '• 代表：福特汽车 (2% 锁 40%)、Meta (13.4% 锁 60.8%)\n• 逻辑：源自福特分红案教训，公众股 1 票、创始人 B 股 10 票\n• 痛点：不断发 A 股融资或做员工激励时，选票仍会被逐渐摊薄'),
        (0.265, '#fb7185', '第三代｜零投票权股普及与指数妥协（2014–2026）',
         '• 代表：Google (GOOG)、Snap (全零票)、Meta (2026 C 股)\n• 博弈：2017 遭标普 500 封杀；2023 年 4 月标普撤销禁令解禁\n• 威力：日常股权激励与融资全用 0 票股，创始人选票永不稀释'),
        (0.050, '#a855f7', '第四代｜无经济权黄金股＋PBC 使命信托（2022–2026）',
         '• 代表：Patagonia (2022)、OpenAI PBC、Anthropic (ANT)\n• 跃迁：投票权与分红权彻底分离，1 股 0 分红锁过半董事会\n• 法盾：借 DGCL § 365 公益条款合法豁免短视盈利官司')
    ]

    for y_pos, col, t_str, b_str in gens:
        card = FancyBboxPatch(
            (0.03, y_pos), 0.94, 0.175,
            boxstyle="round,pad=0.005,rounding_size=0.014",
            facecolor='#161e2e', edgecolor=col, linewidth=1.8, zorder=2
        )
        ax2.add_patch(card)
        ax2.text(0.055, y_pos + 0.140, t_str, ha='left', va='center',
                 color=col, fontsize=11.8, fontweight='bold', zorder=3)
        ax2.text(0.055, y_pos + 0.062, b_str, ha='left', va='center',
                 color='#e2e8f0', fontsize=10.5, linespacing=1.42, zorder=3)

    # Connecting arrows between generations
    for y_top in (0.695, 0.480, 0.265):
        draw_arrow(ax2, 0.50, y_top - 0.006, 0.50, y_top - 0.034, color='#94a3b8', lw=2.0)

    plt.tight_layout(pad=1.8)
    out_path = os.path.join(out_dir, 'ep01_us_equity_evolution_spectrum.png')
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight', pad_inches=0.25)
    plt.close(fig)
    print(f"Saved Chart 2 to: {out_path}")


if __name__ == "__main__":
    create_chart_1()
    create_chart_2()
