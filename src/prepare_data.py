"""Create reproducible expanded survey tables for visualization practice."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


INPUT_FILES = {
    "department": "department_results.xlsx",
    "product": "product_results.xlsx",
}


def validate_table(frame: pd.DataFrame, table_name: str) -> tuple[str, str, list[str]]:
    """Validate the positional schema used by the original survey workbook."""
    if frame.shape[1] < 3:
        raise ValueError(f"{table_name} must contain an ID, a category, and indicators.")

    id_column = frame.columns[0]
    category_column = frame.columns[1]
    indicator_columns = list(frame.columns[2:])

    if frame[id_column].isna().any() or not frame[id_column].is_unique:
        raise ValueError(f"{table_name}: {id_column!r} must be complete and unique.")

    invalid = [
        column
        for column in indicator_columns
        if not frame[column].dropna().isin([0, 1]).all()
    ]
    if invalid:
        raise ValueError(
            f"{table_name}: expected binary values in indicator columns: {invalid}"
        )

    if frame[category_column].dropna().empty:
        raise ValueError(f"{table_name}: {category_column!r} has no usable values.")

    return id_column, category_column, indicator_columns


def expand_table(
    frame: pd.DataFrame,
    table_name: str,
    rows: int,
    rng: np.random.Generator,
) -> pd.DataFrame:
    """Append simulated rows while preserving the workbook's original schema."""
    id_column, category_column, indicator_columns = validate_table(frame, table_name)

    observed_ids = pd.to_numeric(frame[id_column], errors="raise")
    start_id = int(observed_ids.max()) + 1

    simulated = pd.DataFrame(
        rng.integers(0, 2, size=(rows, len(indicator_columns))),
        columns=indicator_columns,
    )
    simulated.insert(
        0,
        category_column,
        rng.choice(frame[category_column].dropna().unique(), size=rows),
    )
    simulated.insert(0, id_column, np.arange(start_id, start_id + rows))

    return pd.concat([frame, simulated], ignore_index=True)


def prepare(input_dir: Path, output_dir: Path, rows: int, seed: int) -> None:
    """Read, validate, expand, and export both survey tables."""
    if rows < 0:
        raise ValueError("--rows must be zero or greater.")

    output_dir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)

    for table_name, filename in INPUT_FILES.items():
        source = input_dir / filename
        frame = pd.read_excel(source)
        expanded = expand_table(frame, table_name, rows, rng)

        target = output_dir / filename.replace(".xlsx", "_expanded.xlsx")
        expanded.to_excel(target, index=False)
        print(
            f"{table_name}: {len(frame)} observed + {rows} simulated "
            f"= {len(expanded)} rows -> {target}"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build deterministic survey tables for visualization practice."
    )
    parser.add_argument("--input-dir", type=Path, default=Path("."))
    parser.add_argument("--output-dir", type=Path, default=Path("data/processed"))
    parser.add_argument("--rows", type=int, default=230)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    prepare(arguments.input_dir, arguments.output_dir, arguments.rows, arguments.seed)
