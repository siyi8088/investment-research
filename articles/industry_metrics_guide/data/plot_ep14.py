#!/usr/bin/env python3
"""
Generate dual-panel comparison chart for Episode 14:
Costco (COST) vs Walmart (WMT, including Sam's Club U.S.)
All figures strictly sourced from audited SEC Form 10-K filings (FY2021 - FY2026).
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
SAMS_BAR = "#059669"
WMT_BAR = "#d97706"
WMT_LINE = "#fbbf24"
THRESH_COLOR = "#10b981"

PERIODS = [
    "FY2021",
    "FY2022",
    "FY2023",
    "FY2024",
    "FY2025",
    "FY2026",
]

# Left Panel: Sales per Sq.Ft. ($/Sq.Ft.) & Merchandise Gross Margin (%)
COST_PSF = [1615, 1818, 1882, 1907, 2004, 2143]
SAMS_PSF = [799, 919, 1054, 1075, 1123, 1155]
WMT_PSF = [495, 536, 574, 610, 641, 668]

COST_GM = [11.13, 10.48, 10.57, 10.92, 11.12, 11.09]
WMT_GM = [24.30, 24.44, 23.46, 23.73, 24.13, 24.21]

# Right Panel: Inventory Turnover Days (DIO) & Accounts Payable / Inventory Coverage (%)
COST_DIO = [30.4, 32.8, 28.6, 30.6, 27.6, 26.7]
WMT_DIO = [39.0, 48.1, 44.5, 40.9, 40.3, 40.1]

COST_AP_COV = [114.5, 99.7, 105.0, 104.2, 109.2, 116.9]
WMT_AP_COV = [109.3, 97.8, 95.0, 103.5, 104.0, 107.2]

PILL_BBOX = dict(boxstyle="round,pad=0.18", facecolor="#0b0f19", edgecolor="none", alpha=0.85)


def main():
    out_path = Path(__file__).resolve().parent.parent / "assets" / "cost_vs_wmt_metrics_trend.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20.5, 9.4), dpi=300)
    fig.patch.set_facecolor(BG_FIG)

    x = np.arange(len(PERIODS))

    # ------------------------------------------------------------------
    # Left Panel: Sales per Sq.Ft. ($/Sq.Ft.) + Merchandise Gross Margin (%)
    # ------------------------------------------------------------------
    ax1.set_facecolor(BG_AX)
    ax1_r = ax1.twinx()

    bw1 = 0.25
    b_cost = ax1.bar(
        x - bw1,
        COST_PSF,
        width=bw1,
        color=COST_BAR,
        alpha=0.88,
        label="COST 好市多 坪效 ($/Sq.Ft.)",
        zorder=2,
    )
    b_sams = ax1.bar(
        x,
        SAMS_PSF,
        width=bw1,
        color=SAMS_BAR,
        alpha=0.88,
        label="山姆 Sam's Club U.S. 坪效 ($/Sq.Ft.)",
        zorder=2,
    )
    b_wmt = ax1.bar(
        x + bw1,
        WMT_PSF,
        width=bw1,
        color=WMT_BAR,
        alpha=0.88,
        label="WMT 沃尔玛全球综合 坪效 ($/Sq.Ft.)",
        zorder=2,
    )

    # Scale axes so lines stay cleanly above lower bars & below top headroom
    ax1.set_ylim(0, 3250)
    ax1_r.set_ylim(0, 32.0)

    ax1_r.plot(
        x,
        WMT_GM,
        color=WMT_LINE,
        marker="s",
        markersize=7,
        linewidth=2.6,
        linestyle="--",
        label="WMT 综合商品毛利率 (%)",
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

    # Direct bar labels
    for rect in b_cost:
        h = rect.get_height()
        ax1.text(
            rect.get_x() + rect.get_width() / 2,
            h + 32,
            f"${h:,}",
            ha="center",
            va="bottom",
            fontsize=8.3,
            color="#bfdbfe",
            fontweight="bold",
        )
    for idx, rect in enumerate(b_sams):
        h = rect.get_height()
        # COST GM% line (~11%) passes right across Sam's top edge in FY25-FY26;
        # center Sam's value vertically inside the green bar for 100% separation.
        ax1.text(
            rect.get_x() + rect.get_width() / 2,
            h * 0.52,
            f"${h:,}",
            ha="center",
            va="center",
            fontsize=8.1,
            color="#ecfdf5",
            fontweight="bold",
            zorder=4,
        )
    for rect in b_wmt:
        h = rect.get_height()
        ax1.text(
            rect.get_x() + rect.get_width() / 2,
            h + 30,
            f"${h:,}",
            ha="center",
            va="bottom",
            fontsize=8.1,
            color="#fde68a",
            fontweight="bold",
        )

    # Gross margin labels
    for idx, (c_gm, w_gm) in enumerate(zip(COST_GM, WMT_GM)):
        ax1_r.annotate(
            f"{w_gm:.1f}%",
            xy=(x[idx], w_gm),
            xytext=(0, 9),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9.0,
            color=WMT_LINE,
            fontweight="bold",
            bbox=PILL_BBOX,
            zorder=6,
        )
        # COST GM (~11% -> 1120 equiv): put above-right over dark gap above WMT bar
        ax1_r.annotate(
            f"{c_gm:.1f}%",
            xy=(x[idx], c_gm),
            xytext=(16, 8),
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
        "每平方英尺坪效 ($/Sq.Ft.) 与商品毛利率定价纪律 (%)",
        fontsize=13.5,
        fontweight="bold",
        color=TEXT_MAIN,
        pad=14,
    )
    ax1.set_xticks(x)
    ax1.set_xticklabels(PERIODS, fontsize=10.0, color=TEXT_MAIN)
    ax1.set_ylabel("每平方英尺年净销售额 ($/Sq.Ft.)", fontsize=10.5, color=TEXT_MUTED)
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
        fontsize=8.6,
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
    b2_wmt = ax2.bar(
        x + bw2 / 2,
        WMT_DIO,
        width=bw2,
        color=WMT_BAR,
        alpha=0.86,
        label="WMT 存货周转天数 DIO (天)",
        zorder=2,
    )

    # Set axis scales so DIO bars stay strictly in bottom <=37% and AP/Inv lines sit in 53%..80%
    ax2.set_ylim(0, 130)
    ax2_r.set_ylim(50, 136)

    ax2_r.axhline(
        100.0,
        color=THRESH_COLOR,
        linestyle=":",
        linewidth=1.5,
        alpha=0.85,
        label="AP/存货 = 100% 占款分水岭",
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
        WMT_AP_COV,
        color=WMT_LINE,
        marker="s",
        markersize=7,
        linewidth=2.6,
        linestyle="--",
        label="WMT 应付账款/存货覆盖率 (%)",
        zorder=5,
    )

    for rect in b2_cost:
        h = rect.get_height()
        ax2.text(
            rect.get_x() + rect.get_width() / 2,
            h + 1.2,
            f"{h:.1f}天",
            ha="center",
            va="bottom",
            fontsize=8.5,
            color="#bfdbfe",
            fontweight="bold",
        )
    for rect in b2_wmt:
        h = rect.get_height()
        ax2.text(
            rect.get_x() + rect.get_width() / 2,
            h + 1.2,
            f"{h:.1f}天",
            ha="center",
            va="bottom",
            fontsize=8.5,
            color="#fde68a",
            fontweight="bold",
        )

    for idx, (c_cov, w_cov) in enumerate(zip(COST_AP_COV, WMT_AP_COV)):
        ax2_r.annotate(
            f"{c_cov:.1f}%",
            xy=(x[idx], c_cov),
            xytext=(0, 9),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8.8,
            color=COST_LINE,
            fontweight="bold",
            bbox=PILL_BBOX,
            zorder=6,
        )
        # Keep WMT below its line when close to COST line (all years except 2023 are below by ~2-10pp)
        w_offset = -16 if idx != 1 else -17
        ax2_r.annotate(
            f"{w_cov:.1f}%",
            xy=(x[idx], w_cov),
            xytext=(0, w_offset),
            textcoords="offset points",
            ha="center",
            va="top",
            fontsize=8.8,
            color=WMT_LINE,
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
    ax2.set_xticklabels(PERIODS, fontsize=10.0, color=TEXT_MAIN)
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
        fontsize=8.6,
        labelcolor=TEXT_MAIN,
    )

    fig.suptitle(
        "线下商超与会员制零售双标本跨周期对决：好市多 COST vs 沃尔玛 WMT（含山姆会员店，FY2021–FY2026）",
        fontsize=16.0,
        fontweight="bold",
        color=TEXT_MAIN,
        y=0.97,
    )

    fig.text(
        0.5,
        0.015,
        "数据来源：好市多 (COST) FY2021–FY2026 SEC Form 10-K（8 月末财年）、沃尔玛 (WMT) FY2021–FY2026 SEC Form 10-K（1 月末财年，含 Sam's Club U.S. 分部）。",
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
