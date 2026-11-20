#!/usr/bin/env python3
"""
Generate dual-panel comparison chart for Episode 15:
McDonald's (MCD, FY21-26Q3) vs Chipotle Mexican Grill (CMG, FY21-26Q3).
All figures strictly sourced from audited SEC Form 10-K / Form 10-Q filings.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

# Configure macOS CJK fonts cleanly with dark institutional styling
plt.rcParams["font.sans-serif"] = ["PingFang SC", "Heiti SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

BG_FIG = "#0b0f19"
BG_AX = "#111827"
GRID_COLOR = "#1f2937"
TEXT_MAIN = "#f3f4f6"
TEXT_MUTED = "#9ca3af"
BORDER_COLOR = "#374151"

MCD_BAR = "#2563eb"
MCD_LINE = "#60a5fa"
CMG_BAR = "#d97706"
CMG_LINE = "#fbbf24"
THRESH_COLOR = "#10b981"

PERIODS = [
    "2021年\n(10-K)",
    "2022年\n(10-K)",
    "2023年\n(10-K)",
    "2024年\n(10-K)",
    "2025年\n(10-K)",
    "2026 Q3\n(最新单季)",
]

# Left Panel: Net Unit Growth YoY (%) & Comparable Restaurant Sales Growth (%)
# MCD total ending units YoY: 40,031/39,198 (+2.1%), 40,275 (+0.6%), 41,822 (+3.8%), 43,477 (+4.0%), 45,356 (+4.3%), 26Q3 46,554/44,599 (+4.4%)
MCD_UNIT_G = [2.1, 0.6, 3.8, 4.0, 4.3, 4.4]
# CMG company-owned ending units YoY: 2,966/2,768 (+7.2%), 3,187 (+7.5%), 3,437 (+7.8%), 3,726 (+8.4%), 4,042 (+8.5%), 26Q3 4,267/3,916 (+9.0%)
CMG_UNIT_G = [7.2, 7.5, 7.8, 8.4, 8.5, 9.0]

MCD_COMP = [17.0, 10.9, 9.0, -0.1, 3.1, 1.5]
CMG_COMP = [19.3, 8.0, 7.9, 7.4, -1.7, 2.1]

# Right Panel: G&A % of Systemwide Sales (%) & GAAP Operating Margin (%)
MCD_GA_SYS = [2.41, 2.42, 2.18, 2.19, 2.18, 1.99]
CMG_GA_SYS = [8.04, 6.53, 6.42, 6.16, 5.47, 5.62]

MCD_OPM = [44.6, 40.4, 45.7, 45.2, 46.1, 50.2]
CMG_OPM = [10.7, 13.4, 15.8, 16.9, 16.2, 13.7]

PILL_BBOX = dict(boxstyle="round,pad=0.18", facecolor="#0b0f19", edgecolor="none", alpha=0.88)


def main():
    out_path = Path(__file__).resolve().parent.parent / "assets" / "mcd_vs_cmg_metrics_trend.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20.5, 9.5), dpi=300)
    fig.patch.set_facecolor(BG_FIG)

    x = np.arange(len(PERIODS))
    bw = 0.34

    # ------------------------------------------------------------------
    # Left Panel: Net Unit Growth YoY (%) + Comparable Sales Growth (%)
    # ------------------------------------------------------------------
    ax1.set_facecolor(BG_AX)
    ax1_r = ax1.twinx()

    b_mcd_u = ax1.bar(
        x - bw / 2,
        MCD_UNIT_G,
        width=bw,
        color=MCD_BAR,
        alpha=0.88,
        label="MCD 全球门店净增速 YoY (%)",
        zorder=2,
    )
    b_cmg_u = ax1.bar(
        x + bw / 2,
        CMG_UNIT_G,
        width=bw,
        color=CMG_BAR,
        alpha=0.88,
        label="CMG 直营门店净增速 YoY (%)",
        zorder=2,
    )

    # Keep unit growth bars in bottom 0%..30% height, Comp lines in 38%..88% height
    ax1.set_ylim(0, 30.0)
    ax1_r.set_ylim(-18.0, 26.5)

    ax1_r.axhline(
        0.0,
        color=THRESH_COLOR,
        linestyle=":",
        linewidth=1.5,
        alpha=0.82,
        label="同店可比增速 0% 荣枯线",
        zorder=3,
    )

    ax1_r.plot(
        x,
        MCD_COMP,
        color=MCD_LINE,
        marker="o",
        markersize=7,
        linewidth=2.6,
        label="MCD 全球同店可比增速 (%)",
        zorder=5,
    )
    ax1_r.plot(
        x,
        CMG_COMP,
        color=CMG_LINE,
        marker="s",
        markersize=7,
        linewidth=2.6,
        linestyle="--",
        label="CMG 同店可比增速 (%)",
        zorder=5,
    )

    for rect in b_mcd_u:
        h = rect.get_height()
        ax1.text(
            rect.get_x() + rect.get_width() / 2,
            h + 0.35,
            f"+{h:.1f}%",
            ha="center",
            va="bottom",
            fontsize=8.3,
            color="#bfdbfe",
            fontweight="bold",
        )
    for rect in b_cmg_u:
        h = rect.get_height()
        ax1.text(
            rect.get_x() + rect.get_width() / 2,
            h + 0.35,
            f"+{h:.1f}%",
            ha="center",
            va="bottom",
            fontsize=8.3,
            color="#fde68a",
            fontweight="bold",
        )

    for idx, (m_c, c_c) in enumerate(zip(MCD_COMP, CMG_COMP)):
        if m_c >= c_c:
            m_y, m_va = 9, "bottom"
            c_y, c_va = -13, "top"
        else:
            c_y, c_va = 9, "bottom"
            m_y, m_va = -13, "top"
        # Prevent overlap when 2026 Q3 values (+1.5% vs +2.1%) sit close to 0% line
        if idx == 5:
            c_y, c_va = 11, "bottom"
            m_y, m_va = -14, "top"
        elif idx == 4:
            m_y, m_va = 10, "bottom"
            c_y, c_va = -12, "top"

        ax1_r.annotate(
            f"{m_c:+.1f}%",
            xy=(x[idx], m_c),
            xytext=(0, m_y),
            textcoords="offset points",
            ha="center",
            va=m_va,
            fontsize=8.8,
            color=MCD_LINE,
            fontweight="bold",
            bbox=PILL_BBOX,
            zorder=6,
        )
        ax1_r.annotate(
            f"{c_c:+.1f}%",
            xy=(x[idx], c_c),
            xytext=(0, c_y),
            textcoords="offset points",
            ha="center",
            va=c_va,
            fontsize=8.8,
            color=CMG_LINE,
            fontweight="bold",
            bbox=PILL_BBOX,
            zorder=6,
        )

    ax1.set_title(
        "扩店扩张节奏 (净门店增速 YoY %) 与同店内生增速 (Comp Sales %)",
        fontsize=13.2,
        fontweight="bold",
        color=TEXT_MAIN,
        pad=14,
    )
    ax1.set_xticks(x)
    ax1.set_xticklabels(PERIODS, fontsize=9.6, color=TEXT_MAIN)
    ax1.set_ylabel("期末门店净扩张增速 YoY (%)", fontsize=10.4, color=TEXT_MUTED)
    ax1_r.set_ylabel("同店可比销售增速 (%)", fontsize=10.4, color=TEXT_MUTED)
    ax1.yaxis.set_major_formatter(mticker.FormatStrFormatter("%d%%"))
    ax1_r.yaxis.set_major_formatter(mticker.FormatStrFormatter("%+d%%"))
    ax1.tick_params(axis="y", colors=TEXT_MUTED)
    ax1_r.tick_params(axis="y", colors=TEXT_MUTED)
    ax1.grid(axis="y", color=GRID_COLOR, linestyle="--", linewidth=0.7, zorder=0)

    ax1.spines["top"].set_visible(False)
    ax1_r.spines["top"].set_visible(False)
    for spine in ["bottom", "left", "right"]:
        ax1.spines[spine].set_color(BORDER_COLOR)
        ax1_r.spines[spine].set_color(BORDER_COLOR)

    h1, l1 = ax1.get_legend_handles_labels()
    h1r, l1r = ax1_r.get_legend_handles_labels()
    ax1.legend(
        h1 + h1r,
        l1 + l1r,
        loc="upper right",
        ncol=2,
        frameon=True,
        facecolor="#0f172a",
        edgecolor=BORDER_COLOR,
        fontsize=8.5,
        labelcolor=TEXT_MAIN,
    )

    # ------------------------------------------------------------------
    # Right Panel: G&A % of Systemwide Sales vs GAAP Operating Margin (%)
    # ------------------------------------------------------------------
    ax2.set_facecolor(BG_AX)
    ax2_r = ax2.twinx()

    b2_mcd = ax2.bar(
        x - bw / 2,
        MCD_GA_SYS,
        width=bw,
        color=MCD_BAR,
        alpha=0.86,
        label="MCD 总部费用 ÷ 体系流水 (%)",
        zorder=2,
    )
    b2_cmg = ax2.bar(
        x + bw / 2,
        CMG_GA_SYS,
        width=bw,
        color=CMG_BAR,
        alpha=0.86,
        label="CMG 总部费用 ÷ 总营收 (%)",
        zorder=2,
    )

    # Keep G&A/Systemwide bars below ~31% height, CMG OPM in ~39%..46%, threshold at ~55%, MCD OPM in ~72%..83%
    ax2.set_ylim(0, 26.0)
    ax2_r.set_ylim(-24.0, 65.0)

    ax2_r.axhline(
        25.0,
        color=THRESH_COLOR,
        linestyle=":",
        linewidth=1.6,
        alpha=0.88,
        label="25% 轻资产特许与纯直营营业利润率分水岭",
        zorder=3,
    )

    ax2_r.plot(
        x,
        MCD_OPM,
        color=MCD_LINE,
        marker="o",
        markersize=7,
        linewidth=2.6,
        label="MCD GAAP 营业利润率 (%)",
        zorder=5,
    )
    ax2_r.plot(
        x,
        CMG_OPM,
        color=CMG_LINE,
        marker="s",
        markersize=7,
        linewidth=2.6,
        linestyle="--",
        label="CMG GAAP 营业利润率 (%)",
        zorder=5,
    )

    for rect in b2_mcd:
        h = rect.get_height()
        ax2.text(
            rect.get_x() + rect.get_width() / 2,
            h + 0.3,
            f"{h:.2f}%",
            ha="center",
            va="bottom",
            fontsize=8.2,
            color="#bfdbfe",
            fontweight="bold",
        )
    for rect in b2_cmg:
        h = rect.get_height()
        ax2.text(
            rect.get_x() + rect.get_width() / 2,
            h + 0.3,
            f"{h:.2f}%",
            ha="center",
            va="bottom",
            fontsize=8.2,
            color="#fde68a",
            fontweight="bold",
        )

    for idx, (m_op, c_op) in enumerate(zip(MCD_OPM, CMG_OPM)):
        m_y = -15 if idx == 5 else 9
        m_va = "top" if idx == 5 else "bottom"
        ax2_r.annotate(
            f"{m_op:.1f}%",
            xy=(x[idx], m_op),
            xytext=(0, m_y),
            textcoords="offset points",
            ha="center",
            va=m_va,
            fontsize=8.9,
            color=MCD_LINE,
            fontweight="bold",
            bbox=PILL_BBOX,
            zorder=6,
        )
        ax2_r.annotate(
            f"{c_op:.1f}%",
            xy=(x[idx], c_op),
            xytext=(0, 8),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8.9,
            color=CMG_LINE,
            fontweight="bold",
            bbox=PILL_BBOX,
            zorder=6,
        )

    ax2.set_title(
        "总部费用体系杠杆 (G&A ÷ 体系流水 %) 与 GAAP 营业利润率 (%)",
        fontsize=13.2,
        fontweight="bold",
        color=TEXT_MAIN,
        pad=14,
    )
    ax2.set_xticks(x)
    ax2.set_xticklabels(PERIODS, fontsize=9.6, color=TEXT_MAIN)
    ax2.set_ylabel("总部费用占体系流水比例 (%)", fontsize=10.4, color=TEXT_MUTED)
    ax2_r.set_ylabel("GAAP 合并营业利润率 (%)", fontsize=10.4, color=TEXT_MUTED)
    ax2.yaxis.set_major_formatter(mticker.FormatStrFormatter("%d%%"))
    ax2_r.yaxis.set_major_formatter(mticker.FormatStrFormatter("%d%%"))
    ax2.tick_params(axis="y", colors=TEXT_MUTED)
    ax2_r.tick_params(axis="y", colors=TEXT_MUTED)
    ax2.grid(axis="y", color=GRID_COLOR, linestyle="--", linewidth=0.7, zorder=0)

    ax2.spines["top"].set_visible(False)
    ax2_r.spines["top"].set_visible(False)
    for spine in ["bottom", "left", "right"]:
        ax2.spines[spine].set_color(BORDER_COLOR)
        ax2_r.spines[spine].set_color(BORDER_COLOR)

    h2, l2 = ax2.get_legend_handles_labels()
    h2r, l2r = ax2_r.get_legend_handles_labels()
    ax2.legend(
        h2 + h2r,
        l2 + l2r,
        loc="upper left",
        ncol=2,
        frameon=True,
        facecolor="#0f172a",
        edgecolor=BORDER_COLOR,
        fontsize=8.5,
        labelcolor=TEXT_MAIN,
    )

    fig.suptitle(
        "连锁餐饮与特许经营帝国双标本跨周期对决：麦当劳 MCD vs 奇波雷 CMG（2021–2026 Q3 SEC 官方对账）",
        fontsize=15.8,
        fontweight="bold",
        color=TEXT_MAIN,
        y=0.97,
    )

    fig.text(
        0.5,
        0.015,
        "数据来源：麦当劳 (MCD) 与奇波雷 (CMG) 2021–2025 SEC Form 10-K 及 2026 Q3 Form 10-Q（截至 2026 年 9 月 30 日）。",
        ha="center",
        va="bottom",
        fontsize=9.0,
        color=TEXT_MUTED,
    )

    plt.tight_layout(rect=[0.01, 0.045, 0.99, 0.93], w_pad=3.2)
    fig.savefig(out_path, dpi=300, facecolor=BG_FIG)
    plt.close(fig)
    print(f"Saved chart to {out_path}")


if __name__ == "__main__":
    main()
