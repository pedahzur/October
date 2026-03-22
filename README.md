# Replication Materials: Embedded Response Capacity (ERC)

## Overview

This package contains the data and code needed to replicate all quantitative analyses reported in the manuscript "Embedded Response Capacity: Organizational Resilience and Crisis Response in the Israeli Security System on October 7, 2023."

## Files

```
replication/
├── README.md                  ← This file
├── ERC_analysis.py            ← Main analysis script (H1–H5 statistical tests)
├── ERC_figures.py             ← Figure generation script (Figures 2–9)
├── fatalities.csv             ← Dataset 2: Security personnel fatalities (N=369)
├── locations_units.csv        ← Dataset 1: Combat participation by location (N=37)
├── results/                   ← Output directory for analysis log
│   └── ERC_analysis_output.txt
└── figures/                   ← Output directory for figures
    ├── Fig2_Temporal_Distribution.pdf
    ├── Fig3_Cumulative_Distribution.pdf
    ├── Fig4_Composition.pdf
    ├── Fig5_SelfJoining_Subgroups.pdf
    ├── Fig6_Predicted_Probabilities.pdf
    ├── Fig7_Forest_Plot.pdf
    ├── Fig8_Diversity.pdf
    └── Fig9_Response_Kidnapping.pdf
```

## Requirements

- Python 3.9 or later
- Required packages:

```bash
pip install numpy scipy statsmodels pandas matplotlib
```

## Usage

1. Place `fatalities.csv` and `locations_units.csv` in the same directory as the scripts.

2. Run the statistical analysis:

```bash
python ERC_analysis.py
```

This produces `results/ERC_analysis_output.txt` containing all test statistics, tables, and model outputs reported in the manuscript.

3. Generate the figures:

```bash
python ERC_figures.py
```

This produces PDF and PNG versions of all figures in the `figures/` directory.

## Dataset Descriptions

### Dataset 1: Combat Participation (`locations_units.csv`)

- **Unit of analysis:** Combat location
- **N:** 37 locations (32 with documented military response, 5 without)
- **Key variables:** Location name, geographic coordinates, responding units (up to 35 per location), time of attack onset, fatalities, injured, kidnapped
- **Sources:** IDF official documentation, Kan 360 investigative reports, verified public sources

### Dataset 2: Security Personnel Fatalities (`fatalities.csv`)

- **Unit of analysis:** Individual fatality
- **N:** 369
- **Key variables:** Name, gender, rank, service status (conscript/reserves/professional), unit, organizational branch (Military/Police/Shin Bet/Emergency Response Team), SOF membership, officer status, combat role, mode of joining (stationed/self-joined), time of death, location, time until operational control
- **Sources:** Israeli Ministry of Defense memorial database, Israel Police memorial records, public documentation projects, verified media reports

### Dataset 3: Special Operations Units

Dataset 3 (N=230 units, 63 variables) is used for qualitative institutional analysis and is not included in this replication package as it does not produce quantitative results. It is available from the author upon request.

## Hypothesis–Analysis Mapping

| Hypothesis | Analysis | Script Function |
|---|---|---|
| H1: Two-Wave Response | Mann-Whitney U, Welch's t, KS test, chi-square (early vs. late) | `test_h1()` |
| H2: Voluntary Mobilization | Proportions, binomial tests, chi-square by subgroup | `test_h2()` |
| H3: ERC Profile | Logistic regression (SOF, officer, service status, branch) | `test_h3()` |
| H4: Ad Hoc Team Formation | Organizational diversity per location, branch diversity | `test_h4()` |

## Notes

- The `fatalities.csv` file must use the column names as provided. The analysis script expects specific Hebrew and English column names from the original dataset.
- Emergency Response Team members (N=43) are excluded from the H3 logistic regression due to perfect separation (all self-joined) and reported separately.
- Figures 6 and 7 use hardcoded regression results for visual consistency. The underlying model is estimated in `ERC_analysis.py`.

## Contact

For questions about the data or replication code, contact the corresponding author.
