# Methodology and limitations

## Purpose

This project demonstrates a reproducible workflow for transforming binary survey responses into ranked summaries and visual reports. It is suitable for reviewing Python analytics, validation, and communication practices. It is not a market-research study.

## Data structure

Each workbook follows the same positional design:

1. a unique response identifier;
2. a respondent-level category field;
3. binary indicator columns, where `1` records a selected department or product and `0` records no selection.

The analysis aggregates only the binary indicator fields. Missing indicator values are treated as zero after validation.

## Observed and simulated data

The files without `_expanded` contain the original small survey sample. The expanded files append simulated rows so that the original visualization exercise has enough records to produce varied charts.

The preparation script makes that expansion reproducible by:

- using NumPy's generator with an explicit seed;
- checking that identifiers are complete and unique;
- checking that all indicator fields contain only zero, one, or missing values;
- preserving the source workbook's column order;
- reporting observed and simulated row counts separately in the command output.

The simulated indicator values are independent Bernoulli draws with equal probability. Categories are sampled from values observed in the original table. This approach is appropriate only for software and visualization practice.

## Analytical outputs

For each table, the workflow calculates:

- total selections by indicator;
- descending category rank;
- top-five categories;
- percentage share of all selections.

Because respondents may select more than one indicator, the percentage charts represent share of selections rather than share of unique respondents.

## Limitations

- The original sample size is limited.
- The sampling frame and response rate are not documented.
- Simulated rows do not preserve relationships among categories or respondent preferences.
- Equal-probability simulation can materially alter category rank and distribution.
- No confidence intervals or population-level inference should be produced from the expanded data.
- Results should not be used for operational, merchandising, or investment decisions.

## Recommended production design

A production survey pipeline should retain a row-level provenance field, separate observed and simulated datasets, document the questionnaire and sampling process, test for duplicate submissions, and report uncertainty alongside descriptive metrics.
