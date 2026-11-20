#!/usr/bin/env python3
"""
Generate dual-panel comparison chart for Episode 14:
Costco (COST, FY21-FY26) vs Target (TGT, FY20-FY25 ended Jan 2021 - Jan 2026).
All figures strictly sourced from audited SEC Form 10-K filings.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

# Configure macOS CJK fonts cleanly with dark theme styling
plt.rcParams["font.sans-serif"] = ["PingFang SC", "Heiti SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

BG_FIG = "#0b0f19"
BG_AX = "#111827"
GRID_COLOR = "#1f2937"
TEXT_MAIN = "#f3f4f6"
TEXT_MUTED = "#9ca3af"
BORDER_COLOR = "#374151"

# Distinct accessible color families matching dark buyer-research aesthetic
COST_BAR = "#2563eb"
COST_LINE = "#60a5fa"
TGT_BAR = "#d97706"
TGT_LINE = "#fbbf24"
THRESH_COLOR = "#10b981"

PERIODS = [
    "2021周期\nCOST21/TGT20",
    "2022周期\nCOST22/TGT21",
    "2023周期\nCOST23/TGT22",
    "2024周期\nCOST24/TGT23",
    "2025周期\nCOST25/TGT24",
    "2026周期\nCOST26/TGT25",
]

# Left Panel: Merchandise Sales per Sq.Ft. ($/Sq.Ft.) & Reported Gross Margin (%)
COST_PSF = [1615, 1818, 1882, 1907, 2004, 2143]
TGT_PSF = [382, 430, 440, 430, 422, 410]

COST_GM = [11.13, 10.48, 10.57, 10.92, 11.12, 11.09]
TGT_GM = [28.4, 28.3, 23.6, 27.5, 28.2, 27.9]

# Right Panel: Inventory Turnover Days (DIO) & Accounts Payable / Inventory Coverage (%)
COST_DIO = [30.4, 32.8, 28.6, 30.6, 27.6, 26.7]
TGT_DIO = [58.8, 67.7, 59.9, 55.7, 60.8, 59.5]

COST_AP_COV = [114.5, 99.7, 105.0, 104.2, 109.2, 116.9]
TGT_AP_COV = [120.7, 111.3, 99.9, 101.8, 102.5, 102.6]

PILL_BBOX = dict(boxstyle="round,pad=0.18", facecolor="#0b0f19", edgecolor="none", alpha=0.86)


def main():
    out_path = Path(__file__).resolve().parent.parent / "assets" / "cost_vs_tgt_metrics_trend.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20.5, 9.4), dpi=300)
    fig.patch.set_facecolor(BG_FIG)

    x = np.arange(len(PERIODS))

    # ------------------------------------------------------------------
    # Left Panel: Sales per Sq.Ft. ($/Sq.Ft.) + Reported Gross Margin (%)
    # ------------------------------------------------------------------
    ax1.set_facecolor(BG_AX)
    ax1_r = ax1.twinx()

    bw1 = 0.34
    b_cost = ax1.bar(
        x - bw1 / 2,
        COST_PSF,
        width=bw1,
        color=COST_BAR,
        alpha=0.88,
        label="COST 好市多坪效 ($/Sq.Ft.)",
        zorder=2,
    )
    b_tgt = ax1.bar(
        x + bw1 / 2,
        TGT_PSF,
        width=bw1,
        color=TGT_BAR,
        alpha=0.88,
        label="TGT 塔吉特坪效 ($/Sq.Ft.)",
        zorder=2,
    )

    # Scale axes so COST bars <= 56%, TGT GM line stays cleanly in 60%..73%, and legend sits in 84%..98%
    ax1.set_ylim(0, 3850)
    ax1_r.set_ylim(0, 39.0)

    ax1_r.plot(
        x,
        TGT_GM,
        color=TGT_LINE,
        marker="s",
        markersize=7,
        linewidth=2.6,
        linestyle="--",
        label="TGT 报告毛利率 (%)",
        zorder=5,
    )
    ax1_r.plot(
        x,
        COST_GM,
        color=COST_LINE,
        marker="o",
        markersize=7,
        linewidth=2.6,
        label="COST 商品毛利率 (%)",
        zorder=5,
    )

    for rect in b_cost:
        h = rect.get_height()
        ax1.text(
            rect.get_x() + rect.get_width() / 2,
            h + 45,
            f"${h:,}",
            ha="center",
            va="bottom",
            fontsize=8.6,
            color="#bfdbfe",
            fontweight="bold",
        )
    for rect in b_tgt:
        h = rect.get_height()
        ax1.text(
            rect.get_x() + rect.get_width() / 2,
            h + 45,
            f"${h:,}",
            ha="center",
            va="bottom",
            fontsize=8.6,
            color="#fde68a",
            fontweight="bold",
        )

    for idx, (c_gm, t_gm) in enumerate(zip(COST_GM, TGT_GM)):
        # TGT GM sits above COST bars except minor approach in FY23 (23.6%)
        ax1_r.annotate(
            f"{t_gm:.1f}%",
            xy=(x[idx], t_gm),
            xytext=(0, 9),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9.0,
            color=TGT_LINE,
            fontweight="bold",
            bbox=PILL_BBOX,
            zorder=6,
        )
        # COST GM (~11%) shifts right into open space above low amber TGT bar
        ax1_r.annotate(
            f"{c_gm:.1f}%",
            xy=(x[idx], c_gm),
            xytext=(22, 6),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8.8,
            color=COST_LINE,
            fontweight="bold",
            bbox=PILL_BBOX,
            zorder=6,
        )

    ax1.set_title(
        "每平方英尺坪效 ($/Sq.Ft.) 与商品毛利率 (%)",
        fontsize=13.5,
        fontweight="bold",
        color=TEXT_MAIN,
        pad=14,
    )
    ax1.set_xticks(x)
    ax1.set_xticklabels(PERIODS, fontsize=9.6, color=TEXT_MAIN)
    ax1.set_ylabel("每平方英尺年商品净销售额 ($/Sq.Ft.)", fontsize=10.5, color=TEXT_MUTED)
    ax1_r.set_ylabel("商品毛利率 (%)", fontsize=10.5, color=TEXT_MUTED)
    ax1.yaxis.set_major_formatter(mticker.StrMethodFormatter("${x:,.0f}"))
    ax1_r.yaxis.set_major_formatter(mticker.FormatStrFormatter("%d%%"))
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
        loc="upper left",
        ncol=2,
        frameon=True,
        facecolor="#0f172a",
        edgecolor=BORDER_COLOR,
        fontsize=8.8,
        labelcolor=TEXT_MAIN,
    )

    # ------------------------------------------------------------------
    # Right Panel: Inventory Turnover Days (DIO) + AP / Inventory Coverage (%)
    # ------------------------------------------------------------------
    ax2.set_facecolor(BG_AX)
    ax2_r = ax2.twinx()

    bw2 = 0.34
    b2_cost = ax2.bar(
        x - bw2 / 2,
        COST_DIO,
        width=bw2,
        color=COST_BAR,
        alpha=0.86,
        label="COST 存货周转天数 DIO (天)",
        zorder=2,
    )
    b2_tgt = ax2.bar(
        x + bw2 / 2,
        TGT_DIO,
        width=bw2,
        color=TGT_BAR,
        alpha=0.86,
        label="TGT 存货周转天数 DIO (天)",
        zorder=2,
    )

    # DIO bars stay below ~41%, while AP/Inventory 99.7%..120.7% stay in 52%..75% height
    ax2.set_ylim(0, 175)
    ax2_r.set_ylim(50, 145)

    ax2_r.axhline(
        100.0,
        color=THRESH_COLOR,
        linestyle=":",
        linewidth=1.6,
        alpha=0.88,
        label="应付/存货 = 100% 占款分水岭",
        zorder=3,
    )

    ax2_r.plot(
        x,
        COST_AP_COV,
        color=COST_LINE,
        marker="o",
        markersize=7,
        linewidth=2.6,
        label="COST 应付账款/存货覆盖率 (%)",
        zorder=5,
    )
    ax2_r.plot(
        x,
        TGT_AP_COV,
        color=TGT_LINE,
        marker="s",
        markersize=7,
        linewidth=2.6,
        linestyle="--",
        label="TGT 应付账款/存货覆盖率 (%)",
        zorder=5,
    )

    for rect in b2_cost:
        h = rect.get_height()
        ax2.text(
            rect.get_x() + rect.get_width() / 2,
            h + 1.5,
            f"{h:.1f}天",
            ha="center",
            va="bottom",
            fontsize=8.5,
            color="#bfdbfe",
            fontweight="bold",
        )
    for rect in b2_tgt:
        h = rect.get_height()
        ax2.text(
            rect.get_x() + rect.get_width() / 2,
            h + 1.5,
            f"{h:.1f}天",
            ha="center",
            va="bottom",
            fontsize=8.5,
            color="#fde68a",
            fontweight="bold",
        )

    for idx, (c_cov, t_cov) in enumerate(zip(COST_AP_COV, TGT_AP_COV)):
        if c_cov >= t_cov:
            c_y, c_va = 9, "bottom"
            t_y, t_va = -13, "top"
        else:
            t_y, t_va = 9, "bottom"
            c_y, c_va = -13, "top"

        ax2_r.annotate(
            f"{c_cov:.1f}%",
            xy=(x[idx], c_cov),
            xytext=(0, c_y),
            textcoords="offset points",
            ha="center",
            va=c_va,
            fontsize=8.8,
            color=COST_LINE,
            fontweight="bold",
            bbox=PILL_BBOX,
            zorder=6,
        )
        ax2_r.annotate(
            f"{t_cov:.1f}%",
            xy=(x[idx], t_cov),
            xytext=(0, t_y),
            textcoords="offset points",
            ha="center",
            va=t_va,
            fontsize=8.8,
            color=TGT_LINE,
            fontweight="bold",
            bbox=PILL_BBOX,
            zorder=6,
        )

    ax2.set_title(
        "存货周转效率 (DIO 天数) 与应付账款占款覆盖率 (AP/Inv %)",
        fontsize=13.5,
        fontweight="bold",
        color=TEXT_MAIN,
        pad=14,
    )
    ax2.set_xticks(x)
    ax2.set_xticklabels(PERIODS, fontsize=9.6, color=TEXT_MAIN)
    ax2.set_ylabel("期末存货周转天数 DIO (天)", fontsize=10.5, color=TEXT_MUTED)
    ax2_r.set_ylabel("期末应付账款 ÷ 存货覆盖率 (%)", fontsize=10.5, color=TEXT_MUTED)
    ax2.yaxis.set_major_formatter(mticker.FormatStrFormatter("%d天"))
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
        fontsize=8.8,
        labelcolor=TEXT_MAIN,
    )

    fig.suptitle(
        "线下商超与会员制零售双标本跨周期对决：好市多 COST vs 塔吉特 TGT（6 周期 10-K 原生对账）",
        fontsize=16.0,
        fontweight="bold",
        color=TEXT_MAIN,
        y=0.97,
    )

    fig.text(
        0.5,
        0.015,
        "数据来源：好市多 (COST) FY2021–FY2026 SEC Form 10-K（8 月末财年）、塔吉特 (TGT) FY2020–FY2025 SEC Form 10-K（21/01止 至 26/01止）。",
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
