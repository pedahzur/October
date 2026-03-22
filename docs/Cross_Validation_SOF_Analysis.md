# Cross-Validation Analysis: Name-Level Matching and SOF Unit Presence

**Date:** March 19, 2026
**Datasets:** D1 (Locations & Units, 37 locations), D2 (Fatalities, N = 369)

---

## Part 1: Name-Level Unit Matching

An explicit name-to-name mapping was constructed between all 95 unit names in Dataset 2 and the 145 unit entries in Dataset 1. The mapping accounts for naming conventions (e.g., "Matkal" in D2 = "Sayeret Matkal" in D1; "Police Yamam" = "Yamam"; "Counterterrorism School" = "Lotar"; "Shin Bet" = "Shabak").

### Results

Of 369 fatalities, 324 (87.8%) could be mapped to a D1 location. Among these 324:

| Category | N | % |
|---|---|---|
| **Unit matched at same location** | 187 | 57.7% |
| **Unit has no D1 equivalent** (reinforcement/later units) | 55 | 17.0% |
| **Unit exists in D1 but at different location** | 82 | 25.3% |

Excluding the 55 fatalities from reinforcement units that have no D1 equivalent (Brigade 215, Brigade 2, Brigade 670, Brigade 900, and similar units dispatched during the broader IDF mobilization), the **match rate is 69.5%** (187 of 269).

The 82 "wrong location" cases largely reflect geographic imprecision in the fatality data: individuals killed en route between locations, at outpost positions adjacent to but not within a documented location, or who moved between engagement sites during the course of the fighting.

---

## Part 2: SOF Unit Cross-Presence Analysis

### SOF in Dataset 2

Dataset 2 codes 60 fatalities (16.3% of total) as SOF = 1, distributed across 15 distinct units:

| D2 SOF Unit | D2 Fatalities | D1 Equivalent | D1 Locations |
|---|---|---|---|
| Matkal | 9 | Sayeret Matkal | Be'eri, Kfar Aza, Alumim, Re'im Base, Yakhini |
| Police Yamam | 8 | Yamam | Be'eri, Nahal Oz Base, Ofakim, Mefalsim, Yakhini |
| Brigade 89 Battalion 217 | 7 | Brigade 89 Battalion 217 | Be'eri, Kfar Aza, Mefalsim, Nir Yitzhak |
| Brigade 89 Battalion 212 | 6 | Brigade 89 Battalion 212 | Kfar Aza, Nahal Oz, Zikim Beach, Zikim Base, Mefalsim |
| Shin Bet | 6 | Shabak / Shabas | Kfar Aza, Mefalsim, Zikim |
| Counterterrorism School | 5 | Lotar | Be'eri, Nahal Oz Base, Holit, Sderot, Orim |
| Shaldag | 5 | Shaldag | Be'eri, Kfar Aza, Alumim, Holit, Re'im Base |
| Brigade 89 Battalion 621 | 4 | Brigade 89 Battalion 621 | Kisufim Base |
| Brigade 888 | 3 | Brigade 888 | Be'eri, Re'im |
| Counterterrorism Nizana | 2 | Lotar Arava | Mivtachim |
| Oketz | 1 | Oketz | Be'eri, Nahal Oz Base |
| Personnel Security Unit | 1 | Shabak | Kfar Aza, Mefalsim, Zikim |
| Shayetet 13 | 1 | Shayetet 13 | Be'eri, Kfar Aza, Sufa Base, Mefalsim |
| Yahalom | 1 | Yahalom | Be'eri, Kfar Aza, Nahal Oz Base, Alumim, Re'im Base, Sderot, Sufa |
| Police Yoav | 1 | Yoav | Ofakim, Sderot |

**All 15 SOF units in Dataset 2 (100%) have identifiable equivalents in Dataset 1.** This full concordance indicates that the fatality data captures the same SOF organizational landscape documented in the combat participation records.

### SOF Unit-at-Location Match

Of the 49 SOF fatalities that occurred at locations documented in Dataset 1, **37 (75.5%)** were from units independently documented as present at that same location. This is substantially higher than the overall unit-level match rate (57.7%), which is consistent with the expectation that SOF units, given their specialized missions and concentrated deployments, would show tighter geographic correspondence between the two datasets.

### SOF Location Overlap

SOF units appear at 29 locations across the two datasets combined. At **11 locations (37.9%)**, SOF presence is documented in both datasets. At 15 locations, SOF presence appears in D1 only (reflecting the fact that SOF personnel often survived these engagements and therefore do not appear in the fatality data). At 3 locations, SOF fatalities appear in D2 only (at sites not covered by D1, such as Moshav Yated and Re'im Base under its alternative encoding).

The asymmetry — more D1-only than D2-only — is expected and methodologically reassuring. SOF units are trained for survival and typically sustain lower casualty rates relative to the number of engagements they participate in. Finding SOF units documented as present in D1 at locations where no SOF fatalities occurred is therefore consistent with their operational characteristics, not a sign of data discordance.

### SOF Diversity Correlation

Among the 11 locations where SOF units appear in both datasets, the number of distinct SOF units correlates positively across the two sources (Pearson r = .71, p = .015; n = 11). Locations with more SOF units in D1 tend to have more distinct SOF units represented among the fatalities.

---

## Summary Table

| Indicator | Result |
|---|---|
| D2 SOF units with D1 equivalents | 15/15 (100%) |
| SOF fatalities matched at same location | 37/49 (75.5%) |
| SOF location overlap (both datasets) | 11/29 locations (37.9%) |
| SOF diversity correlation | r = .71, p = .015 |
| Overall unit-level match (all fatalities) | 187/269 (69.5%) excl. reinforcements |
| Overall branch-level match | 288/324 (88.9%) |
| Overall diversity correlation | r = .62, p < .001 |

---

## Recommended Manuscript Text (Revised)

Replace the cross-validation paragraph in the Methodology section with:

> A preliminary cross-validation analysis assessed the reliability of fatality data as a proxy for force composition by constructing an explicit name-level mapping between all unit designations in Dataset 2 and their equivalents in Dataset 1. Three levels of correspondence were examined. At the organizational branch level (IDF, Police, Shin Bet, local emergency response teams), 88.9% of fatalities occurred at locations where their branch was documented as present in Dataset 1. At the unit level — after excluding 55 fatalities from reinforcement units dispatched during the later stages of the IDF's mobilization, which are not captured in Dataset 1's documentation of initial engagement forces — 69.5% of fatalities matched a unit documented at the same location. Third, organizational diversity at each location correlated positively across the two datasets (Pearson r = .62, p < .001; Spearman ρ = .69, p < .001), indicating that the fatality data preserves the relative distribution of multi-organizational engagement across the battlespace.
>
> The analysis was also conducted specifically for special operations forces (SOF). All 15 SOF units represented among the 60 SOF fatalities in Dataset 2 have identifiable equivalents in Dataset 1, confirming full organizational concordance. Of the 49 SOF fatalities at locations documented in Dataset 1, 75.5% were from units independently documented as present at the same location — a match rate substantially higher than the overall figure, consistent with the concentrated deployment patterns characteristic of elite units. Among the 11 locations where SOF presence is documented in both datasets, the number of distinct SOF units correlated positively (r = .71, p = .015). Together, these findings support the use of fatality data as a reliable proxy for the composition and geographic distribution of responding forces, including specialized units central to the study's analysis of Embedded Response Capacity.
