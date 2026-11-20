#!/usr/bin/env python3
"""
Generate dual-panel comparison chart for Episode 13:
NVIDIA (NVDA, FY22-FY26 & FY27 Q3) vs AMD (FY21-FY25 & 2026 Q3).
All figures strictly sourced from audited SEC Form 10-K / 10-Q / 8-K filings.
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

# Distinct accessible color families: Emerald/Mint (NVDA) vs Crimson/Coral (AMD)
NVDA_BAR = "#059669"
NVDA_LINE = "#34d399"
AMD_BAR = "#dc2626"
AMD_LINE = "#f87171"
THRESH_COLOR = "#38bdf8"

PERIODS = [
    "2021周期\n(NV22/AMD21)",
    "2022周期\n(NV23/AMD22)",
    "2023周期\n(NV24/AMD23)",
    "2024周期\n(NV25/AMD24)",
    "2025周期\n(NV26/AMD25)",
    "2026 Q3\n(FY27Q3/26Q3)",
]

# Left Panel: Data Center Revenue Mix (%) & GAAP Gross Margin (%)
NVDA_DC_PCT = [39.4, 55.6, 78.0, 88.3, 89.7, 92.9]
AMD_DC_PCT = [24.0, 25.6, 28.6, 46.0, 52.5, 63.9]

NVDA_GM = [64.9, 56.9, 72.7, 75.0, 71.1, 74.8]
AMD_GM = [48.2, 44.9, 46.1, 49.4, 49.5, 53.9]

# Right Panel: Manufacturing/Supply Purchase Obligations ($B = 亿美元 / 100M -> 亿美元) & DIO (Days)
NVDA_OBL = [103.0, 80.6, 207.1, 450.8, 952.0, 3900.0]
AMD_OBL = [90.7, 86.1, 45.9, 49.7, 121.7, 488.0]

NVDA_DIO = [86, 122, 115, 86, 92, 112]
AMD_DIO = [72, 80, 121, 141, 142, 147]

PILL_BBOX = dict(boxstyle="round,pad=0.18", facecolor="#0b0f19", edgecolor="none", alpha=0.88)


def main():
    out_path = Path(__file__).resolve().parent.parent / "assets" / "nvda_vs_amd_metrics_trend.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20.5, 9.4), dpi=300)
    fig.patch.set_facecolor(BG_FIG)

    x = np.arange(len(PERIODS))
    bw = 0.34

    # ------------------------------------------------------------------
    # Left Panel: Data Center Revenue Mix (%) + GAAP Gross Margin (%)
    # ------------------------------------------------------------------
    ax1.set_facecolor(BG_AX)
    ax1_r = ax1.twinx()

    b1_nvda = ax1.bar(
        x - bw / 2,
        NVDA_DC_PCT,
        width=bw,
        color=NVDA_BAR,
        alpha=0.84,
        label="NVDA 数据中心营收占比 (%)",
        zorder=2,
    )
    b1_amd = ax1.bar(
        x + bw / 2,
        AMD_DC_PCT,
        width=bw,
        color=AMD_BAR,
        alpha=0.84,
        label="AMD 数据中心营收占比 (%)",
        zorder=2,
    )

    # Keep DC bars cleanly up to 72% height and GM lines separated from DC bar labels
    ax1.set_ylim(0, 130)
    ax1_r.set_ylim(20, 118)

    ax1_r.plot(
        x,
        NVDA_GM,
        color=NVDA_LINE,
        marker="s",
        markersize=7,
        linewidth=2.7,
        label="NVDA GAAP 毛利率 (%)",
        zorder=5,
    )
    ax1_r.plot(
        x,
        AMD_GM,
        color=AMD_LINE,
        marker="^",
        markersize=7.5,
        linewidth=2.7,
        linestyle="--",
        label="AMD GAAP 毛利率 (%)",
        zorder=5,
    )

    for rect in b1_nvda:
        h = rect.get_height()
        ax1.text(
            rect.get_x() + rect.get_width() / 2,
            h + 1.5,
            f"{h:.1f}%",
            ha="center",
            va="bottom",
            fontsize=8.6,
            color="#a7f3d0",
            fontweight="bold",
        )
    for rect in b1_amd:
        h = rect.get_height()
        # Keep AMD bar labels inside bars for 2021-2023 when AMD GM line passes just above; outside when clear
        if h < 35:
            ax1.text(
                rect.get_x() + rect.get_width() / 2,
                h * 0.50,
                f"{h:.1f}%",
                ha="center",
                va="center",
                fontsize=8.3,
                color="#fee2e2",
                fontweight="bold",
                zorder=4,
            )
        else:
            ax1.text(
                rect.get_x() + rect.get_width() / 2,
                h + 1.5,
                f"{h:.1f}%",
                ha="center",
                va="bottom",
                fontsize=8.6,
                color="#fecaca",
                fontweight="bold",
            )

    for idx, (n_gm, a_gm) in enumerate(zip(NVDA_GM, AMD_GM)):
        # NVDA GM: above line for 2021-2022 and 2026Q3 (clears 63.9% AMD bar), below line for 2023-2025
        if idx in (0, 1, 5):
            n_off, n_va = 9, "bottom"
        else:
            n_off, n_va = -13, "top"
        ax1_r.annotate(
            f"{n_gm:.1f}%",
            xy=(x[idx], n_gm),
            xytext=(0, n_off),
            textcoords="offset points",
            ha="center",
            va=n_va,
            fontsize=8.8,
            color=NVDA_LINE,
            fontweight="bold",
            bbox=PILL_BBOX,
            zorder=6,
        )

        # AMD GM: cleanly shift right above AMD bar for 2021 (clears 39.4% NVDA bar), below line for 2023-2026Q3
        if idx == 0:
            a_xoff, a_off, a_va = 18, 8, "bottom"
        elif idx == 1:
            a_xoff, a_off, a_va = 0, 8, "bottom"
        else:
            a_xoff, a_off, a_va = 14 if idx >= 3 else 0, -13, "top"
        ax1_r.annotate(
            f"{a_gm:.1f}%",
            xy=(x[idx], a_gm),
            xytext=(a_xoff, a_off),
            textcoords="offset points",
            ha="center",
            va=a_va,
            fontsize=8.8,
            color=AMD_LINE,
            fontweight="bold",
            bbox=PILL_BBOX,
            zorder=6,
        )

    ax1.set_title(
        "算力结构跃迁与毛利率溢价：数据中心占比 (%) vs GAAP 综合毛利率 (%)",
        fontsize=13.2,
        fontweight="bold",
        color=TEXT_MAIN,
        pad=14,
    )
    ax1.set_xticks(x)
    ax1.set_xticklabels(PERIODS, fontsize=9.4, color=TEXT_MAIN)
    ax1.set_ylabel("数据中心营收占总营收比重 (%)", fontsize=10.5, color=TEXT_MUTED)
    ax1_r.set_ylabel("GAAP 综合毛利率 (%)", fontsize=10.5, color=TEXT_MUTED)
    ax1.yaxis.set_major_formatter(mticker.FormatStrFormatter("%d%%"))
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
    # Right Panel: Off-Balance-Sheet Supply Commitments ($100M / 亿美元) + DIO (Days)
    # ------------------------------------------------------------------
    ax2.set_facecolor(BG_AX)
    ax2_r = ax2.twinx()

    b2_nvda = ax2.bar(
        x - bw / 2,
        NVDA_OBL,
        width=bw,
        color=NVDA_BAR,
        alpha=0.84,
        label="NVDA 制造与供应保供承诺 (亿美元)",
        zorder=2,
    )
    b2_amd = ax2.bar(
        x + bw / 2,
        AMD_OBL,
        width=bw,
        color=AMD_BAR,
        alpha=0.84,
        label="AMD 运营无条件采购承诺 (亿美元)",
        zorder=2,
    )

    ax2.set_ylim(0, 4950)
    ax2_r.set_ylim(5, 195)

    ax2_r.axhline(
        90.0,
        color=THRESH_COLOR,
        linestyle=":",
        linewidth=1.5,
        alpha=0.85,
        label="90 天 Fabless 常态存货中枢参考线",
        zorder=3,
    )

    ax2_r.plot(
        x,
        NVDA_DIO,
        color=NVDA_LINE,
        marker="o",
        markersize=7,
        linewidth=2.7,
        label="NVDA 存货周转天数 DIO (天)",
        zorder=5,
    )
    ax2_r.plot(
        x,
        AMD_DIO,
        color=AMD_LINE,
        marker="D",
        markersize=6.5,
        linewidth=2.7,
        linestyle="--",
        label="AMD 存货周转天数 DIO (天)",
        zorder=5,
    )

    for idx, rect in enumerate(b2_nvda):
        h = rect.get_height()
        lbl = f"${h:,.0f}亿"
        ax2.text(
            rect.get_x() + rect.get_width() / 2,
            h + 55,
            lbl,
            ha="center",
            va="bottom",
            fontsize=8.5,
            color="#a7f3d0",
            fontweight="bold",
        )
    for idx, rect in enumerate(b2_amd):
        h = rect.get_height()
        lbl = f"${h:,.0f}亿"
        # Offset 2021-2022 slightly right/up cleanly since bars are side-by-side at ~100亿
        ax2.text(
            rect.get_x() + rect.get_width() / 2 + (0.04 if idx <= 1 else 0.0),
            h + 55,
            lbl,
            ha="center",
            va="bottom",
            fontsize=8.3,
            color="#fecaca",
            fontweight="bold",
        )

    for idx, (n_dio, a_dio) in enumerate(zip(NVDA_DIO, AMD_DIO)):
        if n_dio >= a_dio:
            n_off, n_va = 9, "bottom"
            a_off, a_va = -13, "top"
        else:
            a_off, a_va = 9, "bottom"
            n_off, n_va = -13, "top"
        # In 2023 (idx=2), 115 vs 121 are close vertically; nudge left/right cleanly
        n_xoff = -14 if idx == 2 else (14 if idx == 5 else 0)
        a_xoff = 14 if idx == 2 else (14 if idx == 5 else 0)
        ax2_r.annotate(
            f"{n_dio}天",
            xy=(x[idx], n_dio),
            xytext=(n_xoff, n_off),
            textcoords="offset points",
            ha="center",
            va=n_va,
            fontsize=8.7,
            color=NVDA_LINE,
            fontweight="bold",
            bbox=PILL_BBOX,
            zorder=6,
        )
        ax2_r.annotate(
            f"{a_dio}天",
            xy=(x[idx], a_dio),
            xytext=(a_xoff, a_off),
            textcoords="offset points",
            ha="center",
            va=a_va,
            fontsize=8.7,
            color=AMD_LINE,
            fontweight="bold",
            bbox=PILL_BBOX,
            zorder=6,
        )

    ax2.set_title(
        "表外上游锁产军备竞赛 ($B 亿美元) vs 存货周转周期 (DIO 天数)",
        fontsize=13.2,
        fontweight="bold",
        color=TEXT_MAIN,
        pad=14,
    )
    ax2.set_xticks(x)
    ax2.set_xticklabels(PERIODS, fontsize=9.4, color=TEXT_MAIN)
    ax2.set_ylabel("表外制造与采购承诺金额 (亿美元)", fontsize=10.5, color=TEXT_MUTED)
    ax2_r.set_ylabel("存货周转天数 DIO (天，平均存货口径)", fontsize=10.5, color=TEXT_MUTED)
    ax2.yaxis.set_major_formatter(mticker.StrMethodFormatter("${x:,.0f}亿"))
    ax2_r.yaxis.set_major_formatter(mticker.FormatStrFormatter("%d天"))
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
        "无晶圆厂芯片设计与算力平台跨周期对决：英伟达 NVDA vs 超威半导体 AMD（截至 2026 Q3 / FY27 Q3 官方财报）",
        fontsize=15.6,
        fontweight="bold",
        color=TEXT_MAIN,
        y=0.97,
    )

    fig.text(
        0.5,
        0.015,
        "数据来源：NVIDIA SEC 10-K (FY22–FY26) 及 FY27 Q3 8-K (EX-99.2/99.3，2026/10/25 止)；AMD SEC 10-K (2021–2025) 及 2026 Q3 10-Q (2026/09/26 止)。",
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
