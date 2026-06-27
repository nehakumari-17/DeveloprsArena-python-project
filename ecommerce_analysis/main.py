"""
main.py  –  E-Commerce Sales Analysis
Week 4 Project: Complete Data Analysis Pipeline

Structure
---------
data/sales_data.csv      → raw input
visualizations/          → 4 PNG charts
report/analysis_report.txt → written insights
"""

import os
import sys
from datetime import datetime

import matplotlib
matplotlib.use("Agg")          # non-interactive backend (safe for all platforms)
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd


# ─── 0. DIRECTORY SETUP ──────────────────────────────────────────────────────

def setup_directories():
    for folder in ["data", "visualizations", "report"]:
        os.makedirs(folder, exist_ok=True)
    print("✓ Project directories ready")


# ─── 1. LOAD & VALIDATE ──────────────────────────────────────────────────────

REQUIRED_COLS = {"order_id", "product_category", "sales_amount", "quantity", "order_date"}


def load_data(filepath: str = "data/sales_data.csv") -> pd.DataFrame:
    """Load CSV with basic validation."""
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        sys.exit(f"✗ File not found: {filepath}\n  Run: python data/generate_data.py")
    except Exception as exc:
        sys.exit(f"✗ Could not read {filepath}: {exc}")

    missing = REQUIRED_COLS - set(df.columns)
    if missing:
        sys.exit(f"✗ Missing columns: {missing}")

    print(f"✓ Loaded  →  {len(df)} rows, {len(df.columns)} columns  [{filepath}]")
    return df


# ─── 2. CLEAN ────────────────────────────────────────────────────────────────

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicates, fix types, drop bad rows."""
    original = len(df)

    df = df.drop_duplicates()
    df = df.dropna(subset=["sales_amount", "product_category"])

    df["order_date"]   = pd.to_datetime(df["order_date"], errors="coerce")
    df                 = df.dropna(subset=["order_date"])

    df["sales_amount"] = pd.to_numeric(df["sales_amount"], errors="coerce")
    df["quantity"]     = pd.to_numeric(df["quantity"],     errors="coerce").fillna(1).astype(int)
    df                 = df[df["sales_amount"] > 0]

    df["month"]        = df["order_date"].dt.to_period("M")
    df["month_label"]  = df["order_date"].dt.strftime("%b %Y")

    print(f"✓ Cleaned →  {original} → {len(df)} rows  ({original - len(df)} dropped)")
    return df.reset_index(drop=True)


# ─── 3. ANALYSE ──────────────────────────────────────────────────────────────

def analyse(df: pd.DataFrame) -> dict:
    """Compute summary metrics and group-level breakdowns."""
    total_revenue   = df["sales_amount"].sum()
    total_orders    = len(df)
    avg_order_value = total_revenue / total_orders
    total_units     = df["quantity"].sum()

    by_category = (
        df.groupby("product_category", sort=False)
          .agg(
              revenue=("sales_amount", "sum"),
              orders =("order_id",     "count"),
              units  =("quantity",     "sum"),
          )
          .sort_values("revenue", ascending=False)
    )

    monthly = (
        df.groupby(["month", "month_label"])
          .agg(
              revenue=("sales_amount", "sum"),
              orders =("order_id",     "count"),
          )
          .reset_index()
          .sort_values("month")
    )

    results = {
        "total_revenue":   total_revenue,
        "total_orders":    total_orders,
        "avg_order_value": avg_order_value,
        "total_units":     total_units,
        "by_category":     by_category,
        "monthly":         monthly,
        "best_month":      monthly.loc[monthly["revenue"].idxmax(), "month_label"],
        "worst_month":     monthly.loc[monthly["revenue"].idxmin(), "month_label"],
        "best_category":   by_category["revenue"].idxmax(),
    }

    print(f"\n{'─'*48}")
    print(f"  Total Revenue     : ₹{total_revenue:>12,.2f}")
    print(f"  Total Orders      : {total_orders:>12}")
    print(f"  Avg Order Value   : ₹{avg_order_value:>12,.2f}")
    print(f"  Total Units Sold  : {total_units:>12}")
    print(f"  Top Category      : {results['best_category']}")
    print(f"  Best Month        : {results['best_month']}")
    print(f"{'─'*48}\n")

    return results


# ─── 4. VISUALISE ────────────────────────────────────────────────────────────

PALETTE  = ["#4A90D9", "#E67E22", "#2ECC71", "#9B59B6", "#E74C3C",
            "#1ABC9C", "#F39C12", "#3498DB"]
BG_COLOR = "#f4f6f9"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top":   False,
    "axes.spines.right": False,
})

def _inr(x, _=None):
    return f"₹{x:,.0f}"


def chart_bar_category(by_category: pd.DataFrame,
                        out: str = "visualizations/1_revenue_by_category.png"):
    """Chart 1 – Vertical bar: revenue by category."""
    cats   = by_category.index.tolist()
    revs   = by_category["revenue"].values
    colors = PALETTE[: len(cats)]

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(cats, revs, color=colors, edgecolor="white", linewidth=0.9, width=0.55)

    # Value labels above bars
    for bar, val in zip(bars, revs):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + revs.max() * 0.012,
            f"₹{val:,.0f}",
            ha="center", va="bottom", fontsize=8.5, fontweight="bold",
        )

    ax.set_title("Revenue by Product Category", fontsize=14, fontweight="bold", pad=14)
    ax.set_xlabel("Category", fontsize=11)
    ax.set_ylabel("Revenue (₹)", fontsize=11)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(_inr))
    ax.set_facecolor(BG_COLOR)
    fig.patch.set_facecolor("white")
    fig.tight_layout()
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✓ {out}")


def chart_line_monthly(monthly: pd.DataFrame,
                        out: str = "visualizations/2_monthly_revenue_trend.png"):
    """Chart 2 – Line: monthly revenue trend with area fill."""
    x      = range(len(monthly))
    revs   = monthly["revenue"].values
    labels = monthly["month_label"].tolist()

    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(x, revs, marker="o", linewidth=2.5, color="#4A90D9",
            markerfacecolor="white", markeredgewidth=2.2, markersize=8, zorder=3)
    ax.fill_between(x, revs, alpha=0.14, color="#4A90D9")

    # Annotate min / max
    for idx, val in enumerate(revs):
        if val == revs.max() or val == revs.min():
            label = f"₹{val:,.0f}"
            color = "#2ECC71" if val == revs.max() else "#E74C3C"
            ax.annotate(label, (idx, val), textcoords="offset points",
                        xytext=(0, 10 if val == revs.max() else -18),
                        ha="center", fontsize=8.5, color=color, fontweight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=40, ha="right", fontsize=8.5)
    ax.set_title("Monthly Revenue Trend (2025)", fontsize=14, fontweight="bold", pad=14)
    ax.set_ylabel("Revenue (₹)", fontsize=11)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(_inr))
    ax.grid(axis="y", linestyle="--", alpha=0.45)
    ax.set_facecolor(BG_COLOR)
    fig.patch.set_facecolor("white")
    fig.tight_layout()
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✓ {out}")


def chart_pie_share(by_category: pd.DataFrame,
                     out: str = "visualizations/3_revenue_share_pie.png"):
    """Chart 3 – Donut pie: revenue percentage share."""
    cats   = by_category.index.tolist()
    revs   = by_category["revenue"].values
    colors = PALETTE[: len(cats)]

    fig, ax = plt.subplots(figsize=(8, 6))
    wedges, texts, autotexts = ax.pie(
        revs, labels=cats, colors=colors,
        autopct="%1.1f%%", startangle=140, pctdistance=0.80,
        wedgeprops=dict(width=0.55, edgecolor="white", linewidth=2),
    )
    for at in autotexts:
        at.set_fontsize(9)
        at.set_fontweight("bold")
    ax.set_title("Revenue Share by Category", fontsize=14, fontweight="bold", pad=18)
    fig.patch.set_facecolor("white")
    fig.tight_layout()
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✓ {out}")


def chart_grouped_orders(by_category: pd.DataFrame,
                          out: str = "visualizations/4_orders_vs_revenue.png"):
    """Chart 4 – Horizontal grouped bar: orders vs revenue (normalised)."""
    cats  = by_category.index.tolist()
    y     = np.arange(len(cats))
    width = 0.35

    rev_n = by_category["revenue"].values / by_category["revenue"].max()
    ord_n = by_category["orders"].values  / by_category["orders"].max()

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh(y - width / 2, rev_n, width, label="Revenue (norm.)", color="#4A90D9", edgecolor="white")
    ax.barh(y + width / 2, ord_n, width, label="Orders (norm.)",  color="#E67E22", edgecolor="white")

    ax.set_yticks(y)
    ax.set_yticklabels(cats, fontsize=10)
    ax.set_xlabel("Normalised Value  (1 = highest)", fontsize=10)
    ax.set_title("Revenue vs Order Volume per Category", fontsize=13, fontweight="bold", pad=14)
    ax.legend(fontsize=10)
    ax.grid(axis="x", linestyle="--", alpha=0.4)
    ax.set_facecolor(BG_COLOR)
    fig.patch.set_facecolor("white")
    fig.tight_layout()
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✓ {out}")


# ─── 5. REPORT ───────────────────────────────────────────────────────────────

def write_report(results: dict, out: str = "report/analysis_report.txt"):
    r  = results
    bc = r["by_category"]
    mn = r["monthly"]
    W  = 58

    def rule(char="─"): return char * W
    def h(title):       return f"\n{rule()}\n  {title}\n{rule()}"

    lines = [
        "=" * W,
        "       E-COMMERCE SALES ANALYSIS — FULL REPORT",
        f"       Generated : {datetime.now().strftime('%d %b %Y  %H:%M')}",
        "=" * W,
        h("EXECUTIVE SUMMARY"),
        f"  Total Revenue         ₹{r['total_revenue']:>12,.2f}",
        f"  Total Orders           {r['total_orders']:>12}",
        f"  Average Order Value   ₹{r['avg_order_value']:>12,.2f}",
        f"  Total Units Sold       {r['total_units']:>12}",
        f"  Best Month             {r['best_month']}",
        f"  Worst Month            {r['worst_month']}",
        f"  Top Category           {r['best_category']}",
        h("REVENUE BREAKDOWN BY CATEGORY"),
        f"  {'Category':<22} {'Revenue':>12}  {'Share':>6}  {'Orders':>6}  {'Units':>5}",
        f"  {rule('-')}",
    ]
    for cat, row in bc.iterrows():
        pct = row["revenue"] / r["total_revenue"] * 100
        lines.append(
            f"  {cat:<22} ₹{row['revenue']:>11,.2f}  {pct:>5.1f}%  {int(row['orders']):>6}  {int(row['units']):>5}"
        )

    lines += [h("MONTHLY REVENUE"),
              f"  {'Month':<14} {'Revenue':>12}  {'Orders':>7}"]
    lines.append(f"  {rule('-')}")
    for _, row in mn.iterrows():
        lines.append(f"  {row['month_label']:<14} ₹{row['revenue']:>11,.2f}  {int(row['orders']):>7}")

    lines += [
        h("KEY INSIGHTS"),
        f"  1. {r['best_category']} generates the highest revenue across all categories.",
        f"  2. Peak sales month was {r['best_month']} — ideal for promotions.",
        f"  3. Average order value of ₹{r['avg_order_value']:,.2f} reflects mid-to-premium spending.",
        f"  4. All {len(bc)} categories are active, reducing revenue concentration risk.",
        "",
        h("RECOMMENDATIONS"),
        f"  • Increase inventory for {r['best_category']} ahead of peak season.",
        f"  • Run discount campaigns during {r['worst_month']} to lift slow-month sales.",
        "  • Introduce product bundles to raise average order value.",
        "  • Analyse low-performing categories for potential discontinuation.",
        "",
        "=" * W,
        "  Visualizations saved in  visualizations/",
        "=" * W,
    ]

    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  ✓ {out}")


# ─── MAIN ────────────────────────────────────────────────────────────────────

def main():
    print("\n" + "═" * 48)
    print("   🛒  E-Commerce Sales Analysis  🛒")
    print("═" * 48 + "\n")

    setup_directories()

    df      = load_data("data/sales_data.csv")
    df      = clean_data(df)
    results = analyse(df)

    print("Generating visualizations …")
    chart_bar_category(results["by_category"])
    chart_line_monthly(results["monthly"])
    chart_pie_share(results["by_category"])
    chart_grouped_orders(results["by_category"])

    print("\nWriting report …")
    write_report(results)

    print("\n✅  All done!  Check  visualizations/  and  report/\n")


if __name__ == "__main__":
    main()
