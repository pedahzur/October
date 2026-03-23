# Source Inventory: ERC — October 7 Crisis Response

## Summary
- Project: Embedded Response Capacity (ERC)
- Research question: How did Israeli security personnel achieve effective response despite C2 collapse on October 7?
- Collection period: 2024 – ongoing
- Total sources logged: 6 (datasets and source categories)
- Last updated: 2026-03-23

## Collection Status Overview

| Source Type | Total | Collected | Pending | Blocked | Notes |
|---|---|---|---|---|---|
| Archival documents | — | — | — | — | Not applicable |
| Interviews | 0 | 0 | TBD | — | Potential future phase |
| Survey responses | — | — | — | — | Not applicable |
| Fieldwork observations | — | — | — | — | Not applicable |
| Government documents | 3+ | 3+ | — | — | IDF official publications, Israel Police, Knesset testimonies |
| Newspaper/periodical sources | 50+ | 50+ | — | — | Hebrew and English media; see `sources/README.md` |
| Secondary datasets | 2 | 2 | 0 | — | Fatalities (N=369), Locations (N=37) |
| Other | 1 | 1 | 0 | — | Evidence matrix; unit-level qualitative dataset (N=230) |

## Source Categories

### DAT-001 — Fatalities Dataset
- **Type**: dataset
- **Title or description**: Security personnel fatalities, October 7–9, 2023
- **Repository / institution / location**: `data/fatalities.csv`
- **Date of source**: October 2023 events; compiled 2024–2026
- **Date collected / accessed**: Ongoing through March 2026
- **Language**: English (coded from Hebrew originals)
- **Collection status**: collected
- **Access restrictions**: open (replication package)
- **N**: 369 individuals
- **Variables**: name, gender, rank, service status, unit, branch, SOF membership, officer status, combat role, joining mode, time of death, location
- **Sources**: Israeli Ministry of Defense memorial database, Israel Police records, verified media
- **Relevance to research question**: Primary dataset for H1–H3 (temporal response, voluntary mobilization, ERC profile)
- **Quality / reliability notes**: Confidence levels assigned per `data/metadata.json`
- **Translation needed**: no (coded in English)

### DAT-002 — Location-Unit Deployment Dataset
- **Type**: dataset
- **Title or description**: Combat participation by location, October 7–9
- **Repository / institution / location**: `data/locations_units.csv`
- **Date of source**: October 2023 events; compiled 2024–2026
- **Date collected / accessed**: Ongoing through March 2026
- **Language**: English (canonical names from Hebrew)
- **Collection status**: collected
- **N**: 37 locations (32 with documented response, 5 without)
- **Variables**: location name, coordinates, responding units (up to 35), attack onset, fatalities, injured, kidnapped
- **Sources**: IDF official documentation, Kan 360, verified public sources
- **Relevance to research question**: Primary dataset for H4–H5 (ad hoc team formation, operational stabilization)
- **Quality / reliability notes**: Three-tier confidence (VERIFIED/LIKELY/UNCONFIRMED); see `data/metadata.json`

### DAT-003 — Evidence Matrix
- **Type**: dataset
- **Title or description**: Unit × location evidence matrix with source URLs
- **Repository / institution / location**: `data/evidence_matrix.csv`
- **Collection status**: collected
- **Relevance to research question**: Source traceability for all unit-location claims

### GOV-001 — IDF Official Publications
- **Type**: government document
- **Title or description**: IDF Spokesperson publications, unit battle reports, published inquiry findings
- **Repository / institution / location**: idf.il, iaf.org.il
- **Language**: Hebrew
- **Collection status**: collected (ongoing as new probes published)
- **Access restrictions**: open (published online)
- **Translation needed**: partial — key passages translated for manuscript
- **Quality / reliability notes**: Primary official source; PR-filtered but factually anchored; highest priority per metadata.json

### GOV-002 — Knesset Inquiry Testimonies
- **Type**: government document
- **Title or description**: Parliamentary inquiry testimonies and transcripts
- **Repository / institution / location**: knesset.gov.il
- **Language**: Hebrew
- **Collection status**: collected (partial; ongoing releases)
- **Translation needed**: partial

### PRS-001 — Hebrew and English Media Sources
- **Type**: newspaper / periodical
- **Title or description**: Probe-based reconstructions, investigative reports, and news coverage
- **Repository / institution / location**: Multiple — see `sources/README.md` for full domain list
- **Language**: Hebrew (primary), English (secondary)
- **Collection status**: collected (50+ articles indexed)
- **Access restrictions**: some paywalled (Haaretz)
- **Quality / reliability notes**: Probe-based reconstructions (Times of Israel) given priority; date metadata issues noted in sources/README.md
- **Translation needed**: partial — Hebrew sources translated for quotation

## Source Log

*Individual source entries to be added as the writing phase requires specific citations.*
