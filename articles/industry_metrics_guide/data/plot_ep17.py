#!/usr/bin/env python3
"""
Generate dual-panel comparison chart for Episode 17:
Freeport-McMoRan (FCX, FY21-26Q3) vs Southern Copper (SCCO, FY21-26Q3).
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

FCX_BAR = "#2563eb"
FCX_LINE = "#60a5fa"
SCCO_BAR = "#d97706"
SCCO_LINE = "#fbbf24"
THRESH_COLOR = "#10b981"

PERIODS = [
    "2021年\n(10-K)",
    "2022年\n(10-K)",
    "2023年\n(10-K)",
    "2024年\n(10-K)",
    "2025年\n(10-K)",
    "2026 Q3\n(最新单季)",
]

# Left Panel (Single unified USD/lb axis): Unit Net Cash Cost C1 & Unit C1 Cash Margin (Realized/LME Price - Net C1)
FCX_C1 = [1.34, 1.50, 1.61, 1.56, 1.65, 2.07]
SCCO_C1 = [0.67, 0.78, 1.03, 0.89, 0.58, 0.09]

FCX_SPREAD = [2.99, 2.40, 2.24, 2.65, 3.10, 4.47]
SCCO_SPREAD = [3.56, 3.22, 2.82, 3.26, 3.93, 6.32]

# Right Panel: CapEx / CFO (%) bars & NCI Profit Leakage (NCI / Consolidated Net Income %) lines
FCX_CAPEX_CFO = [27.4, 67.5, 91.4, 67.2, 80.1, 58.5]
SCCO_CAPEX_CFO = [20.8, 33.8, 28.2, 23.2, 27.9, 23.2]

FCX_NCI_PCT = [19.7, 22.6, 50.7, 57.1, 46.9, 30.5]
SCCO_NCI_PCT = [0.4, 0.4, 0.4, 0.4, 0.3, 0.3]

PILL_BBOX = dict(boxstyle="round,pad=0.18", facecolor="#0b0f19", edgecolor="none", alpha=0.88)


def main():
    out_path = Path(__file__).resolve().parent.parent / "assets" / "fcx_vs_scco_metrics_trend.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20.5, 9.5), dpi=300)
    fig.patch.set_facecolor(BG_FIG)

    x = np.arange(len(PERIODS))
    bw = 0.34

    # ------------------------------------------------------------------
    # Left Panel: Unit Net Cash Cost C1 vs Unit C1 Cash Margin (USD/lb)
    # ------------------------------------------------------------------
    ax1.set_facecolor(BG_AX)

    b_fcx_c1 = ax1.bar(
        x - bw / 2,
        FCX_C1,
        width=bw,
        color=FCX_BAR,
        alpha=0.86,
        label="FCX 单位净现金成本 C1 ($/磅)",
        zorder=2,
    )
    b_scco_c1 = ax1.bar(
        x + bw / 2,
        SCCO_C1,
        width=bw,
        color=SCCO_BAR,
        alpha=0.86,
        label="SCCO 单位净现金成本 C1 ($/磅)",
        zorder=2,
    )

    ax1.set_ylim(0, 7.9)

    ax1.axhline(
        1.50,
        color=THRESH_COLOR,
        linestyle=":",
        linewidth=1.6,
        alpha=0.88,
        label="1.50 美元/磅 全球低成本铜矿分水岭",
        zorder=2,
    )

    ax1.plot(
        x,
        FCX_SPREAD,
        color=FCX_LINE,
        marker="o",
        markersize=7,
        linewidth=2.6,
        label="FCX 单位 C1 现金毛利 = 均价 − C1 ($/磅)",
        zorder=5,
    )
    ax1.plot(
        x,
        SCCO_SPREAD,
        color=SCCO_LINE,
        marker="s",
        markersize=7,
        linewidth=2.6,
        linestyle="--",
        label="SCCO 单位 C1 现金毛利 = LME均价 − C1 ($/磅)",
        zorder=5,
    )

    for rect in b_fcx_c1:
        h = rect.get_height()
        ax1.text(
            rect.get_x() + rect.get_width() / 2,
            h + 0.08,
            f"${h:.2f}",
            ha="center",
            va="bottom",
            fontsize=8.2,
            color="#bfdbfe",
            fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.12", facecolor=BG_AX, edgecolor="none", alpha=0.88),
            zorder=4,
        )
    for rect in b_scco_c1:
        h = rect.get_height()
        ax1.text(
            rect.get_x() + rect.get_width() / 2,
            h + 0.08,
            f"${h:.2f}",
            ha="center",
            va="bottom",
            fontsize=8.2,
            color="#fde68a",
            fontweight="bold",
        )

    for idx, (f_s, s_s) in enumerate(zip(FCX_SPREAD, SCCO_SPREAD)):
        ax1.annotate(
            f"${f_s:.2f}",
            xy=(x[idx], f_s),
            xytext=(0, -15),
            textcoords="offset points",
            ha="center",
            va="top",
            fontsize=8.8,
            color=FCX_LINE,
            fontweight="bold",
            bbox=PILL_BBOX,
            zorder=6,
        )
        ax1.annotate(
            f"${s_s:.2f}",
            xy=(x[idx], s_s),
            xytext=(0, 9),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8.8,
            color=SCCO_LINE,
            fontweight="bold",
            bbox=PILL_BBOX,
            zorder=6,
        )

    ax1.set_title(
        "单位净现金成本 C1 与铜价−C1 现金毛利剪刀差 (美元/磅)",
        fontsize=13.2,
        fontweight="bold",
        color=TEXT_MAIN,
        pad=14,
    )
    ax1.set_xticks(x)
    ax1.set_xticklabels(PERIODS, fontsize=9.6, color=TEXT_MAIN)
    ax1.set_ylabel("美元 / 磅 (USD/lb)", fontsize=10.4, color=TEXT_MUTED)
    ax1.yaxis.set_major_formatter(mticker.FormatStrFormatter("$%.1f"))
    ax1.set_yticks([0, 1.5, 3.0, 4.5, 6.0, 7.5])
    ax1.tick_params(axis="y", colors=TEXT_MUTED)
    ax1.grid(axis="y", color=GRID_COLOR, linestyle="--", linewidth=0.7, zorder=0)

    ax1.spines["top"].set_visible(False)
    for spine in ["bottom", "left", "right"]:
        ax1.spines[spine].set_color(BORDER_COLOR)

    ax1.legend(
        loc="upper left",
        ncol=1,
        frameon=True,
        facecolor="#0f172a",
        edgecolor=BORDER_COLOR,
        fontsize=8.3,
        labelcolor=TEXT_MAIN,
    )

    # ------------------------------------------------------------------
    # Right Panel: CapEx / CFO (%) + NCI Profit Leakage (%)
    # ------------------------------------------------------------------
    ax2.set_facecolor(BG_AX)
    ax2_r = ax2.twinx()

    b2_fcx = ax2.bar(
        x - bw / 2,
        FCX_CAPEX_CFO,
        width=bw,
        color=FCX_BAR,
        alpha=0.86,
        label="FCX 资本开支占 CFO 比 (%)",
        zorder=2,
    )
    b2_scco = ax2.bar(
        x + bw / 2,
        SCCO_CAPEX_CFO,
        width=bw,
        color=SCCO_BAR,
        alpha=0.86,
        label="SCCO 资本开支占 CFO 比 (%)",
        zorder=2,
    )

    # Strict vertical zoning: bars in 0%..38% height, NCI lines in 45%..82% height (clear gap below legend)
    ax2.set_ylim(0, 240.0)
    ax2_r.set_ylim(-68.0, 82.0)

    ax2_r.axhline(
        30.0,
        color=THRESH_COLOR,
        linestyle=":",
        linewidth=1.6,
        alpha=0.88,
        label="30% 少数股东利润截留警戒线",
        zorder=2,
    )

    ax2_r.plot(
        x,
        FCX_NCI_PCT,
        color=FCX_LINE,
        marker="o",
        markersize=7,
        linewidth=2.6,
        label="FCX 少数股东净利截留占比 (%)",
        zorder=5,
    )
    ax2_r.plot(
        x,
        SCCO_NCI_PCT,
        color=SCCO_LINE,
        marker="s",
        markersize=7,
        linewidth=2.6,
        linestyle="--",
        label="SCCO 少数股东净利截留占比 (%)",
        zorder=5,
    )

    for rect in b2_fcx:
        h = rect.get_height()
        ax2.text(
            rect.get_x() + rect.get_width() / 2,
            h + 3.0,
            f"{h:.1f}%",
            ha="center",
            va="bottom",
            fontsize=8.2,
            color="#bfdbfe",
            fontweight="bold",
        )
    for rect in b2_scco:
        h = rect.get_height()
        ax2.text(
            rect.get_x() + rect.get_width() / 2,
            h + 3.0,
            f"{h:.1f}%",
            ha="center",
            va="bottom",
            fontsize=8.2,
            color="#fde68a",
            fontweight="bold",
        )

    for idx, (f_n, s_n) in enumerate(zip(FCX_NCI_PCT, SCCO_NCI_PCT)):
        ax2_r.annotate(
            f"{f_n:.1f}%",
            xy=(x[idx], f_n),
            xytext=(0, 9 if idx != 5 else 10),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8.8,
            color=FCX_LINE,
            fontweight="bold",
            bbox=PILL_BBOX,
            zorder=6,
        )
        ax2_r.annotate(
            f"{s_n:.1f}%",
            xy=(x[idx], s_n),
            xytext=(0, 9),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8.8,
            color=SCCO_LINE,
            fontweight="bold",
            bbox=PILL_BBOX,
            zorder=6,
        )

    ax2.set_title(
        "资本开支周期强度 (CapEx/CFO %) 与少数股东利润截留 (%)",
        fontsize=13.2,
        fontweight="bold",
        color=TEXT_MAIN,
        pad=14,
    )
    ax2.set_xticks(x)
    ax2.set_xticklabels(PERIODS, fontsize=9.6, color=TEXT_MAIN)
    ax2.set_ylabel("资本开支占经营现金流比 (%)", fontsize=10.4, color=TEXT_MUTED)
    ax2_r.set_ylabel("少数股东损益 ÷ 合并净利润 (%)", fontsize=10.4, color=TEXT_MUTED)
    ax2.set_yticks([0, 30, 60, 90])
    ax2_r.set_yticks([0, 20, 40, 60])
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
        loc="upper right",
        ncol=2,
        frameon=True,
        facecolor="#0f172a",
        edgecolor=BORDER_COLOR,
        fontsize=8.3,
        labelcolor=TEXT_MAIN,
    )

    fig.suptitle(
        "上游金属矿业与资源周期双标本跨周期对决：自由港迈克墨伦 FCX vs 南方铜业 SCCO（2021–2026 Q3 SEC 官方对账）",
        fontsize=15.4,
        fontweight="bold",
        color=TEXT_MAIN,
        y=0.97,
    )

    fig.text(
        0.5,
        0.015,
        "数据来源：自由港迈克墨伦 (FCX) 与南方铜业 (SCCO) 2021–2025 SEC Form 10-K 及 2026 Q3 Form 10-Q（截至 2026 年 9 月 30 日）。",
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
