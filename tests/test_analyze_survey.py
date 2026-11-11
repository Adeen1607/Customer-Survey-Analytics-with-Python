"""Workbook validation tests for survey visualization inputs."""

import pandas as pd
import pytest

from src.analyze_survey import load_totals


def test_zero_response_workbook_fails_before_chart_generation(tmp_path):
    source = tmp_path / "survey.xlsx"
    pd.DataFrame({
        "id": [1, 2], "segment": ["A", "B"],
        "item_a": [0, 0], "item_b": [None, None],
    }).to_excel(source, index=False)
    with pytest.raises(ValueError, match="no positive indicator responses"):
        load_totals(source, "department")


def test_valid_indicator_totals_are_aggregated(tmp_path):
    source = tmp_path / "survey.xlsx"
    pd.DataFrame({
        "id": [1, 2], "segment": ["A", "B"],
        "item_a": [1, 1], "item_b": [0, 1],
    }).to_excel(source, index=False)
    totals = load_totals(source, "product")
    assert totals.to_dict() == {"item_a": 2, "item_b": 1}


def test_nonbinary_indicator_values_are_rejected(tmp_path):
    source = tmp_path / "survey.xlsx"
    pd.DataFrame({
        "id": [1], "segment": ["A"], "item_a": [2],
    }).to_excel(source, index=False)
    with pytest.raises(ValueError, match="non-binary indicator"):
        load_totals(source, "product")
