#!/usr/bin/env python3
"""
Generate dual-panel comparison chart for Episode 16:
NextEra Energy (NEE, FY21-26Q3) vs Vistra Corp. (VST, FY21-26Q3).
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

NEE_BAR = "#2563eb"
NEE_LINE = "#60a5fa"
VST_BAR = "#d97706"
VST_LINE = "#fbbf24"
THRESH_COLOR = "#10b981"

PERIODS = [
    "2021年\n(10-K)",
    "2022年\n(10-K)",
    "2023年\n(10-K)",
    "2024年\n(10-K)",
    "2025年\n(10-K)",
    "2026 Q3\n(最新单季)",
]

# Left Panel: Operating Revenues ($B) & Fuel / Purchased Power % of Revenue
NEE_REV = [170.7, 209.6, 281.1, 247.5, 274.1, 80.9]
VST_REV = [120.8, 137.3, 147.8, 172.2, 177.4, 63.5]

NEE_FUEL_PCT = [26.5, 30.5, 19.4, 20.3, 18.0, 21.0]
VST_FUEL_PCT = [75.9, 75.8, 51.1, 42.3, 51.3, 39.9]

# Right Panel: Free Cash Flow = CFO - Total CapEx ($B) & CFO / Total Debt (%)
# Note: 2026 Q3 CFO/Total Debt uses annualized 9M 2026 CFO (NEE 123.2*4/3 / 1139.3 = 14.4%; VST 43.3*4/3 / 211.5 = 27.3%)
NEE_FCF = [-85.2, -110.2, -138.1, -114.7, -121.2, -31.2]
VST_FCF = [-12.4, -8.2, 37.8, 24.9, 13.2, 13.6]

NEE_CFO_DEBT = [13.8, 12.7, 15.4, 16.1, 13.1, 14.4]
VST_CFO_DEBT = [-1.9, 3.7, 37.9, 26.8, 20.3, 27.3]

PILL_BBOX = dict(boxstyle="round,pad=0.18", facecolor="#0b0f19", edgecolor="none", alpha=0.88)


def main():
    out_path = Path(__file__).resolve().parent.parent / "assets" / "nee_vs_vst_metrics_trend.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20.5, 9.5), dpi=300)
    fig.patch.set_facecolor(BG_FIG)

    x = np.arange(len(PERIODS))
    bw = 0.34

    # ------------------------------------------------------------------
    # Left Panel: Operating Revenue ($B) + Fuel & Purchased Power Ratio (%)
    # ------------------------------------------------------------------
    ax1.set_facecolor(BG_AX)
    ax1_r = ax1.twinx()

    b_nee_r = ax1.bar(
        x - bw / 2,
        NEE_REV,
        width=bw,
        color=NEE_BAR,
        alpha=0.86,
        label="NEE 营业收入 (亿美元)",
        zorder=2,
    )
    b_vst_r = ax1.bar(
        x + bw / 2,
        VST_REV,
        width=bw,
        color=VST_BAR,
        alpha=0.86,
        label="VST 营业收入 (亿美元)",
        zorder=2,
    )

    # Strict vertical zoning: bars in 0..34% height, Fuel% lines in 43%..86% height
    ax1.set_ylim(0, 820.0)
    ax1_r.set_ylim(-40.0, 96.0)

    ax1_r.axhline(
        30.0,
        color=THRESH_COLOR,
        linestyle=":",
        linewidth=1.6,
        alpha=0.88,
        label="30% 清洁能源/受管制燃料成本分水岭",
        zorder=3,
    )

    ax1_r.plot(
        x,
        NEE_FUEL_PCT,
        color=NEE_LINE,
        marker="o",
        markersize=7,
        linewidth=2.6,
        label="NEE 燃料与购电成本占比 (%)",
        zorder=5,
    )
    ax1_r.plot(
        x,
        VST_FUEL_PCT,
        color=VST_LINE,
        marker="s",
        markersize=7,
        linewidth=2.6,
        linestyle="--",
        label="VST 燃料与购电成本占比 (%)",
        zorder=5,
    )

    for rect in b_nee_r:
        h = rect.get_height()
        ax1.text(
            rect.get_x() + rect.get_width() / 2,
            h + 8.0,
            f"{h:.1f}",
            ha="center",
            va="bottom",
            fontsize=8.2,
            color="#bfdbfe",
            fontweight="bold",
        )
    for rect in b_vst_r:
        h = rect.get_height()
        ax1.text(
            rect.get_x() + rect.get_width() / 2,
            h + 8.0,
            f"{h:.1f}",
            ha="center",
            va="bottom",
            fontsize=8.2,
            color="#fde68a",
            fontweight="bold",
        )

    for idx, (n_f, v_f) in enumerate(zip(NEE_FUEL_PCT, VST_FUEL_PCT)):
        if idx in (0, 2, 4):
            n_y, n_va = -14, "top"
        else:
            n_y, n_va = 10, "bottom"
        ax1_r.annotate(
            f"{n_f:.1f}%",
            xy=(x[idx], n_f),
            xytext=(0, n_y),
            textcoords="offset points",
            ha="center",
            va=n_va,
            fontsize=8.8,
            color=NEE_LINE,
            fontweight="bold",
            bbox=PILL_BBOX,
            zorder=6,
        )
        v_x = 10 if idx == 2 else 0
        v_y = 10 if idx in (2, 3) else 9
        ax1_r.annotate(
            f"{v_f:.1f}%",
            xy=(x[idx], v_f),
            xytext=(v_x, v_y),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8.8,
            color=VST_LINE,
            fontweight="bold",
            bbox=PILL_BBOX,
            zorder=6,
        )

    ax1.set_title(
        "营收规模 (亿美元) 与燃料及购电成本占营收比 (%)",
        fontsize=13.2,
        fontweight="bold",
        color=TEXT_MAIN,
        pad=14,
    )
    ax1.set_xticks(x)
    ax1.set_xticklabels(PERIODS, fontsize=9.6, color=TEXT_MAIN)
    ax1.set_ylabel("营业收入 (亿美元)", fontsize=10.4, color=TEXT_MUTED)
    ax1_r.set_ylabel("燃料、购电及输配成本占营收比 (%)", fontsize=10.4, color=TEXT_MUTED)
    ax1.yaxis.set_major_formatter(mticker.FormatStrFormatter("%d"))
    ax1_r.yaxis.set_major_formatter(mticker.FormatStrFormatter("%d%%"))
    ax1_r.set_yticks([0, 20, 40, 60, 80])
    ax1.set_yticks([0, 100, 200, 300])
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
        fontsize=8.4,
        labelcolor=TEXT_MAIN,
    )

    # ------------------------------------------------------------------
    # Right Panel: Free Cash Flow ($B) + CFO / Total Debt Credit Coverage (%)
    # ------------------------------------------------------------------
    ax2.set_facecolor(BG_AX)
    ax2_r = ax2.twinx()

    ax2.axhline(0.0, color="#475569", linestyle="-", linewidth=1.0, zorder=1)

    b2_nee = ax2.bar(
        x - bw / 2,
        NEE_FCF,
        width=bw,
        color=NEE_BAR,
        alpha=0.86,
        label="NEE 自由现金流 FCF (亿美元)",
        zorder=2,
    )
    b2_vst = ax2.bar(
        x + bw / 2,
        VST_FCF,
        width=bw,
        color=VST_BAR,
        alpha=0.86,
        label="VST 自由现金流 FCF (亿美元)",
        zorder=2,
    )

    # Strict vertical zoning: FCF bars in 10%..47% height, CFO/Debt lines in 50%..85% height
    ax2.set_ylim(-185.0, 290.0)
    ax2_r.set_ylim(-55.0, 58.0)

    ax2_r.axhline(
        15.0,
        color=THRESH_COLOR,
        linestyle=":",
        linewidth=1.6,
        alpha=0.88,
        label="15% 投资级公用事业 CFO/债务 信用底线",
        zorder=3,
    )

    ax2_r.plot(
        x,
        NEE_CFO_DEBT,
        color=NEE_LINE,
        marker="o",
        markersize=7,
        linewidth=2.6,
        label="NEE 经营现金流 ÷ 总有息债务 (%)",
        zorder=5,
    )
    ax2_r.plot(
        x,
        VST_CFO_DEBT,
        color=VST_LINE,
        marker="s",
        markersize=7,
        linewidth=2.6,
        linestyle="--",
        label="VST 经营现金流 ÷ 总有息债务 (%)",
        zorder=5,
    )

    for rect in b2_nee:
        h = rect.get_height()
        ax2.text(
            rect.get_x() + rect.get_width() / 2,
            h - 4.5,
            f"{h:.1f}",
            ha="center",
            va="top",
            fontsize=8.2,
            color="#bfdbfe",
            fontweight="bold",
        )
    for rect in b2_vst:
        h = rect.get_height()
        if h >= 0:
            ax2.text(
                rect.get_x() + rect.get_width() / 2,
                h + 4.5,
                f"+{h:.1f}",
                ha="center",
                va="bottom",
                fontsize=8.2,
                color="#fde68a",
                fontweight="bold",
            )
        else:
            ax2.text(
                rect.get_x() + rect.get_width() / 2,
                h - 4.5,
                f"{h:.1f}",
                ha="center",
                va="top",
                fontsize=8.2,
                color="#fde68a",
                fontweight="bold",
            )

    for idx, (n_c, v_c) in enumerate(zip(NEE_CFO_DEBT, VST_CFO_DEBT)):
        if idx == 0:
            n_x, n_y, n_va = 0, -15, "top"
        elif idx == 1:
            n_x, n_y, n_va = -12, 12, "bottom"
        else:
            n_x, n_y, n_va = 0, -15, "top"
        ax2_r.annotate(
            f"{n_c:.1f}%",
            xy=(x[idx], n_c),
            xytext=(n_x, n_y),
            textcoords="offset points",
            ha="center",
            va=n_va,
            fontsize=8.8,
            color=NEE_LINE,
            fontweight="bold",
            bbox=PILL_BBOX,
            zorder=6,
        )
        v_y = -14 if idx in (0, 1) else 9
        v_va = "top" if idx in (0, 1) else "bottom"
        ax2_r.annotate(
            f"{v_c:.1f}%",
            xy=(x[idx], v_c),
            xytext=(0, v_y),
            textcoords="offset points",
            ha="center",
            va=v_va,
            fontsize=8.8,
            color=VST_LINE,
            fontweight="bold",
            bbox=PILL_BBOX,
            zorder=6,
        )

    ax2.set_title(
        "重资产扩产自由现金流 FCF (亿美元) 与信用覆盖率 CFO/总债务 (%)",
        fontsize=13.2,
        fontweight="bold",
        color=TEXT_MAIN,
        pad=14,
    )
    ax2.set_xticks(x)
    ax2.set_xticklabels(PERIODS, fontsize=9.6, color=TEXT_MAIN)
    ax2.set_ylabel("自由现金流 FCF = CFO − 总资本开支 (亿美元)", fontsize=10.4, color=TEXT_MUTED)
    ax2_r.set_ylabel("经营现金流 ÷ 总有息债务 (%)", fontsize=10.4, color=TEXT_MUTED)
    ax2.set_yticks([-150, -100, -50, 0, 50])
    ax2_r.set_yticks([0, 15, 30, 45])
    ax2.yaxis.set_major_formatter(mticker.FormatStrFormatter("%d"))
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
        fontsize=8.4,
        labelcolor=TEXT_MAIN,
    )

    fig.suptitle(
        "电力与公用事业双标本跨周期对决：新纪元能源 NEE vs 维斯达能源 VST（2021–2026 Q3 SEC 官方对账）",
        fontsize=15.6,
        fontweight="bold",
        color=TEXT_MAIN,
        y=0.97,
    )

    fig.text(
        0.5,
        0.015,
        "数据来源：新纪元能源 (NEE) 与维斯达能源 (VST) 2021–2025 SEC Form 10-K 及 2026 Q3 Form 10-Q；2026 Q3 之 CFO/总债务按前九月年化口径折算。",
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
