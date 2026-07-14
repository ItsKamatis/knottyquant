from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter, PercentFormatter


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
RATES = PUBLIC / "assets" / "data" / "rates"
PORTFOLIO = PUBLIC / "assets" / "data" / "portfolio"
OUT = PUBLIC / "images" / "research"

INK = "#142923"
INK_2 = "#233b34"
TEXT = "#4d5f59"
PAPER = "#fbf9f4"
PAPER_DEEP = "#e9e2d5"
RULE = "#c9c2b5"
SAGE = "#dbe4dd"
TEAL = "#2f6b62"
RUST = "#a84a32"
OCHRE = "#a97322"
BLUE = "#3c6684"


def setup():
    plt.rcParams.update(
        {
            "figure.facecolor": PAPER,
            "axes.facecolor": PAPER,
            "savefig.facecolor": PAPER,
            "font.family": "DejaVu Sans",
            "font.size": 11,
            "axes.edgecolor": RULE,
            "axes.labelcolor": TEXT,
            "axes.titlecolor": INK,
            "xtick.color": TEXT,
            "ytick.color": TEXT,
            "grid.color": RULE,
            "grid.alpha": 0.55,
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )


def title(ax, heading, note):
    ax.set_title(heading, loc="left", fontsize=16, fontweight="bold", pad=16)
    ax.text(0, 1.01, note, transform=ax.transAxes, color=TEXT, fontsize=9, va="bottom")


def save(fig, name):
    fig.savefig(OUT / name, dpi=180, bbox_inches="tight", pad_inches=0.28)
    plt.close(fig)


def rates_curve():
    data = pd.read_csv(RATES / "curve_nodes.csv")
    fig, axes = plt.subplots(1, 2, figsize=(13.2, 6.2), gridspec_kw={"width_ratios": [1.3, 1]})
    ax = axes[0]
    ax.plot(data["time_years"], 100 * data["zero_rate_cc"], color=TEAL, lw=2.6, marker="o", ms=5, label="Continuous zero rate")
    ax.plot(data["time_years"], 100 * data["forward_rate_act360"], color=RUST, lw=2.2, marker="s", ms=4.5, label="Interval forward rate")
    title(ax, "Bootstrapped SOFR curve", "Synthetic OIS quotes, 2 July 2026")
    ax.set_xlabel("Maturity (years)")
    ax.set_ylabel("Rate (%)")
    ax.grid(axis="y")
    ax.legend(frameon=False, loc="lower right")
    ax = axes[1]
    ax.plot(data["time_years"], data["discount_factor"], color=INK_2, lw=2.7, marker="o", ms=5)
    ax.fill_between(data["time_years"], data["discount_factor"], 0, color=SAGE, alpha=0.72)
    title(ax, "Discount factors", "Log-linear interpolation; extrapolation forbidden")
    ax.set_xlabel("Maturity (years)")
    ax.set_ylabel("Discount factor")
    ax.set_ylim(0, 1.04)
    ax.grid(axis="y")
    fig.tight_layout(w_pad=3.2)
    save(fig, "rates-curve.png")


def rates_risk():
    key = pd.read_csv(RATES / "key_rate_dv01.csv")
    key = key[key["trade_id"] == "TOTAL"].copy()
    scenarios = pd.read_csv(RATES / "scenarios.csv")
    scenarios = scenarios[scenarios["trade_id"] == "TOTAL"].copy()
    scenario_order = ["parallel_up", "parallel_down", "steepener", "flattener"]
    scenarios["scenario"] = pd.Categorical(scenarios["scenario"], scenario_order, ordered=True)
    scenarios = scenarios.sort_values("scenario")

    fig, axes = plt.subplots(1, 2, figsize=(14.2, 6.3), gridspec_kw={"width_ratios": [1.3, 1]})
    ax = axes[0]
    colors = [TEAL if value >= 0 else RUST for value in key["key_rate_dv01"]]
    ax.bar(key["tenor"], key["key_rate_dv01"], color=colors, width=0.72)
    title(ax, "Net key-rate DV01", "USD per bp; central quote bumps and full rebootstrap")
    ax.set_xlabel("OIS quote tenor")
    ax.set_ylabel("USD per bp")
    ax.axhline(0, color=INK, lw=0.8)
    ax.grid(axis="y")
    ax.tick_params(axis="x", rotation=38)

    ax = axes[1]
    labels = ["Parallel +25", "Parallel -25", "Steepener", "Flattener"]
    values = scenarios["scenario_pnl"].to_numpy()
    colors = [RUST if value < 0 else TEAL for value in values]
    ax.barh(labels, values / 1000, color=colors, height=0.58)
    title(ax, "Full-revaluation scenarios", "Total change in model value, USD thousands")
    ax.set_xlabel("Change in model value (USD thousands)")
    ax.axvline(0, color=INK, lw=0.8)
    ax.grid(axis="x")
    for index, value in enumerate(values / 1000):
        ax.text(
            value - 3.0 if value > 0 else value + 3.0,
            index,
            f"{value:+.1f}",
            ha="right" if value > 0 else "left",
            va="center",
            color=PAPER,
            fontsize=9,
            fontweight="bold",
        )
    fig.tight_layout(w_pad=5.8)
    save(fig, "rates-risk.png")


def rates_pnl():
    data = pd.read_csv(RATES / "pnl_waterfall.csv")
    components = data[data["pnl_component"] == True].copy()  # noqa: E712
    labels = ["Carry / roll", "Curve move", "Amendments", "New trade", "Cash"]
    values = components["amount"].to_numpy()
    starts = np.r_[0.0, np.cumsum(values)[:-1]]
    total = values.sum()

    fig, ax = plt.subplots(figsize=(11.8, 6.2))
    colors = [TEAL if value >= 0 else RUST for value in values]
    ax.bar(np.arange(len(values)), values / 1000, bottom=starts / 1000, color=colors, width=0.66)
    running = np.r_[0.0, np.cumsum(values)] / 1000
    for i in range(len(values) - 1):
        ax.plot([i + 0.33, i + 1 - 0.33], [running[i + 1], running[i + 1]], color=RULE, lw=1.1)
    ax.bar(len(values) + 0.35, total / 1000, color=INK_2, width=0.66)
    ax.set_xticks([*range(len(values)), len(values) + 0.35], [*labels, "Explained change"], rotation=24, ha="right")
    title(ax, "Opening-to-closing value-change explain", "Model-value bridge; synthetic trades and ledger")
    ax.set_ylabel("Contribution (USD thousands)")
    ax.axhline(0, color=INK, lw=0.8)
    ax.grid(axis="y")
    for i, value in enumerate(values):
        endpoint = (starts[i] + value) / 1000
        label = f"{value / 1000:+.2f}" if abs(value) < 100 else f"{value / 1000:+.1f}"
        if abs(value) >= 5000:
            ax.text(i, (starts[i] + value / 2) / 1000, label, ha="center", va="center", fontsize=9, color=PAPER, fontweight="bold")
        else:
            ax.text(i, endpoint + (1.15 if value >= 0 else -1.25), label, ha="center", va="center", fontsize=9, color=INK)
    ax.text(len(values) + 0.35, total / 1000 + 1.6, f"{total / 1000:+.1f}", ha="center", fontsize=9, color=INK)
    fig.tight_layout()
    save(fig, "rates-value-change.png")


def portfolio_growth():
    data = pd.read_csv(PORTFOLIO / "monthly_results.csv")
    method_styles = {
        "equal_weight": ("Equal weight", TEXT, 1.7, "--"),
        "global_minimum_variance": ("Minimum variance", BLUE, 1.9, "-"),
        "shrinkage_mean_variance": ("Shrinkage mean-variance", TEAL, 2.6, "-"),
        "historical_joint_cvar": ("Historical CVaR", OCHRE, 1.9, "-"),
        "benchmark_relative_constrained": ("Benchmark-relative constrained", RUST, 2.6, "-"),
        "exact_cardinality_cvar": ("Exact-cardinality CVaR", INK_2, 1.8, ":"),
    }
    fig, ax = plt.subplots(figsize=(12.3, 6.5))
    for method, (label, color, width, style) in method_styles.items():
        subset = data[data["method"] == method].sort_values("month")
        wealth = (1 + subset["net_return"]).cumprod()
        ax.plot(pd.to_datetime(subset["month"]), wealth, label=label, color=color, lw=width, ls=style)
    title(ax, "Walk-forward comparison", "Public deterministic synthetic panel; net of modeled transaction costs")
    ax.set_ylabel("Growth of 1.00")
    ax.set_xlabel("Holding month")
    ax.grid(axis="y")
    ax.legend(frameon=False, ncol=2, fontsize=9, loc="upper left")
    fig.tight_layout()
    save(fig, "portfolio-growth.png")


def portfolio_tradeoffs():
    data = pd.read_csv(PORTFOLIO / "summary.csv")
    data = data[~data["method"].str.startswith("130_30")].copy()
    names = {
        "equal_weight": "Equal weight",
        "global_minimum_variance": "Minimum variance",
        "shrinkage_mean_variance": "Mean-variance",
        "maximum_sharpe_with_gmv_fallback": "Max Sharpe / GMV fallback",
        "historical_joint_cvar": "Historical CVaR",
        "benchmark_relative_constrained": "Benchmark-relative",
        "exact_cardinality_cvar": "Cardinality CVaR",
    }
    data["label"] = data["method"].map(names)
    colors = [RUST if m == "benchmark_relative_constrained" else TEAL if m == "shrinkage_mean_variance" else INK_2 for m in data["method"]]
    sizes = 150 + 1600 * data["average_monthly_one_way_turnover"].clip(lower=0)
    fig, ax = plt.subplots(figsize=(11.8, 6.5))
    ax.scatter(100 * data["annualized_volatility"], 100 * data["annualized_return"], s=sizes, c=colors, alpha=0.82, edgecolor=PAPER, linewidth=1.2)
    offsets = {
        "Equal weight": (5, 7),
        "Minimum variance": (7, -15),
        "Mean-variance": (-94, 8),
        "Max Sharpe / GMV fallback": (7, -17),
        "Historical CVaR": (-2, -18),
        "Benchmark-relative": (7, 6),
        "Cardinality CVaR": (7, 6),
    }
    for _, row in data.iterrows():
        dx, dy = offsets[row["label"]]
        ax.annotate(row["label"], (100 * row["annualized_volatility"], 100 * row["annualized_return"]), xytext=(dx, dy), textcoords="offset points", fontsize=9, color=INK)
    title(ax, "Return, risk, and turnover", "Bubble area reflects average monthly one-way turnover")
    ax.set_xlabel("Annualized volatility (%)")
    ax.set_ylabel("Annualized return (%)")
    ax.set_xlim(11.15, 13.15)
    ax.set_ylim(2.88, 6.38)
    ax.grid()
    fig.tight_layout()
    save(fig, "portfolio-tradeoffs.png")


def portfolio_attribution():
    data = pd.read_csv(PORTFOLIO / "active_attribution.csv")
    subset = data[data["method"] == "benchmark_relative_constrained"].copy()
    totals = subset.groupby("component", as_index=False)["contribution"].sum()
    order = ["factor:MKT_RF", "factor:SMB", "factor:HML", "factor:RMW", "factor:CMA", "factor:MOM", "specific", "transaction_cost"]
    labels = ["Market", "Size", "Value", "Profitability", "Investment", "Momentum", "Specific residual", "Transaction cost"]
    totals = totals.set_index("component").reindex(order).fillna(0)
    values = 100 * totals["contribution"].to_numpy()
    colors = [TEAL if value >= 0 else RUST for value in values]
    fig, ax = plt.subplots(figsize=(11.8, 6.3))
    bars = ax.barh(labels, values, color=colors, height=0.6)
    title(ax, "Active-return attribution", "Benchmark-relative method; sums of monthly arithmetic contributions")
    ax.set_xlabel("Contribution (percentage points)")
    ax.axvline(0, color=INK, lw=0.8)
    ax.grid(axis="x")
    ax.bar_label(bars, labels=[f"{v:+.2f}" for v in values], padding=4, fontsize=9, color=INK)
    fig.tight_layout()
    save(fig, "portfolio-attribution.png")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    setup()
    rates_curve()
    rates_risk()
    rates_pnl()
    portfolio_growth()
    portfolio_tradeoffs()
    portfolio_attribution()


if __name__ == "__main__":
    main()
