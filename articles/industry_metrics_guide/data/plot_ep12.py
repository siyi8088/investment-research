#!/usr/bin/env python3
"""
Generate dual-panel comparison chart for Episode 12:
TSMC (TSM) vs SMIC (00981.HK / 688981.SH)
All figures strictly sourced from audited SEC 20-F / 6-K and HKEX / SSE filings (2021 - 2026 Q3).
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
TSMC_BAR = "#2563eb"
TSMC_LINE = "#60a5fa"
SMIC_BAR = "#d97706"
SMIC_LINE = "#fbbf24"

PERIODS = [
    "2021 年",
    "2022 年",
    "2023 年",
    "2024 年",
    "2025 年",
    "2026 Q3\n(单季)",
]

# Panel 1: Revenue (USD $B) & Gross Margin (%)
TSMC_REV_USD = [56.82, 75.88, 69.30, 90.08, 122.42, 46.72]
SMIC_REV_USD = [5.44, 7.27, 6.32, 8.03, 9.33, 3.19]

TSMC_GM = [51.6, 59.6, 54.4, 56.1, 59.9, 66.4]
SMIC_GM = [30.8, 38.0, 19.3, 18.0, 21.0, 29.9]

# Panel 2: CapEx Intensity (CapEx / Revenue %) & D&A Burden (Total D&A / Revenue %)
TSMC_CAPEX_PCT = [52.9, 47.8, 43.9, 33.0, 33.4, 29.7]
SMIC_CAPEX_PCT = [82.9, 87.3, 118.2, 91.2, 86.8, 34.3]

TSMC_DA_PCT = [26.6, 19.3, 24.6, 22.9, 18.1, 14.7]
SMIC_DA_PCT = [34.4, 31.2, 42.2, 40.1, 40.8, 35.7]

PILL_BBOX = dict(boxstyle="round,pad=0.18", facecolor="#0b0f19", edgecolor="none", alpha=0.82)


def main():
    out_path = Path(__file__).resolve().parent.parent / "assets" / "tsmc_vs_smic_metrics_trend.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 9.2), dpi=300)
    fig.patch.set_facecolor(BG_FIG)

    x = np.arange(len(PERIODS))
    bar_w = 0.34

    # ------------------------------------------------------------------
    # Left Panel: Revenue Scale ($B) + Gross Margin (%)
    # ------------------------------------------------------------------
    ax1.set_facecolor(BG_AX)
    ax1_r = ax1.twinx()

    bars_t1 = ax1.bar(
        x - bar_w / 2,
        TSMC_REV_USD,
        width=bar_w,
        color=TSMC_BAR,
        alpha=0.88,
        label="台积电 TSMC 总营收 ($B)",
        zorder=2,
    )
    bars_s1 = ax1.bar(
        x + bar_w / 2,
        SMIC_REV_USD,
        width=bar_w,
        color=SMIC_BAR,
        alpha=0.88,
        label="中芯国际 SMIC 总营收 ($B)",
        zorder=2,
    )

    ax1.set_ylim(0, 225)
    ax1_r.set_ylim(0, 82)

    ax1_r.plot(
        x,
        TSMC_GM,
        color=TSMC_LINE,
        marker="o",
        markersize=7,
        linewidth=2.6,
        label="台积电 TSMC 毛利率 (%)",
        zorder=4,
    )
    ax1_r.plot(
        x,
        SMIC_GM,
        color=SMIC_LINE,
        marker="s",
        markersize=7,
        linewidth=2.6,
        linestyle="--",
        label="中芯国际 SMIC 毛利率 (%)",
        zorder=4,
    )

    # Direct bar value labels
    for rect in bars_t1:
        h = rect.get_height()
        ax1.text(
            rect.get_x() + rect.get_width() / 2,
            h + 2.2,
            f"${h:.1f}B",
            ha="center",
            va="bottom",
            fontsize=8.6,
            color="#bfdbfe",
            fontweight="bold",
        )
    for rect in bars_s1:
        h = rect.get_height()
        ax1.text(
            rect.get_x() + rect.get_width() / 2,
            h + 2.2,
            f"${h:.2f}B",
            ha="center",
            va="bottom",
            fontsize=8.4,
            color="#fde68a",
            fontweight="bold",
        )

    # Gross Margin point labels with collision-free offsets & pill background
    for idx, (t_gm, s_gm) in enumerate(zip(TSMC_GM, SMIC_GM)):
        ax1_r.annotate(
            f"{t_gm:.1f}%",
            xy=(x[idx], t_gm),
            xytext=(0, 10),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9.2,
            color=TSMC_LINE,
            fontweight="bold",
        )
        # Offset SMIC GM slightly right in 2023-2025 so it sits over the dark gap between bars
        s_xytext = (16, 7) if idx in (2, 3, 4) else (0, 9)
        ax1_r.annotate(
            f"{s_gm:.1f}%",
            xy=(x[idx], s_gm),
            xytext=s_xytext,
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9.0,
            color=SMIC_LINE,
            fontweight="bold",
            bbox=PILL_BBOX if idx in (2, 3, 4) else None,
            zorder=5,
        )

    ax1.set_title(
        "营收体量 (USD $B) 与综合毛利率 (%) 跨周期对比",
        fontsize=13.5,
        fontweight="bold",
        color=TEXT_MAIN,
        pad=14,
    )
    ax1.set_xticks(x)
    ax1.set_xticklabels(PERIODS, fontsize=9.8, color=TEXT_MAIN)
    ax1.set_ylabel("总营收 (十亿美元 $B)", fontsize=10.5, color=TEXT_MUTED)
    ax1_r.set_ylabel("综合毛利率 (%)", fontsize=10.5, color=TEXT_MUTED)
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
    # Right Panel: CapEx Intensity (%) vs Total D&A Burden (% of Revenue)
    # ------------------------------------------------------------------
    ax2.set_facecolor(BG_AX)

    bars_t2 = ax2.bar(
        x - bar_w / 2,
        TSMC_CAPEX_PCT,
        width=bar_w,
        color=TSMC_BAR,
        alpha=0.82,
        label="台积电 CapEx 占营收比 (%)",
        zorder=2,
    )
    bars_s2 = ax2.bar(
        x + bar_w / 2,
        SMIC_CAPEX_PCT,
        width=bar_w,
        color=SMIC_BAR,
        alpha=0.82,
        label="中芯国际 CapEx 占营收比 (%)",
        zorder=2,
    )

    ax2.plot(
        x,
        TSMC_DA_PCT,
        color=TSMC_LINE,
        marker="o",
        markersize=7,
        linewidth=2.6,
        label="台积电 折旧摊销占营收比 (%)",
        zorder=4,
    )
    ax2.plot(
        x,
        SMIC_DA_PCT,
        color=SMIC_LINE,
        marker="s",
        markersize=7,
        linewidth=2.6,
        linestyle="--",
        label="中芯国际 折旧摊销占营收比 (%)",
        zorder=4,
    )

    ax2.set_ylim(0, 142)

    for idx, rect in enumerate(bars_t2):
        h = rect.get_height()
        ax2.text(
            rect.get_x() + rect.get_width() / 2 - (0.03 if idx == 2 else 0),
            h + 1.5,
            f"{h:.1f}%",
            ha="center",
            va="bottom",
            fontsize=8.6,
            color="#bfdbfe",
            fontweight="bold",
        )
    for idx, rect in enumerate(bars_s2):
        h = rect.get_height()
        # In 2026 Q3 (idx 5), SMIC CapEx bar is 34.3% at x+0.17; shift label slightly right
        x_pos = rect.get_x() + rect.get_width() / 2 + (0.08 if idx == 5 else 0)
        y_pos = h + 1.5
        ax2.text(
            x_pos,
            y_pos,
            f"{h:.1f}%",
            ha="center",
            va="bottom",
            fontsize=8.6,
            color="#fde68a",
            fontweight="bold",
        )

    for idx, (t_da, s_da) in enumerate(zip(TSMC_DA_PCT, SMIC_DA_PCT)):
        ax2.annotate(
            f"{t_da:.1f}%",
            xy=(x[idx], t_da),
            xytext=(0, -14),
            textcoords="offset points",
            ha="center",
            va="top",
            fontsize=8.8,
            color=TSMC_LINE,
            fontweight="bold",
            bbox=PILL_BBOX,
            zorder=5,
        )
        # Collision-free placement for SMIC D&A% line labels
        if idx == 2:
            # 2023: TSMC CapEx bar is 43.9% at left, SMIC D&A is 42.2% at center -> place below-right on orange bar
            s_xytext = (16, -13)
            s_va = "top"
        elif idx == 5:
            # 2026 Q3: SMIC D&A is 35.7% at center -> place cleanly above-left of marker
            s_xytext = (-10, 11)
            s_va = "bottom"
        else:
            s_xytext = (10 if idx in (3, 4) else 0, 9)
            s_va = "bottom"
        ax2.annotate(
            f"{s_da:.1f}%",
            xy=(x[idx], s_da),
            xytext=s_xytext,
            textcoords="offset points",
            ha="center",
            va=s_va,
            fontsize=8.8,
            color=SMIC_LINE,
            fontweight="bold",
            bbox=PILL_BBOX,
            zorder=5,
        )

    ax2.set_title(
        "资本开支强度 (CapEx/Rev %) 与折旧摊销负担 (D&A/Rev %) 对比",
        fontsize=13.5,
        fontweight="bold",
        color=TEXT_MAIN,
        pad=14,
    )
    ax2.set_xticks(x)
    ax2.set_xticklabels(PERIODS, fontsize=9.8, color=TEXT_MAIN)
    ax2.set_ylabel("占当期总营收比例 (%)", fontsize=10.5, color=TEXT_MUTED)
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
        "晶圆代工双标本跨周期对决：台积电 TSMC vs 中芯国际 SMIC (2021–2026 Q3)",
        fontsize=16.5,
        fontweight="bold",
        color=TEXT_MAIN,
        y=0.97,
    )

    fig.text(
        0.5,
        0.015,
        "数据来源：台积电 (TSM) SEC Form 20-F / 2026 Q3 Form 6-K 财报，中芯国际 (00981.HK / 688981.SH) 2021–2025 年报及 2026 Q3 季报 (IFRS 美元口径)。",
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
