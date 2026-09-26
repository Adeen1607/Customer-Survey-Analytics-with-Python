"""Generate reusable survey summaries and portfolio-ready visual outputs."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import squarify


FILES = {
    "department": "department_results_expanded.xlsx",
    "product": "product_results_expanded.xlsx",
}
COLORS = {
    "department": "#2563EB",
    "product": "#059669",
}


def load_totals(path: Path, table_name: str) -> pd.Series:
    """Validate an expanded survey table and aggregate its indicator columns."""
    frame = pd.read_excel(path)
    if frame.shape[1] < 3:
        raise ValueError(f"{table_name}: expected at least three columns.")

    indicators = frame.iloc[:, 2:]
    invalid = [
        column
        for column in indicators
        if not indicators[column].dropna().isin([0, 1]).all()
    ]
    if invalid:
        raise ValueError(f"{table_name}: non-binary indicator columns: {invalid}")

    totals = indicators.fillna(0).sum().sort_values(ascending=False)
    totals.index.name = "category"
    totals.name = "response_count"
    return totals


def add_labels(axis: plt.Axes) -> None:
    for bar in axis.patches:
        height = bar.get_height()
        axis.annotate(
            f"{height:,.0f}",
            (bar.get_x() + bar.get_width() / 2, height),
            ha="center",
            va="bottom",
            xytext=(0, 4),
            textcoords="offset points",
            fontsize=9,
        )


def save_bar(series: pd.Series, title: str, ylabel: str, path: Path) -> None:
    figure, axis = plt.subplots(figsize=(11, 6))
    series.plot(kind="bar", ax=axis, color="#2563EB")
    axis.set_title(title, loc="left", fontweight="bold")
    axis.set_xlabel("")
    axis.set_ylabel(ylabel)
    axis.grid(axis="y", alpha=0.25)
    axis.tick_params(axis="x", rotation=40)
    add_labels(axis)
    figure.tight_layout()
    figure.savefig(path, dpi=160)
    plt.close(figure)


def save_share(series: pd.Series, title: str, path: Path) -> None:
    figure, axis = plt.subplots(figsize=(9, 7))
    series.plot(
        kind="pie",
        ax=axis,
        autopct="%1.1f%%",
        startangle=90,
        cmap="tab20",
        textprops={"fontsize": 8},
    )
    axis.set_title(title, loc="left", fontweight="bold")
    axis.set_ylabel("")
    figure.tight_layout()
    figure.savefig(path, dpi=160)
    plt.close(figure)


def save_treemap(series: pd.Series, title: str, path: Path) -> None:
    figure, axis = plt.subplots(figsize=(11, 6))
    labels = [f"{label}\n{value:,.0f}" for label, value in series.items()]
    squarify.plot(
        sizes=series.values,
        label=labels,
        alpha=0.85,
        color=plt.cm.Paired.colors,
        ax=axis,
        text_kwargs={"fontsize": 8},
    )
    axis.set_title(title, loc="left", fontweight="bold")
    axis.axis("off")
    figure.tight_layout()
    figure.savefig(path, dpi=160)
    plt.close(figure)


def analyze(input_dir: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    department_totals = load_totals(
        input_dir / FILES["department"], "department"
    )
    product_totals = load_totals(input_dir / FILES["product"], "product")

    for name, totals in (
        ("department", department_totals),
        ("product", product_totals),
    ):
        totals.to_csv(output_dir / f"{name}_totals.csv")
        totals.head(5).to_csv(output_dir / f"top_5_{name}.csv")

    save_bar(
        department_totals,
        "Reported Department Visits",
        "Response count",
        output_dir / "department_visits.png",
    )
    save_bar(
        product_totals,
        "Reported Product Purchases",
        "Response count",
        output_dir / "product_purchases.png",
    )
    save_bar(
        department_totals.head(5),
        "Top Five Departments",
        "Response count",
        output_dir / "top_5_departments.png",
    )
    save_bar(
        product_totals.head(5),
        "Top Five Products",
        "Response count",
        output_dir / "top_5_products.png",
    )
    save_share(
        department_totals,
        "Share of Reported Department Visits",
        output_dir / "department_share.png",
    )
    save_share(
        product_totals,
        "Share of Reported Product Purchases",
        output_dir / "product_share.png",
    )
    save_treemap(
        product_totals,
        "Product Purchase Mix",
        output_dir / "product_treemap.png",
    )
    print(f"Analysis outputs written to {output_dir}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze expanded survey workbooks.")
    parser.add_argument("--input-dir", type=Path, default=Path("data/processed"))
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts"))
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    analyze(arguments.input_dir, arguments.output_dir)
