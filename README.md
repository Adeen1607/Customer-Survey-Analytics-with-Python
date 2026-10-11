# Customer Survey Analytics with Python

A reproducible analytics case study that summarizes customer department visits and product purchase preferences from a small survey dataset. The project demonstrates data preparation, validation, aggregation, and business-focused visualization with Python.

> **Data note:** the original survey contained a limited number of responses. The `*_expanded.xlsx` files include simulated binary observations created for visualization practice. Results from the expanded files are illustrative and must not be interpreted as population estimates or real customer behaviour.

## Business questions

- Which departments receive the highest share of reported visits?
- Which product categories are purchased most often?
- How concentrated are responses among the top five departments and products?
- What validation checks are needed before survey indicators are aggregated?

## Project structure

| Path | Purpose |
|---|---|
| `department_results.xlsx` | Original department-response table |
| `product_results.xlsx` | Original product-response table |
| `department_results_expanded.xlsx` | Original and simulated department observations |
| `product_results_expanded.xlsx` | Original and simulated product observations |
| `DataModeling.ipynb` | Initial data-expansion exploration |
| `Data_Analysis.ipynb` | Exploratory charts and ranked summaries |
| `src/prepare_data.py` | Deterministic data expansion with schema checks |
| `src/analyze_survey.py` | Reproducible summary tables and chart generation |
| `docs/METHODOLOGY.md` | Assumptions, limitations, and interpretation guidance |

## Analytical workflow

1. Load the department and product survey tables.
2. Verify identifier, category, and binary indicator fields.
3. Create reproducible simulated rows with a fixed random seed when requested.
4. Aggregate indicator columns into visit and purchase counts.
5. Rank the leading departments and products.
6. Export reusable CSV summaries and PNG charts.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python src/prepare_data.py --input-dir . --output-dir data/processed --rows 230 --seed 42
python src/analyze_survey.py --input-dir data/processed --output-dir artifacts
```

On Windows PowerShell, activate the environment with `.venv\Scripts\Activate.ps1`.

## Outputs

The analysis script generates:

- `department_totals.csv` and `product_totals.csv`
- top-five department and product rankings
- bar charts for overall and top-five response counts
- a product-purchase treemap
- department and product share charts

## Tools demonstrated

Python, pandas, NumPy, Matplotlib, Squarify, Excel ingestion, data validation, synthetic-data controls, exploratory data analysis, and data visualization.

## Responsible interpretation

This repository is a portfolio exercise in analytical workflow design. The original sample is small and the expanded rows are simulated independently; therefore, the charts demonstrate reporting technique rather than statistically reliable market conclusions. See [the methodology](docs/METHODOLOGY.md) before using or presenting any result.


## Rebuild the reading edition

```bash
python -m pip install -r requirements-research.txt
python scripts/build_research_site.py
```

This renders saved notebook outputs without rerunning model training or external APIs. To refresh findings, run the analysis commands above first, update `reports/research-findings.md`, and rebuild.

<!-- research-edition:start -->
## Research edition

[Research report and final visual results](research/report.md) · [Browser-ready notebook catalogue](research/notebooks.html)

The original survey workbooks are a small observed sample. DataModeling.ipynb expands them with independently simulated binary observations; Data_Analysis.ipynb plots expanded observations. Those charts demonstrate visual reporting only. They do not strengthen population inference; use separately labelled original-sample summaries for empirical interpretation.


The `research/` folder contains a professional static reading edition. The Pages workflow deploys it after GitHub Pages is enabled with **GitHub Actions** as the publishing source. Intended URL: `https://adeen1607.github.io/Customer-Survey-Analytics-with-Python/`. Deployment status must be checked in Actions before treating that address as live.

<!-- research-edition:end -->
