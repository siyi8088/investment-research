#!/usr/bin/env python3
"""
Generate dual-panel comparison chart for Episode 11:
ASML Holding (ASML) vs KLA Corporation (KLAC)
All figures strictly sourced from audited SEC 20-F / 6-K / 10-K / 10-Q filings.
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

# Strictly one color family per company
ASML_BAR = "#2563eb"
ASML_LINE = "#60a5fa"
KLA_BAR = "#d97706"
KLA_LINE = "#fbbf24"

PERIODS = [
    "2021 / FY22",
    "2022 / FY23",
    "2023 / FY24",
    "2024 / FY25",
    "2025 / FY26",
    "26Q3 / Q1FY27\n(单季)",
]

# Panel 1: Revenue (USD $B) & GAAP Operating Margin (%)
# ASML EUR converted via ECB/Fed H.10 avg FX: 1.1827, 1.0530, 1.0813, 1.0824, 1.1300, 1.1568
ASML_REV_USD = [22.01, 22.30, 29.80, 30.59, 36.91, 13.49]
KLA_REV_USD = [9.21, 10.50, 9.81, 12.16, 13.58, 4.14]

ASML_OPM = [36.3, 30.7, 32.8, 31.9, 34.6, 44.4]
KLA_OPM = [39.7, 38.1, 34.1, 39.3, 41.7, 45.0]

# Panel 2: GAAP Gross Margin (%) & China Revenue Share (%)
ASML_GM = [52.7, 50.5, 51.3, 51.3, 52.8, 57.5]
KLA_GM = [61.0, 59.8, 60.0, 60.9, 61.3, 61.9]

# Note: ASML Q3'26 23.0% is Net System Sales geography disclosure from Q3'26 6-K presentation
ASML_CHINA = [14.7, 13.8, 26.3, 36.1, 29.1, 23.0]
KLA_CHINA = [28.9, 27.3, 42.8, 33.3, 29.8, 34.5]


def main():
    out_path = Path(__file__).resolve().parent.parent / "assets" / "asml_vs_kla_metrics_trend.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 9.2), dpi=300)
    fig.patch.set_facecolor(BG_FIG)

    x = np.arange(len(PERIODS))
    bar_w = 0.34

    # ------------------------------------------------------------------
    # Left Panel: Revenue Scale ($B) + GAAP Operating Margin (%)
    # ------------------------------------------------------------------
    ax1.set_facecolor(BG_AX)
    ax1_r = ax1.twinx()

    bars_a1 = ax1.bar(
        x - bar_w / 2,
        ASML_REV_USD,
        width=bar_w,
        color=ASML_BAR,
        alpha=0.88,
        label="ASML 总营收 ($B, 按年均汇率折算)",
        zorder=2,
    )
    bars_k1 = ax1.bar(
        x + bar_w / 2,
        KLA_REV_USD,
        width=bar_w,
        color=KLA_BAR,
        alpha=0.88,
        label="KLA 总营收 ($B)",
        zorder=2,
    )

    # Keep bars strictly in lower 52% of left axis so OPM lines never cross bars
    ax1.set_ylim(0, 74)
    ax1_r.set_ylim(0, 52)

    line_a1 = ax1_r.plot(
        x,
        ASML_OPM,
        color=ASML_LINE,
        marker="o",
        markersize=7,
        linewidth=2.6,
        label="ASML 营业利润率 (%)",
        zorder=4,
    )
    line_k1 = ax1_r.plot(
        x,
        KLA_OPM,
        color=KLA_LINE,
        marker="s",
        markersize=7,
        linewidth=2.6,
        linestyle="--",
        label="KLA 营业利润率 (%)",
        zorder=4,
    )

    # Direct bar value labels
    for rect in bars_a1:
        h = rect.get_height()
        ax1.text(
            rect.get_x() + rect.get_width() / 2,
            h + 0.9,
            f"${h:.1f}B",
            ha="center",
            va="bottom",
            fontsize=8.8,
            color="#bfdbfe",
            fontweight="bold",
        )
    for rect in bars_k1:
        h = rect.get_height()
        ax1.text(
            rect.get_x() + rect.get_width() / 2,
            h + 0.9,
            f"${h:.1f}B",
            ha="center",
            va="bottom",
            fontsize=8.8,
            color="#fde68a",
            fontweight="bold",
        )

    # OPM point labels with collision-safe offsets
    for idx, (a_val, k_val) in enumerate(zip(ASML_OPM, KLA_OPM)):
        # KLA is consistently above ASML except close in Q3'26/Q1'27 (45.0 vs 44.4)
        k_offset = 10 if idx != 5 else 11
        a_offset = -16 if idx != 5 else -16
        ax1_r.annotate(
            f"{k_val:.1f}%",
            xy=(x[idx], k_val),
            xytext=(0, k_offset),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9,
            color=KLA_LINE,
            fontweight="bold",
        )
        ax1_r.annotate(
            f"{a_val:.1f}%",
            xy=(x[idx], a_val),
            xytext=(0, a_offset),
            textcoords="offset points",
            ha="center",
            va="top",
            fontsize=9,
            color=ASML_LINE,
            fontweight="bold",
        )

    ax1.set_title(
        "营收体量 (USD $B) 与 GAAP 营业利润率 (%) 对比",
        fontsize=13.5,
        fontweight="bold",
        color=TEXT_MAIN,
        pad=14,
    )
    ax1.set_xticks(x)
    ax1.set_xticklabels(PERIODS, fontsize=9.8, color=TEXT_MAIN)
    ax1.set_ylabel("总营收 (十亿美元 $B)", fontsize=10.5, color=TEXT_MUTED)
    ax1_r.set_ylabel("GAAP 营业利润率 (%)", fontsize=10.5, color=TEXT_MUTED)
    ax1.yaxis.set_major_formatter(mticker.FormatStrFormatter("$%dB"))
    ax1_r.yaxis.set_major_formatter(mticker.FormatStrFormatter("%d%%"))
    ax1.tick_params(axis="y", colors=TEXT_MUTED)
    ax1_r.tick_params(axis="y", colors=TEXT_MUTED)
    ax1.grid(axis="y", color=GRID_COLOR, linestyle="--", linewidth=0.7, zorder=0)

    for spine in ["top"]:
        ax1.spines[spine].set_visible(False)
        ax1_r.spines[spine].set_visible(False)
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
    # Right Panel: GAAP Gross Margin (%) vs China Revenue Concentration (%)
    # ------------------------------------------------------------------
    ax2.set_facecolor(BG_AX)

    bars_a2 = ax2.bar(
        x - bar_w / 2,
        ASML_CHINA,
        width=bar_w,
        color=ASML_BAR,
        alpha=0.88,
        label="ASML 中国大陆营收占比 (%)",
        zorder=2,
    )
    bars_k2 = ax2.bar(
        x + bar_w / 2,
        KLA_CHINA,
        width=bar_w,
        color=KLA_BAR,
        alpha=0.88,
        label="KLA 中国大陆营收占比 (%)",
        zorder=2,
    )

    line_a2 = ax2.plot(
        x,
        ASML_GM,
        color=ASML_LINE,
        marker="o",
        markersize=7,
        linewidth=2.6,
        label="ASML GAAP 毛利率 (%)",
        zorder=4,
    )
    line_k2 = ax2.plot(
        x,
        KLA_GM,
        color=KLA_LINE,
        marker="s",
        markersize=7,
        linewidth=2.6,
        linestyle="--",
        label="KLA GAAP 毛利率 (%)",
        zorder=4,
    )

    ax2.set_ylim(0, 78)

    for idx, rect in enumerate(bars_a2):
        h = rect.get_height()
        lbl = f"{h:.1f}%*" if idx == 5 else f"{h:.1f}%"
        ax2.text(
            rect.get_x() + rect.get_width() / 2,
            h + 0.9,
            lbl,
            ha="center",
            va="bottom",
            fontsize=8.6,
            color="#bfdbfe",
            fontweight="bold",
        )
    for rect in bars_k2:
        h = rect.get_height()
        ax2.text(
            rect.get_x() + rect.get_width() / 2,
            h + 0.9,
            f"{h:.1f}%",
            ha="center",
            va="bottom",
            fontsize=8.6,
            color="#fde68a",
            fontweight="bold",
        )

    for idx, (a_gm, k_gm) in enumerate(zip(ASML_GM, KLA_GM)):
        ax2.annotate(
            f"{k_gm:.1f}%",
            xy=(x[idx], k_gm),
            xytext=(0, 9),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9,
            color=KLA_LINE,
            fontweight="bold",
        )
        ax2.annotate(
            f"{a_gm:.1f}%",
            xy=(x[idx], a_gm),
            xytext=(0, -14),
            textcoords="offset points",
            ha="center",
            va="top",
            fontsize=9,
            color=ASML_LINE,
            fontweight="bold",
        )

    ax2.set_title(
        "GAAP 毛利率护城河 (%) 与中国大陆营收集中度 (%) 对比",
        fontsize=13.5,
        fontweight="bold",
        color=TEXT_MAIN,
        pad=14,
    )
    ax2.set_xticks(x)
    ax2.set_xticklabels(PERIODS, fontsize=9.8, color=TEXT_MAIN)
    ax2.set_ylabel("占当期营收比例 (%)", fontsize=10.5, color=TEXT_MUTED)
    ax2.yaxis.set_major_formatter(mticker.FormatStrFormatter("%d%%"))
    ax2.tick_params(axis="y", colors=TEXT_MUTED)
    ax2.grid(axis="y", color=GRID_COLOR, linestyle="--", linewidth=0.7, zorder=0)

    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.spines["bottom"].set_color(BORDER_COLOR)
    ax2.spines["left"].set_color(BORDER_COLOR)

    ax2.legend(
        loc="upper left",
        ncol=2,
        frameon=True,
        facecolor="#0f172a",
        edgecolor=BORDER_COLOR,
        fontsize=8.8,
        labelcolor=TEXT_MAIN,
    )

    fig.suptitle(
        "前道核心设备双寡头全景：ASML (CY21–26Q3) vs KLA (FY22–Q1 FY27)",
        fontsize=16.5,
        fontweight="bold",
        color=TEXT_MAIN,
        y=0.97,
    )

    fig.text(
        0.5,
        0.015,
        "数据来源：ASML SEC 20-F/6-K (CY21–Q3'26，EUR按ECB/Fed H.10年均汇率折算USD) & KLA SEC 10-K/10-Q (FY22–Q1 FY27，6月30日财年)。*注：ASML 26Q3 23.0% 为净系统销售地理占比。",
        ha="center",
        va="bottom",
        fontsize=9,
        color=TEXT_MUTED,
    )

    plt.tight_layout(rect=[0.01, 0.045, 0.99, 0.93], w_pad=3.2)
    fig.savefig(out_path, dpi=300, facecolor=BG_FIG)
    plt.close(fig)
    print(f"Saved chart to {out_path}")


if __name__ == "__main__":
    main()
