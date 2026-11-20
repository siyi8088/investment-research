import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['STHeiti', 'Arial Unicode MS', 'PingFang HK', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False


def bond_price(c_annual, y_annual, n_periods):
    i = y_annual / 2.0
    c_semi = 100.0 * (c_annual / 2.0)
    if np.isscalar(i):
        if i == 0:
            return c_semi * n_periods + 100.0
    vn = (1.0 + i) ** (-n_periods)
    an = (1.0 - vn) / i
    return c_semi * an + 100.0 * vn


def bond_metrics(c_annual, y_annual, n_periods):
    i = y_annual / 2.0
    c_semi = 100.0 * (c_annual / 2.0)
    k = np.arange(1, n_periods + 1, dtype=float)
    cfs = np.full(n_periods, c_semi, dtype=float)
    cfs[-1] += 100.0
    pvs = cfs / ((1.0 + i) ** k)
    p = float(np.sum(pvs))
    t_yrs = k / 2.0
    d_mac = float(np.sum(t_yrs * pvs) / p)
    d_mod = d_mac / (1.0 + i)
    return p, d_mac, d_mod, pvs, t_yrs


def make_chart_1_tangent():
    """生成配图1：久期一阶线性近似（切线）vs. 真实价格曲线与误差拆解图"""
    c30, y0_30, n30 = 0.05125, 0.05216, 60
    p0_30, dm_30, dmod_30, _, _ = bond_metrics(c30, y0_30, n30)

    c10, y0_10, n10 = 0.04625, 0.04683, 20
    p0_10, dm_10, dmod_10, _, _ = bond_metrics(c10, y0_10, n10)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6.4), dpi=300)
    fig.patch.set_facecolor('#F8FAFC')

    # --- 左图：30Y 真实曲线 vs 一阶切线 ---
    ax1.set_facecolor('#FFFFFF')
    ys = np.linspace(0.018, 0.088, 300)
    p_exact_curve = np.array([bond_price(c30, y, n30) for y in ys])
    p_tangent_line = p0_30 * (1.0 - dmod_30 * (ys - y0_30))

    ax1.plot(ys * 100, p_exact_curve, color='#0369A1', linewidth=3.0, label='真实折现价格曲线 P(y)')
    ax1.plot(ys * 100, p_tangent_line, color='#D97706', linewidth=2.4, linestyle='--', label=f'久期一阶切线 (斜率 = -D_Mod×P0)')

    # 切点
    ax1.scatter([y0_30 * 100], [p0_30], color='#0F172A', s=65, zorder=6)
    ax1.annotate(
        f'当前切点\n(y0={y0_30*100:.3f}%, P0={p0_30:.2f})',
        xy=(y0_30 * 100, p0_30),
        xytext=(y0_30 * 100 - 1.35, 62.0),
        fontsize=9.2, fontweight='bold', color='#0F172A',
        arrowprops=dict(arrowstyle='->', color='#475569', lw=1.3),
        bbox=dict(boxstyle='round,pad=0.3', fc='#F1F5F9', ec='#CBD5E1')
    )

    # -200 bps 点对比
    y_dn = y0_30 - 0.02
    p_ex_dn = bond_price(c30, y_dn, n30)
    p_ap_dn = p0_30 * (1.0 - dmod_30 * (-0.02))
    ax1.plot([y_dn * 100, y_dn * 100], [p_ap_dn, p_ex_dn], color='#059669', linewidth=3.0)
    ax1.scatter([y_dn * 100, y_dn * 100], [p_ex_dn, p_ap_dn], color=['#0369A1', '#D97706'], s=55, zorder=6)
    ax1.annotate(
        f'降息 -200 bps (y={y_dn*100:.3f}%)\n真实上涨至 {p_ex_dn:.2f}\n切线仅预测 {p_ap_dn:.2f}\n多涨 +{p_ex_dn - p_ap_dn:.2f} 美元',
        xy=(y_dn * 100, (p_ex_dn + p_ap_dn) / 2),
        xytext=(y_dn * 100 + 0.35, 152.0),
        fontsize=8.8, fontweight='bold', color='#065F46',
        arrowprops=dict(arrowstyle='->', color='#059669', lw=1.5),
        bbox=dict(boxstyle='round,pad=0.35', fc='#ECFDF5', ec='#6EE7B7')
    )

    # +200 bps 点对比
    y_up = y0_30 + 0.02
    p_ex_up = bond_price(c30, y_up, n30)
    p_ap_up = p0_30 * (1.0 - dmod_30 * 0.02)
    ax1.plot([y_up * 100, y_up * 100], [p_ap_up, p_ex_up], color='#059669', linewidth=3.0)
    ax1.scatter([y_up * 100, y_up * 100], [p_ex_up, p_ap_up], color=['#0369A1', '#D97706'], s=55, zorder=6)
    ax1.annotate(
        f'加息 +200 bps (y={y_up*100:.3f}%)\n真实仅跌至 {p_ex_up:.2f}\n切线过度预测跌至 {p_ap_up:.2f}\n少跌 +{p_ex_up - p_ap_up:.2f} 美元',
        xy=(y_up * 100, (p_ex_up + p_ap_up) / 2),
        xytext=(y_up * 100 - 1.35, 110.0),
        fontsize=8.8, fontweight='bold', color='#065F46',
        arrowprops=dict(arrowstyle='->', color='#059669', lw=1.5),
        bbox=dict(boxstyle='round,pad=0.35', fc='#ECFDF5', ec='#6EE7B7')
    )

    ax1.set_title('① 30年期美债 (912810UW6) 价格曲线 vs. 一阶切线', fontsize=12.5, fontweight='bold', color='#1E293B', pad=12)
    ax1.set_xlabel('市场到期收益率 y (%)', fontsize=10.5, color='#334155')
    ax1.set_ylabel('每百元面值价格 P (美元)', fontsize=10.5, color='#334155')
    ax1.set_xlim(1.7, 8.8)
    ax1.set_ylim(45, 195)
    ax1.grid(True, linestyle='--', alpha=0.35, color='#94A3B8')
    ax1.legend(loc='upper right', frameon=True, facecolor='#F8FAFC', edgecolor='#E2E8F0', fontsize=9.5)

    # --- 右图：切线误差曲线 (Error = dP_exact - dP_approx) ---
    ax2.set_facecolor('#FFFFFF')
    dy_bps = np.linspace(-200, 200, 201)
    dy = dy_bps / 10000.0
    err_30 = np.array([bond_price(c30, y0_30 + d, n30) - p0_30 * (1.0 - dmod_30 * d) for d in dy])
    err_10 = np.array([bond_price(c10, y0_10 + d, n10) - p0_10 * (1.0 - dmod_10 * d) for d in dy])

    ax2.axvspan(-10, 10, color='#10B981', alpha=0.16, label='日内高精度安全区 (|Δy| ≤ 10 bps, 误差 < 0.02 美元)')
    ax2.plot(dy_bps, err_30, color='#0369A1', linewidth=2.8, label='30Y 国债 912810UW6 切线误差')
    ax2.plot(dy_bps, err_10, color='#D97706', linewidth=2.5, linestyle='-.', label='10Y 国债 91282CRF0 切线误差')
    ax2.axhline(0, color='#64748B', linewidth=1.0, linestyle=':')

    # 标注极值
    ax2.scatter([-200, 200], [err_30[0], err_30[-1]], color='#0369A1', s=45, zorder=5)
    ax2.annotate(f'+{err_30[0]:.2f} 美元', xy=(-200, err_30[0]), xytext=(-180, err_30[0] - 0.55),
                 fontsize=9.5, fontweight='bold', color='#0369A1')
    ax2.annotate(f'+{err_30[-1]:.2f} 美元', xy=(200, err_30[-1]), xytext=(125, err_30[-1] + 0.35),
                 fontsize=9.5, fontweight='bold', color='#0369A1')

    ax2.annotate('两翼恒大于零：\n曲线永远位于切线上方\n(第06讲将用二阶“凸性”补全)',
                 xy=(0, 2.2), ha='center', fontsize=9.5, color='#334155',
                 bbox=dict(boxstyle='round,pad=0.35', fc='#F8FAFC', ec='#CBD5E1'))

    ax2.set_title('② 不同利率冲击下的切线近似误差 (真实变动 - 切线预测)', fontsize=12.5, fontweight='bold', color='#1E293B', pad=12)
    ax2.set_xlabel('收益率平行冲击 Δy (bps)', fontsize=10.5, color='#334155')
    ax2.set_ylabel('近似误差 ΔP_exact - ΔP_approx (美元/百元)', fontsize=10.5, color='#334155')
    ax2.set_xlim(-215, 215)
    ax2.set_ylim(-0.4, 9.0)
    ax2.grid(True, linestyle='--', alpha=0.35, color='#94A3B8')
    ax2.legend(loc='upper center', frameon=True, facecolor='#F8FAFC', edgecolor='#E2E8F0', fontsize=9.0)

    plt.tight_layout(pad=2.5)
    out1 = '/Users/siyi/Documents/code/investment-research/articles/us_treasury_guide/assets/05_duration_tangent_approximation.png'
    plt.savefig(out1, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close(fig)
    print('Saved:', out1)


def make_chart_2_balance_ceiling():
    """生成配图2：现金流天平重心与永续债久期天花板全景图"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6.4), dpi=300)
    fig.patch.set_facecolor('#F8FAFC')

    # --- 左图：10Y 国债现金流现值分布与天平支点 (D_Mac = 8.11 年) ---
    ax1.set_facecolor('#FFFFFF')
    p10, dm10, _, pvs10, t10 = bond_metrics(0.04625, 0.04683, 20)
    weights10 = (pvs10 / p10) * 100.0

    bars = ax1.bar(t10, weights10, width=0.34, color='#38BDF8', edgecolor='#0284C7', alpha=0.9, label='每半年票息现值权重 w_k (%)')
    bars[-1].set_color('#0369A1')
    bars[-1].set_edgecolor('#0F172A')
    bars[-1].set_label(f'第10年末本金+末期票息权重 ({weights10[-1]:.2f}%)')

    # 画出天平支点与期限对比线
    ax1.axvline(dm10, color='#D97706', linewidth=2.6, linestyle='--', label=f'麦考利久期重心 D_Mac = {dm10:.2f} 年')
    ax1.scatter([dm10], [2.2], marker='^', s=240, color='#D97706', zorder=7)
    ax1.annotate(
        f'天平支点 (重心)\nD_Mac = {dm10:.2f} 年\n(第04讲 8.11 年免疫点)',
        xy=(dm10, 4.5), xytext=(4.2, 22.0),
        fontsize=9.5, fontweight='bold', color='#B45309',
        arrowprops=dict(arrowstyle='->', color='#D97706', lw=1.6),
        bbox=dict(boxstyle='round,pad=0.35', fc='#FFFBEB', ec='#FCD34D')
    )
    ax1.annotate(
        f'到期日 T = 10.0 年\n(单笔回收占总现值 {weights10[-1]:.1f}%)',
        xy=(10.0, weights10[-1]), xytext=(5.5, 52.0),
        fontsize=9.5, fontweight='bold', color='#0369A1',
        arrowprops=dict(arrowstyle='->', color='#0369A1', lw=1.4),
        bbox=dict(boxstyle='round,pad=0.3', fc='#F0F9FF', ec='#BAE6FD')
    )

    ax1.set_title('① 10年期国债 (91282CRF0) 现金流现值天平与麦考利重心', fontsize=12.5, fontweight='bold', color='#1E293B', pad=12)
    ax1.set_xlabel('未来收款时间 t (年)', fontsize=10.5, color='#334155')
    ax1.set_ylabel('单期现金流占总价格权重 w_k (%)', fontsize=10.5, color='#334155')
    ax1.set_xlim(0, 10.8)
    ax1.set_ylim(0, 73)
    ax1.grid(axis='y', linestyle='--', alpha=0.35, color='#94A3B8')
    ax1.legend(loc='upper left', frameon=True, facecolor='#F8FAFC', edgecolor='#E2E8F0', fontsize=9.0)

    # --- 右图：不同票息率下修正久期随期限的变化与永续债天花板 (y = 5.000%) ---
    ax2.set_facecolor('#FFFFFF')
    t_grid = np.arange(1, 101, 1)
    y_bench = 0.05

    for c_val, col, ls, lbl in [
        (0.000, '#64748B', ':', '零息债 c = 0.0% (D_Mod 与期限线性同步扩张)'),
        (0.025, '#0EA5E9', '-.', '折价低息债 c = 2.5%'),
        (0.050, '#0369A1', '-', '平价基准债 c = 5.0%'),
        (0.075, '#059669', '--', '溢价高息债 c = 7.5%'),
    ]:
        dmods = [bond_metrics(c_val, y_bench, int(t * 2))[2] for t in t_grid]
        ax2.plot(t_grid, dmods, color=col, linestyle=ls, linewidth=2.5, label=lbl)

    ax2.axhline(20.0, color='#DC2626', linewidth=2.2, linestyle='--', label='永续债修正久期极限 D_Mod,∞ = 1/y = 20.00 年')
    ax2.annotate(
        '任何正票息国债在 y=5% 时\n当期限 T→∞ 最终均收敛于 20.0 年\n(注: 折价低息债会先小幅超过 20.0 后回落收敛)',
        xy=(82, 20.0), xytext=(30, 25.0),
        fontsize=8.8, fontweight='bold', color='#B91C1C',
        arrowprops=dict(arrowstyle='->', color='#DC2626', lw=1.4),
        bbox=dict(boxstyle='round,pad=0.3', fc='#FEF2F2', ec='#FECACA')
    )

    ax2.set_title('② 久期三大定律：期限越长越平缓，最终锁死在永续天花板 (y=5.0%)', fontsize=12.5, fontweight='bold', color='#1E293B', pad=12)
    ax2.set_xlabel('债券剩余到期期限 T (年)', fontsize=10.5, color='#334155')
    ax2.set_ylabel('修正久期 D_Mod (年)', fontsize=10.5, color='#334155')
    ax2.set_xlim(0, 102)
    ax2.set_ylim(0, 35)
    ax2.grid(True, linestyle='--', alpha=0.35, color='#94A3B8')
    ax2.legend(loc='lower right', frameon=True, facecolor='#F8FAFC', edgecolor='#E2E8F0', fontsize=8.8)

    plt.tight_layout(pad=2.5)
    out2 = '/Users/siyi/Documents/code/investment-research/articles/us_treasury_guide/assets/05_duration_balance_and_ceiling.png'
    plt.savefig(out2, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close(fig)
    print('Saved:', out2)


if __name__ == '__main__':
    make_chart_1_tangent()
    make_chart_2_balance_ceiling()
