"""Generate an interactive Plotly HTML dashboard from the cleaned Superstore dataset."""

from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "superstore_cleaned.csv"
DASHBOARD_PATH = PROJECT_ROOT / "dashboards" / "sales_dashboard.html"


def build_dashboard(df: pd.DataFrame, output_path: Path = DASHBOARD_PATH) -> None:
    """Create and save a 2x2 interactive Plotly sales & profit dashboard."""
    cat_summary = (
        df.groupby("category", as_index=False)[["sales", "profit"]]
        .sum()
        .sort_values("sales", ascending=False)
    )
    region_summary = (
        df.groupby("region", as_index=False)[["sales", "profit"]]
        .sum()
        .sort_values("sales", ascending=False)
    )
    monthly_summary = (
        df.groupby("order_year_month", as_index=False)[["sales", "profit"]]
        .sum()
        .sort_values("order_year_month")
    )
    subcat_profit = (
        df.groupby("sub_category", as_index=False)[["sales", "profit"]]
        .sum()
        .sort_values("profit", ascending=True)
    )

    fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=(
            "Sales vs Profit by Category",
            "Sales by Region",
            "Monthly Sales & Profit Trend",
            "Profit by Sub-Category",
        ),
        specs=[[{"type": "bar"}, {"type": "pie"}], [{"type": "scatter"}, {"type": "bar"}]],
        vertical_spacing=0.16,
        horizontal_spacing=0.12,
    )

    # Panel 1: Category Sales & Profit
    fig.add_trace(
        go.Bar(name="Sales", x=cat_summary["category"], y=cat_summary["sales"], marker_color="#2563eb"),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Bar(name="Profit", x=cat_summary["category"], y=cat_summary["profit"], marker_color="#16a34a"),
        row=1,
        col=1,
    )

    # Panel 2: Regional Share
    fig.add_trace(
        go.Pie(
            labels=region_summary["region"],
            values=region_summary["sales"],
            hole=0.4,
            textinfo="label+percent",
            showlegend=False,
        ),
        row=1,
        col=2,
    )

    # Panel 3: Monthly Trend
    fig.add_trace(
        go.Scatter(
            name="Monthly Sales",
            x=monthly_summary["order_year_month"],
            y=monthly_summary["sales"],
            mode="lines+markers",
            line=dict(color="#2563eb", width=2),
        ),
        row=2,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            name="Monthly Profit",
            x=monthly_summary["order_year_month"],
            y=monthly_summary["profit"],
            mode="lines+markers",
            line=dict(color="#16a34a", width=2),
        ),
        row=2,
        col=1,
    )

    # Panel 4: Sub-Category Profit
    colors = ["#dc2626" if val < 0 else "#0d9488" for val in subcat_profit["profit"]]
    fig.add_trace(
        go.Bar(
            name="Sub-Category Profit",
            x=subcat_profit["profit"],
            y=subcat_profit["sub_category"],
            orientation="h",
            marker_color=colors,
            showlegend=False,
        ),
        row=2,
        col=2,
    )

    total_sales = df["sales"].sum()
    total_profit = df["profit"].sum()
    margin = (total_profit / total_sales) * 100
    fig.update_layout(
        title=(
            f"Superstore Sales & Profit Dashboard | "
            f"Total Sales: ${total_sales:,.0f} | Total Profit: ${total_profit:,.0f} | "
            f"Margin: {margin:.2f}%"
        ),
        height=850,
        template="plotly_white",
        barmode="group",
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(output_path, include_plotlyjs="cdn")
    print(f"Saved interactive dashboard: {output_path}")


def main() -> None:
    df = pd.read_csv(DATA_PATH)
    build_dashboard(df)


if __name__ == "__main__":
    main()

