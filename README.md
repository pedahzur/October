# Replication Materials: Embedded Response Capacity (ERC)

## Overview

This repository contains the data and code needed to replicate all quantitative analyses reported in the manuscript "Embedded Response Capacity: Organizational Resilience and Crisis Response in the Israeli Security System on October 7, 2023."

## Repository Layout

```
October/
├── README.md                        ← This file
├── manuscript.md                    ← Manuscript (unit-deployment ranking)
├── data/                            ← All datasets
│   ├── fatalities.csv               ← Dataset 2: Security personnel fatalities (N=369)
│   ├── locations_units.csv          ← Dataset 1: Combat participation by location (N=37)
│   ├── day_of_oct7.csv              ← Day-of articles with verified publication dates
│   ├── urls_by_unit.txt             ← Source URLs organised by unit
│   ├── attack_locations_oct7.csv    ← Attack locations
│   ├── locations_units_oct7.csv     ← Location–unit mapping (Oct 7)
│   ├── evidence_matrix.csv          ← Unit × location evidence matrix
│   └── Locations and Units October 7 - Sheet1.csv
├── scripts/                         ← Analysis and utility scripts
│   ├── ERC_analysis.py              ← Main analysis script (H1–H5 statistical tests)
│   ├── ERC_figures.py               ← Figure generation script (Figures 2–9)
│   ├── batch_tag.py                 ← Batch tagging utility
│   └── export_readwise.py           ← Readwise export utility
├── results/                         ← Output from analysis scripts
│   └── ERC_analysis_output.txt      ← All test statistics, tables, and model outputs
├── figures/                         ← Publication-ready figures
│   ├── Fig2_Temporal_Distribution.png
│   ├── Fig3_Cumulative_Distribution.png
│   ├── Fig4_Composition.png
│   ├── Fig5_SelfJoining_Subgroups.png
│   ├── Fig6_Predicted_Probabilities.png
│   ├── Fig7_Forest_Plot.png
│   ├── Fig8_Diversity.png
│   ├── Fig9_Response_Kidnapping.png
│   └── H1–H5 exploratory figures
├── docs/                            ← Working documents and findings notes
│   ├── ERC.md
│   ├── Oct7_Collection_Organization_Plan.docx
│   ├── Cross_Validation_SOF_Analysis.md
│   ├── ERC_March_13_2026.md
│   ├── H1_Findings_Complete.md
│   ├── H2_Findings_Complete.md
│   ├── H3_Findings_Complete.md
│   └── H4_H5_Findings_Complete.md
├── locations/                       ← Location profiles
│   ├── README.md
│   ├── kibbutz_beeri.md
│   └── nova_festival.md
├── units/                           ← Unit profiles
│   ├── README.md
│   └── shaldag.md
├── sources/                         ← Source domain and reliability guide
│   └── README.md
└── references/                      ← Bibliography
    └── references.bib
```

## Requirements

- Python 3.9 or later
- Required packages:

```bash
pip install numpy scipy statsmodels pandas matplotlib
```

## Usage

Run all commands from the **repository root**.

1. Run the statistical analysis:

```bash
python scripts/ERC_analysis.py
```

This produces `results/ERC_analysis_output.txt` containing all test statistics, tables, and model outputs reported in the manuscript.

2. Generate the figures:

```bash
python scripts/ERC_figures.py
```

This produces PDF and PNG versions of all figures in the `figures/` directory.

## Dataset Descriptions

### Dataset 1: Combat Participation (`data/locations_units.csv`)

- **Unit of analysis:** Combat location
- **N:** 37 locations (32 with documented military response, 5 without)
- **Key variables:** Location name, geographic coordinates, responding units (up to 35 per location), time of attack onset, fatalities, injured, kidnapped
- **Sources:** IDF official documentation, Kan 360 investigative reports, verified public sources

### Dataset 2: Security Personnel Fatalities (`data/fatalities.csv`)

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

- The `data/fatalities.csv` file must use the column names as provided. The analysis script expects specific Hebrew and English column names from the original dataset.
- Emergency Response Team members (N=43) are excluded from the H3 logistic regression due to perfect separation (all self-joined) and reported separately.
- Figures 6 and 7 use hardcoded regression results for visual consistency. The underlying model is estimated in `scripts/ERC_analysis.py`.

## Contact

For questions about the data or replication code, contact the corresponding author.
