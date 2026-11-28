import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# Set font for macOS
plt.rcParams['font.sans-serif'] = ['PingFang SC', 'Heiti SC', 'Arial Unicode MS', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets')
os.makedirs(out_dir, exist_ok=True)


def draw_box(ax, x, y, w, h, title, body, facecolor='#111827', edgecolor='#38bdf8',
             title_color='#f8fafc', body_color='#cbd5e1', title_size=12.0, body_size=9.8,
             lw=1.8, title_y_ratio=0.74, body_y_ratio=0.34, zorder=3):
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
                color=body_color, fontsize=body_size, linespacing=1.44, zorder=zorder + 1)
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
# CHART 1: 美国上市公司“三层权力隔离”与英伟达 11 人董事会解剖图（精密等距母线版）
# ==============================================================================
def create_chart_1():
    fig, ax = plt.subplots(figsize=(17.2, 13.4), dpi=300)
    fig.patch.set_facecolor('#0b0f17')
    ax.set_facecolor('#0b0f17')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Main Header
    ax.text(0.51, 0.964, '美国上市公司顶层权力架构：英伟达（NVDA）11 人董事会解剖图',
            ha='center', va='center', color='#f8fafc', fontsize=19.2, fontweight='bold')
    ax.text(0.51, 0.932, '以 2026 年 11 月改组后架构为真实样本（单一普通股，1 股 1 票）：出资权、董事会决策监督权与日常经营权的层级闭环',
            ha='center', va='center', color='#94a3b8', fontsize=11.4)

    # Left margin layer badges (aligned to exact vertical midpoints of the 4 trays)
    layer_labels = [
        (0.835, '第一层\n出资股东\n(所有权层)'),
        (0.608, '第二层\n11人董事会\n(决策监督层)'),
        (0.363, '第三层\n四大委员会\n(独董实权层)'),
        (0.123, '第四层\n日常高管层\n(受雇执行层)')
    ]
    for ly, ltxt in layer_labels:
        ax.text(0.038, ly, ltxt, ha='center', va='center', color='#cbd5e1',
                fontsize=10.0, fontweight='bold', linespacing=1.38,
                bbox=dict(boxstyle='round,pad=0.42', facecolor='#111827', edgecolor='#334155', lw=1.4))

    # ==========================================================================
    # TIER 1: Stockholders Tray [0.774 -> 0.896] (h = 0.122, mid = 0.835)
    # ==========================================================================
    draw_tray(ax, 0.080, 0.774, 0.900, 0.122, facecolor='#0d1422', edgecolor='#1e3a5f', lw=1.5)

    draw_box(ax, 0.092, 0.784, 0.552, 0.102,
             '华尔街机构与全球公众股东（合计持股约 96.42% ＝ 投票权 96.42%）',
             '贝莱德 (7.43%)、先锋领航 (7.31%) 等机构与散户｜享有分红与剩余收益权\n铁律：哪怕集齐过半数股东签名，依法也无权直接发文件雇佣或开除 CEO',
             facecolor='#0f1d2b', edgecolor='#06b6d4', title_color='#a5f3fc', title_size=11.8, body_size=9.6)

    draw_box(ax, 0.658, 0.784, 0.310, 0.102,
             '创始人股东 黄仁勋（持股 3.58%）',
             '同股同权（无 AB 超级投票股）｜选票同样仅 3.58%\n在股东大会上与外部机构按 1 股 1 票平等合池计票',
             facecolor='#1c1917', edgecolor='#f59e0b', title_color='#fde68a', title_size=11.8, body_size=9.6)

    # --- Connector Zone 1 -> 2 [0.680 -> 0.774] (EXACT gap = 0.094) ---
    bus1_y = 0.754
    ax.plot([0.368, 0.368], [0.784, bus1_y], color='#38bdf8', lw=2.0, zorder=4)
    ax.plot([0.813, 0.813], [0.784, bus1_y], color='#f59e0b', lw=2.0, zorder=4)
    ax.plot([0.368, 0.813], [bus1_y, bus1_y], color='#64748b', lw=2.0, zorder=4)
    draw_arrow(ax, 0.530, bus1_y, 0.530, 0.682, color='#cbd5e1', lw=2.2, zorder=4)

    ax.text(0.530, 0.725, '全体股东合池投票：每年仅选举“全体 11 名董事”（DGCL § 141(a) 赋予董事会掌管公司最高权力）',
            ha='center', va='center', color='#f1f5f9', fontsize=9.8, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.30', facecolor='#162032', edgecolor='#475569', lw=1.3), zorder=6)

    # ==========================================================================
    # TIER 2: 11-Member Board of Directors Tray [0.536 -> 0.680] (h = 0.144, mid = 0.608)
    # ==========================================================================
    draw_tray(ax, 0.080, 0.536, 0.900, 0.144, facecolor='#0e1525', edgecolor='#334155', lw=1.6)

    # Card 1: Independent Chair (center x = 0.228)
    draw_box(ax, 0.092, 0.546, 0.272, 0.124,
             '首位独立董事长｜Harvey C. Jones',
             '1993 年入局元老独董｜2026.11 首设此职\n执掌董事会木槌，主持会议并代表董事会发声\n实现“管董事会的董事长”与“管业务的 CEO”分家',
             facecolor='#221c12', edgecolor='#fbbf24', title_color='#fef08a', title_size=11.5, body_size=9.2)

    # Card 2: Other 9 Independent Directors (center x = 0.560)
    draw_box(ax, 0.378, 0.546, 0.364, 0.124,
             '其余 9 名外部独立董事（不在公司领薪的“外人”）',
             '• 首席独董 Stephen Neal（律所荣誉主席，召集独董闭门会）\n• 前高盛副主席 Johnson、前百事北美 CEO Hudson、前礼来高管 Shah、\n  加州理工教授 Dabiri 及 Seawell、Coxe、Stevens、Lora',
             facecolor='#0d2133', edgecolor='#38bdf8', title_color='#e0f2fe', title_size=11.5, body_size=9.1)

    # Card 3: Sole Insider Director Jensen Huang (center x = 0.862)
    draw_box(ax, 0.756, 0.546, 0.212, 0.124,
             '唯一内部董事｜黄仁勋',
             '仅占 11 席中的 1 席（9.1%）\n全公司唯一上桌的内部高管\n涉己薪酬/调查表决依法回避',
             facecolor='#231520', edgecolor='#fb7185', title_color='#ffe4e6', title_size=11.5, body_size=9.2)

    # --- Connector Zone 2 -> 3 [0.442 -> 0.536] (EXACT gap = 0.094) ---
    merge_indep_y = 0.518
    bus2_y = 0.464
    comm_centers = [0.1945, 0.4182, 0.6418, 0.8655]

    ax.plot([0.228, 0.228], [0.546, merge_indep_y], color='#fbbf24', lw=2.0, zorder=4)
    ax.plot([0.560, 0.560], [0.546, merge_indep_y], color='#38bdf8', lw=2.0, zorder=4)
    ax.plot([0.228, 0.560], [merge_indep_y, merge_indep_y], color='#38bdf8', lw=2.0, zorder=4)
    ax.plot([0.4182, 0.4182], [merge_indep_y, bus2_y], color='#38bdf8', lw=2.2, zorder=4)

    ax.plot([comm_centers[0], comm_centers[-1]], [bus2_y, bus2_y], color='#38bdf8', lw=2.0, zorder=4)
    for cx in comm_centers:
        draw_arrow(ax, cx, bus2_y, cx, 0.444, color='#38bdf8', lw=1.9, zorder=4)

    ax.text(0.4182, 0.491, '仅由左侧 10 名外部独立董事分组兼任，100% 掌控四大核心委员会',
            ha='center', va='center', color='#bae6fd', fontsize=9.7, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.26', facecolor='#0f172a', edgecolor='#0284c7', lw=1.2), zorder=6)

    # Explicit Firewall Stop Sign under Jensen Huang (aligned horizontally at y = 0.491)
    ax.plot([0.862, 0.862], [0.546, 0.510], color='#f43f5e', lw=2.0, ls='--', zorder=5)
    ax.text(0.862, 0.491, '⊘ 隔离墙：CEO 禁入委员会',
            ha='center', va='center', color='#fda4af', fontsize=9.6, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.26', facecolor='#2b141d', edgecolor='#f43f5e', lw=1.3), zorder=6)

    # ==========================================================================
    # TIER 3: Four 100% Independent Standing Committees [0.284 -> 0.442] (h = 0.158, mid = 0.363)
    # ==========================================================================
    draw_tray(ax, 0.080, 0.284, 0.900, 0.158, facecolor='#0d1422', edgecolor='#1e3a5f', lw=1.5)

    draw_box(ax, 0.0920, 0.294, 0.205, 0.138,
             '① 审计委员会 (Audit)',
             '100% 独董｜主席 Seawell\n• 直接雇佣与监督外部审计师\n• 严查财报真伪与内控底线\n• 杜绝管理层自己审自己',
             facecolor='#111c2d', edgecolor='#38bdf8', title_color='#bae6fd', title_size=11.3, body_size=9.2)

    draw_box(ax, 0.3157, 0.294, 0.205, 0.138,
             '② 薪酬委员会 (Comp)',
             '100% 独董｜主席 Hudson\n• 核定 CEO 与高管工资及股票\n• 独立聘请第三方薪酬顾问\n• 防止高管自己给自己发奖金',
             facecolor='#111c2d', edgecolor='#38bdf8', title_color='#bae6fd', title_size=11.3, body_size=9.2)

    draw_box(ax, 0.5393, 0.294, 0.205, 0.138,
             '③ 提名与治理委员会',
             '100% 独董｜主席 Neal\n• 物色并提名下届董事候选人\n• 制定公司治理准则与评估\n• 防止 CEO 把私交塞满董事会',
             facecolor='#111c2d', edgecolor='#38bdf8', title_color='#bae6fd', title_size=11.3, body_size=9.2)

    draw_box(ax, 0.7630, 0.294, 0.205, 0.138,
             '④ 国安与出口管制委员会',
             '100% 独董｜主席 Johnson\n• 2026.11.17 风暴期间新设\n• 直管芯片出口合规与地缘风险\n• 授权独立聘请外部国安顾问',
             facecolor='#132421', edgecolor='#10b981', title_color='#a7f3d0', title_size=11.3, body_size=9.2, lw=2.1)

    # --- Connector Zone 3 -> 4 [0.190 -> 0.284] (EXACT gap = 0.094) ---
    draw_arrow(ax, 0.370, 0.284, 0.370, 0.192, color='#a855f7', lw=2.3, zorder=4)
    ax.text(0.370, 0.237, '董事会整体垄断高管任免权 (DGCL § 142(b)) ＋ 各委员会分掌查账与核薪',
            ha='center', va='center', color='#e9d5ff', fontsize=9.7, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.28', facecolor='#181826', edgecolor='#6d28d9', lw=1.3), zorder=6)

    draw_arrow(ax, 0.8655, 0.180, 0.8655, 0.292, color='#10b981', lw=2.3, ls='--', zorder=5)
    ax.text(0.8655, 0.237, '↑ 越级直报专线',
            ha='center', va='center', color='#6ee7b7', fontsize=9.7, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.28', facecolor='#0b1917', edgecolor='#059669', lw=1.3), zorder=6)

    # ==========================================================================
    # TIER 4: Corporate Officers & Direct Compliance Line [0.056 -> 0.190] (h = 0.134, mid = 0.123)
    # ==========================================================================
    draw_tray(ax, 0.080, 0.056, 0.900, 0.134, facecolor='#0e1320', edgecolor='#312e81', lw=1.5)

    draw_box(ax, 0.092, 0.066, 0.556, 0.114,
             '公司高管团队（Officers：总裁兼 CEO 黄仁勋 ＋ CFO Colette Kress 等）',
             '• 法律身份：受雇于董事会的全职经营官，负责芯片研发与日常管理（CFO 等高管并非董事）\n• 任免实例：平时获授权冲锋；11.11 董事会接下辞呈由 CFO 暂代，11.23 国安警报解除后全票复职',
             facecolor='#181826', edgecolor='#a855f7', title_color='#e9d5ff', title_size=11.5, body_size=9.3)

    draw_box(ax, 0.736, 0.066, 0.232, 0.114,
             '双轨合规防线（2026.11 新增）',
             '内部国安与全球贸易合规团队：\n日常向高管层汇报，同时绕开管理层\n直接向第四委员会（全独董）汇报',
             facecolor='#132421', edgecolor='#34d399', title_color='#d1fae5', title_size=10.8, body_size=9.0)

    # Clean horizontal routine reporting link in [0.648 -> 0.736]
    draw_arrow(ax, 0.732, 0.113, 0.652, 0.113, color='#94a3b8', lw=1.9, zorder=5)
    ax.text(0.692, 0.135, '日常汇报', ha='center', va='center', color='#cbd5e1', fontsize=9.0, fontweight='bold', zorder=5)

    # Footer note
    ax.text(0.51, 0.022, '注：持股比例与委员会架构依据英伟达 2026 年 5 月 12 日 SEC DEF 14A 代理声明书及 2026 年 7 月、11 月系列 Form 8-K 公告核实整理。',
            ha='center', va='center', color='#64748b', fontsize=9.0)

    out_path = os.path.join(out_dir, 'ep01_nvidia_board_power_architecture.png')
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight', pad_inches=0.25)
    plt.close(fig)
    print(f"Saved Chart 1 to: {out_path}")


# ==============================================================================
# CHART 2: 百年危机打补丁史 ＋ 美股独立董事的“平时放权 vs 战时拉闸”（大字号饱满版）
# ==============================================================================
def create_chart_2():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16.0, 9.2), dpi=300, gridspec_kw={'width_ratios': [1.02, 1.0]})
    fig.patch.set_facecolor('#0b0f17')

    c_card = '#111827'
    c_text = '#f8fafc'
    c_muted = '#94a3b8'

    # --- Left Panel: 100-Year Evolution Ladder ---
    ax1.set_facecolor(c_card)
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.axis('off')

    panel1_border = FancyBboxPatch(
        (0.01, 0.01), 0.98, 0.98,
        boxstyle="round,pad=0.004,rounding_size=0.016",
        facecolor=c_card, edgecolor='#334155', linewidth=1.6, zorder=1
    )
    ax1.add_patch(panel1_border)

    ax1.text(0.5, 0.952, '左图：美股董事会百年进化史——四次危机催生的铁律',
             ha='center', va='center', color=c_text, fontsize=16.0, fontweight='bold', zorder=3)
    ax1.text(0.5, 0.905, '从“老板私人俱乐部”到“外部独董绝对控盘”，每一颗牙齿都是大丑闻逼出来的',
             ha='center', va='center', color=c_muted, fontsize=11.8, zorder=3)

    eras = [
        (0.685, '#38bdf8', '1932｜两权分离觉醒（Berle & Means 现代公司论）',
         '• 现实剧变：大型公司股权极度分散，成千上万小股民失去直接控制力\n'
         '• 核心命题：揭示“出钱股东”与“掌权经理人”利益背离，奠定董事会受托基石'),
        (0.468, '#f59e0b', '1996 & 2002｜安然造假崩盘与《萨班斯法案》(SOX)',
         '• 惨痛教训：安然、世通做假账崩盘，昔日熟人董事会沦为橡皮图章\n'
         '• 铁腕补丁：确立 Caremark 监督红线；强制独董过半、审计委员会 100% 独董'),
        (0.252, '#a855f7', '2010｜次贷危机与《多德-弗兰克法案》(Dodd-Frank)',
         '• 惨痛教训：华尔街高管靠短期豪赌拿天价奖金，公司暴雷后全身而退\n'
         '• 铁腕补丁：强制薪酬委员会 100% 独董，引入股东薪酬投票与错账奖金追回'),
        (0.036, '#10b981', '2020s–2026｜地缘科技合规与“董事长—CEO 分权”',
         '• 标普趋势：约 61% 成分股拆分董事长与 CEO 两职（41% 设独立董事长）\n'
         '• 英伟达样本：2026.11 首设独立董事长，并新建全独董“国安与出口管制委员会”')
    ]

    for y_pos, col, t_str, b_str in eras:
        card = FancyBboxPatch(
            (0.028, y_pos), 0.944, 0.182,
            boxstyle="round,pad=0.005,rounding_size=0.014",
            facecolor='#161e2e', edgecolor=col, linewidth=1.9, zorder=2
        )
        ax1.add_patch(card)
        ax1.text(0.045, y_pos + 0.142, t_str, ha='left', va='center',
                 color=col, fontsize=14.4, fontweight='bold', zorder=3)
        ax1.text(0.045, y_pos + 0.062, b_str, ha='left', va='center',
                 color='#e2e8f0', fontsize=12.8, linespacing=1.82, zorder=3)

    for y_top in (0.685, 0.468, 0.252):
        draw_arrow(ax1, 0.50, y_top - 0.005, 0.50, y_top - 0.029, color='#94a3b8', lw=2.2)

    # --- Right Panel: Dual-Mode Operating Mechanism of Independent Directors ---
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

    ax2.text(0.5, 0.952, '右图：美股独董的“双态开关”——平时放权 vs 战时拉闸',
             ha='center', va='center', color=c_text, fontsize=16.0, fontweight='bold', zorder=3)
    ax2.text(0.5, 0.905, '为什么年领约 35 万美元津贴的“兼职外人”，平时不微操、危机时却六亲不认？',
             ha='center', va='center', color=c_muted, fontsize=11.8, zorder=3)

    # Peacetime Box (Top)
    peacetime_box = FancyBboxPatch(
        (0.028, 0.554), 0.944, 0.312,
        boxstyle="round,pad=0.005,rounding_size=0.016",
        facecolor='#0f2229', edgecolor='#06b6d4', linewidth=2.1, zorder=2
    )
    ax2.add_patch(peacetime_box)
    ax2.text(0.045, 0.824, '【常态模式】商业判断准则保护伞（Business Judgment Rule）',
             ha='left', va='center', color='#67e8f9', fontsize=14.4, fontweight='bold', zorder=3)
    peacetime_body = (
        '• 适用场景：日常芯片研发、百亿资本开支、市场竞争与并购战略\n'
        '• 独董动作：每年开数次例会与闭门会，审视战略与薪酬，绝不微操\n'
        '• 法院铁律：只要无利益输送且程序知情，法官绝不“事后诸葛亮”\n'
        '• 现实效果：哪怕新业务亏掉百亿，独董 0 赔偿 → 给足试错空间'
    )
    ax2.text(0.045, 0.678, peacetime_body, ha='left', va='center',
             color='#e2e8f0', fontsize=13.0, linespacing=1.88, zorder=3)

    # Trigger Switch Banner (Middle)
    draw_arrow(ax2, 0.50, 0.548, 0.50, 0.516, color='#f43f5e', lw=2.3)
    switch_box = FancyBboxPatch(
        (0.034, 0.434), 0.932, 0.076,
        boxstyle="round,pad=0.005,rounding_size=0.014",
        facecolor='#2b141d', edgecolor='#f43f5e', linewidth=1.9, zorder=3
    )
    ax2.add_patch(switch_box)
    ax2.text(0.50, 0.472, '↓ 触发造假、违法或国安“红旗警报 (Red Flags)”：瞬间切换战时 ↓',
             ha='center', va='center', color='#fda4af', fontsize=12.6, fontweight='bold', zorder=4)
    draw_arrow(ax2, 0.50, 0.428, 0.50, 0.396, color='#f43f5e', lw=2.3)

    # Wartime Box (Bottom)
    wartime_box = FancyBboxPatch(
        (0.028, 0.036), 0.944, 0.354,
        boxstyle="round,pad=0.005,rounding_size=0.016",
        facecolor='#23151d', edgecolor='#fb7185', linewidth=2.1, zorder=2
    )
    ax2.add_patch(wartime_box)
    ax2.text(0.045, 0.348, '【战时模式】Caremark 监督红线与个人连带追责倒逼',
             ha='left', va='center', color='#fda4af', fontsize=14.4, fontweight='bold', zorder=3)
    wartime_body = (
        '• 致命代价：见红旗装瞎或包庇，即属“恶意失职 (Bad Faith)”，\n'
        '  免责伞作废！股东可发起衍生诉讼，独董面临声誉破产与连带索赔\n'
        '• 法定动作：隔离涉事 CEO → 设独董特别委员会 → 聘外部律所彻查\n'
        '• 英伟达闭环：11.08 独立调查 → 11.11 接辞呈 → 11.17 设国安委\n'
        '  → 11.23 获政府确认消除国安风险后全票迎回（保统帅＋守免责线）'
    )
    ax2.text(0.045, 0.180, wartime_body, ha='left', va='center',
             color='#e2e8f0', fontsize=12.7, linespacing=1.74, zorder=3)

    plt.tight_layout(pad=1.5)
    out_path = os.path.join(out_dir, 'ep01_us_board_evolution_and_dual_mode.png')
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight', pad_inches=0.25)
    plt.close(fig)
    print(f"Saved Chart 2 to: {out_path}")


if __name__ == "__main__":
    create_chart_1()
    create_chart_2()
