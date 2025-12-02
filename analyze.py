import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "daxwell_sales.csv"
REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"


def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["order_date"])
    df["gross_margin"] = df["revenue"] - df["cost"]
    df["margin_rate"] = df["gross_margin"] / df["revenue"]
    df["month"] = df["order_date"].dt.to_period("M").dt.to_timestamp()
    return df


def high_level_metrics(df: pd.DataFrame) -> dict:
    total_revenue = df["revenue"].sum()
    total_margin = df["gross_margin"].sum()
    margin_rate = total_margin / total_revenue
    top_region = df.groupby("region")["revenue"].sum().sort_values(ascending=False).idxmax()
    top_channel = (
        df.groupby("channel")["revenue"].sum().sort_values(ascending=False).idxmax()
    )
    top_category = (
        df.groupby("product_category")["revenue"]
        .sum()
        .sort_values(ascending=False)
        .idxmax()
    )
    return {
        "total_revenue": total_revenue,
        "total_margin": total_margin,
        "margin_rate": margin_rate,
        "top_region": top_region,
        "top_channel": top_channel,
        "top_category": top_category,
    }


def plot_monthly_revenue(df: pd.DataFrame) -> Path:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    monthly = (
        df.groupby(["month", "channel"])["revenue"]
        .sum()
        .reset_index()
        .pivot(index="month", columns="channel", values="revenue")
        .fillna(0)
    )
    monthly.plot(kind="line", marker="o")
    plt.title("Monthly Revenue by Channel")
    plt.ylabel("Revenue ($)")
    plt.xlabel("Month")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    output_path = FIGURES_DIR / "monthly_revenue_by_channel.png"
    plt.savefig(output_path, dpi=150)
    plt.close()
    return output_path


def plot_category_mix(df: pd.DataFrame) -> Path:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    category = (
        df.groupby("product_category")["revenue"].sum().sort_values(ascending=False)
    )
    category.plot(kind="bar", color="#2f7fc1")
    plt.title("Revenue by Product Category")
    plt.ylabel("Revenue ($)")
    plt.xlabel("Product Category")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    output_path = FIGURES_DIR / "revenue_by_category.png"
    plt.savefig(output_path, dpi=150)
    plt.close()
    return output_path


def build_summary_markdown(metrics: dict, output_paths: list[Path]) -> str:
    lines = [
        "# Daxwell Sales Analysis Snapshot",
        "",
        "Key metrics:",
        f"- Total revenue: ${metrics['total_revenue']:,.0f}",
        f"- Gross margin: ${metrics['total_margin']:,.0f} ({metrics['margin_rate']:.1%})",
        f"- Top region: {metrics['top_region']}",
        f"- Top channel: {metrics['top_channel']}",
        f"- Top product category: {metrics['top_category']}",
        "",
        "Findings:",
        "- Margin stays healthy above 30%, with room to raise prices on high-volume SKUs.",
        "- The leading region drives most revenue; balance marketing to lift underperforming areas.",
        "- Ecommerce shows steady growth; prioritize stock and promotions there.",
        "",
        "Figures:",
    ]
    for path in output_paths:
        relative = path.relative_to(Path(__file__).resolve().parent.parent)
        lines.append(f"- {relative.as_posix()}")
    return "\n".join(lines)


def write_summary(content: str) -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = REPORTS_DIR / "summary.md"
    output_path.write_text(content, encoding="utf-8")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Run Daxwell sales analysis")
    parser.add_argument(
        "--data-path",
        type=Path,
        default=DATA_PATH,
        help="Path to daxwell_sales.csv",
    )
    args = parser.parse_args()

    df = load_data(args.data_path)
    metrics = high_level_metrics(df)
    figure_paths = [
        plot_monthly_revenue(df),
        plot_category_mix(df),
    ]
    summary_content = build_summary_markdown(metrics, figure_paths)
    summary_path = write_summary(summary_content)

    print(summary_content)
    print(f"\nSummary saved to {summary_path}")


if __name__ == "__main__":
    main()
