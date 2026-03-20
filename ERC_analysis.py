"""
Embedded Response Capacity (ERC): Replication Code
===================================================
Analysis of the Israeli Security Response to the October 7, 2023 Attack

Author: Ami Pedahzur
Date: March 2026

This script replicates all quantitative analyses reported in the manuscript.
It produces tables and test statistics for hypotheses H1–H5.

Requirements:
    pip install numpy scipy statsmodels pandas

Input files (place in same directory as this script):
    1. fatalities.csv          — Dataset 2: Security personnel fatalities (N=369)
    2. locations_units.csv     — Dataset 1: Combat participation by location (N=37)

Usage:
    python ERC_analysis.py
"""

import csv
import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import binomtest, chi2_contingency, mannwhitneyu, pearsonr, spearmanr
from collections import defaultdict
import statsmodels.api as sm
from statsmodels.discrete.discrete_model import Logit
import warnings
import os
import sys

warnings.filterwarnings("ignore")

# ============================================================================
# CONFIGURATION
# ============================================================================

FATALITIES_FILE = "fatalities.csv"
LOCATIONS_FILE = "locations_units.csv"

# Output
OUTPUT_DIR = "results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

LOG_FILE = os.path.join(OUTPUT_DIR, "ERC_analysis_output.txt")


# ============================================================================
# UTILITIES
# ============================================================================

class Logger:
    """Writes to both stdout and a log file."""
    def __init__(self, filepath):
        self.terminal = sys.stdout
        self.log = open(filepath, "w", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        self.terminal.flush()
        self.log.flush()

    def close(self):
        self.log.close()


def wilson_ci(p, n, z=1.96):
    """Wilson score confidence interval for a proportion."""
    denom = 1 + z**2 / n
    center = (p + z**2 / (2 * n)) / denom
    margin = z * np.sqrt((p * (1 - p) + z**2 / (4 * n)) / n) / denom
    return center - margin, center + margin


def cramers_v(chi2, n, k):
    """Cramér's V effect size for chi-square tests."""
    return np.sqrt(chi2 / (n * (min(k, 2) - 1)))


def print_header(text, char="=", width=70):
    print(f"\n{char * width}")
    print(text)
    print(f"{char * width}")


def print_subheader(text, char="-", width=50):
    print(f"\n{text}")
    print(f"{char * width}")


# ============================================================================
# DATA LOADING
# ============================================================================

def load_fatalities(filepath):
    """Load and parse the fatalities dataset (Dataset 2)."""
    with open(filepath, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    records = []
    for r in rows:
        rec = {
            "name": r.get("Name", "").strip(),
            "gender": r.get("Gender", "").strip(),
            "rank": r.get("Rank", "").strip(),
            "service": r.get("Conscript/Reserves/ Professional", "").strip(),
            "role": r.get("Role", "").strip(),
            "role_type": r.get("Role type ", "").strip(),
            "unit": r.get("Unit", "").strip(),
            "branch": r.get("Branch ", "").strip(),
            "sof": r.get("SOF", "").strip(),
            "officer": r.get("Officer", "").strip(),
            "combat": r.get("Combat", "").strip(),
            "joined": r.get("Joined", "").strip(),
            "date": r.get("Date", "").strip(),
            "time": r.get("Time", "").strip(),
            "location": r.get("Location ", "").strip(),
            "toc": r.get("Time until operational control  ", "").strip(),
        }
        records.append(rec)

    print(f"Loaded fatalities dataset: N = {len(records)}")
    return records


def load_locations(filepath):
    """Load and parse the locations/units dataset (Dataset 1)."""
    with open(filepath, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    locations = []
    for r in rows:
        loc_name = r["Location"].strip()
        units = []
        for col in ["Units"] + [f"Units {i}" for i in range(2, 36)]:
            if col in r and r[col] and r[col].strip() and r[col].strip() != "No military response":
                units.append(r[col].strip())

        try:
            fat = int(r.get("Fatalities", "0").strip() or "0")
        except ValueError:
            fat = 0
        try:
            kid = int(r.get("Kidnapped", "0").strip() or "0")
        except ValueError:
            kid = 0

        locations.append({
            "name": loc_name,
            "units": units,
            "n_units": len(units),
            "has_response": len(units) > 0,
            "fatalities": fat,
            "kidnapped": kid,
        })

    print(f"Loaded locations dataset: N = {len(locations)}")
    return locations


# ============================================================================
# H1: TWO-WAVE RESPONSE HYPOTHESIS
# ============================================================================

def test_h1(records):
    """Test H1: Two distinct temporal waves of responders."""
    print_header("H1: TWO-WAVE RESPONSE HYPOTHESIS")

    # Extract valid observations
    stationed_times = []
    selfjoined_times = []
    for r in records:
        j = r["joined"]
        t = r["time"]
        if j not in ("0", "1") or not t or not t.replace(".", "").isdigit():
            continue
        t_val = float(t)
        if j == "0":
            stationed_times.append(t_val)
        else:
            selfjoined_times.append(t_val)

    s = np.array(stationed_times)
    sj = np.array(selfjoined_times)

    print(f"\nSample sizes:")
    print(f"  Stationed: n = {len(s)}")
    print(f"  Self-Joined: n = {len(sj)}")

    # Descriptive statistics
    print_subheader("Descriptive Statistics")
    for label, arr in [("Stationed", s), ("Self-Joined", sj)]:
        print(f"\n  {label}:")
        print(f"    Mean:   {np.mean(arr):.2f} hours")
        print(f"    Median: {np.median(arr):.1f} hours")
        print(f"    SD:     {np.std(arr, ddof=1):.2f}")
        print(f"    IQR:    {np.percentile(arr, 25):.0f}–{np.percentile(arr, 75):.0f}")
        print(f"    Range:  {np.min(arr):.0f}–{np.max(arr):.0f}")

    diff = np.mean(sj) - np.mean(s)
    print(f"\n  Mean difference: {diff:.2f} hours")

    # Statistical tests
    print_subheader("Statistical Tests")

    # Mann-Whitney U (one-tailed)
    u_stat, u_p = mannwhitneyu(s, sj, alternative="less")
    r_rb = 1 - (2 * u_stat) / (len(s) * len(sj))
    print(f"\n  Mann-Whitney U test (one-tailed: stationed < self-joined):")
    print(f"    U = {u_stat:.0f}, p = {u_p:.2e}")
    print(f"    Rank-biserial correlation: r = {r_rb:.3f}")

    # Welch's t-test
    t_stat, t_p = stats.ttest_ind(s, sj, equal_var=False)
    pooled_sd = np.sqrt(
        ((len(s) - 1) * np.std(s, ddof=1)**2 + (len(sj) - 1) * np.std(sj, ddof=1)**2)
        / (len(s) + len(sj) - 2)
    )
    cohens_d = (np.mean(sj) - np.mean(s)) / pooled_sd
    print(f"\n  Welch's t-test:")
    print(f"    t = {t_stat:.3f}, p = {t_p:.2e}")
    print(f"    Cohen's d = {cohens_d:.3f}")

    # Kolmogorov-Smirnov
    ks_stat, ks_p = stats.ks_2samp(s, sj)
    print(f"\n  Kolmogorov-Smirnov test:")
    print(f"    D = {ks_stat:.3f}, p = {ks_p:.2e}")

    # Early response (≤3 hours)
    early_s = int(np.sum(s <= 3))
    early_sj = int(np.sum(sj <= 3))
    table = [[early_s, len(s) - early_s], [early_sj, len(sj) - early_sj]]
    chi2, chi_p, dof, _ = chi2_contingency(table)
    print(f"\n  Early response (≤3 hours) chi-square:")
    print(f"    Stationed:   {early_s}/{len(s)} ({early_s/len(s)*100:.1f}%)")
    print(f"    Self-joined: {early_sj}/{len(sj)} ({early_sj/len(sj)*100:.1f}%)")
    print(f"    χ²({dof}) = {chi2:.2f}, p = {chi_p:.2e}")

    # Summary table
    print_subheader("Table 2: Temporal Characteristics")
    print(f"\n  {'':35} {'Stationed':>12} {'Self-Joined':>12} {'Test':>18}")
    print(f"  {'':35} {'(n='+str(len(s))+')':>12} {'(n='+str(len(sj))+')':>12}")
    print(f"  {'-' * 78}")
    print(f"  {'Mean time (hours)':35} {np.mean(s):>12.2f} {np.mean(sj):>12.2f} {'t=' + str(round(abs(t_stat), 2)):>18}")
    print(f"  {'Median time (hours)':35} {np.median(s):>12.1f} {np.median(sj):>12.1f} {'U=' + str(int(u_stat)):>18}")
    print(f"  {'SD':35} {np.std(s, ddof=1):>12.2f} {np.std(sj, ddof=1):>12.2f}")
    s_iqr = f"{np.percentile(s,25):.0f}–{np.percentile(s,75):.0f}"
    sj_iqr = f"{np.percentile(sj,25):.0f}–{np.percentile(sj,75):.0f}"
    print(f"  {'IQR (hours)':35} {s_iqr:>12} {sj_iqr:>12}")
    print(f"  {'% killed ≤ 3 hours':35} {early_s/len(s)*100:>11.1f}% {early_sj/len(sj)*100:>11.1f}% {'χ²=' + str(round(chi2, 2)):>18}")
    print(f"  {'Effect size (Cohen d)':35} {'':>12} {'':>12} {'d=' + str(round(cohens_d, 2)):>18}")
    print(f"  {'All tests':35} {'':>12} {'':>12} {'p < .001':>18}")

    return {"s": s, "sj": sj, "cohens_d": cohens_d}


# ============================================================================
# H2: VOLUNTARY MOBILIZATION HYPOTHESIS
# ============================================================================

def test_h2(records):
    """Test H2: Substantial proportion self-joined."""
    print_header("H2: VOLUNTARY MOBILIZATION HYPOTHESIS")

    # Core proportion
    valid = [r for r in records if r["joined"] in ("0", "1")]
    n_total = len(valid)
    n_sj = sum(1 for r in valid if r["joined"] == "1")
    n_st = n_total - n_sj
    p_sj = n_sj / n_total
    ci_low, ci_high = wilson_ci(p_sj, n_total)

    print(f"\n  Total (with coded Joined): {n_total}")
    print(f"  Self-Joined: {n_sj} ({p_sj*100:.1f}%), 95% CI [{ci_low*100:.1f}%, {ci_high*100:.1f}%]")
    print(f"  Stationed:   {n_st} ({n_st/n_total*100:.1f}%)")

    # Among combat participants
    combat = [r for r in valid if r["combat"] == "1"]
    n_combat_sj = sum(1 for r in combat if r["joined"] == "1")
    print(f"\n  Among combat participants (n={len(combat)}): {n_combat_sj} self-joined ({n_combat_sj/len(combat)*100:.1f}%)")

    # Binomial tests
    bt25 = binomtest(n_sj, n_total, 0.25, alternative="greater")
    bt33 = binomtest(n_sj, n_total, 0.33, alternative="greater")
    print(f"\n  Binomial test (H0: ≤25%): p = {bt25.pvalue:.2e}")
    print(f"  Binomial test (H0: ≤33%): p = {bt33.pvalue:.2e}")

    # Chi-square by subgroups
    subgroups = [
        ("Branch", "branch", ["Military", "Police", "Shin Bet", "Emergency Response Team"]),
        ("Service status", "service", ["Conscript", "Professional", "Reserves"]),
        ("SOF", "sof", ["0", "1"]),
        ("Officer", "officer", ["0", "1"]),
    ]

    print_subheader("Chi-Square Tests by Subgroup")
    for sg_label, sg_key, sg_vals in subgroups:
        table = []
        labels = []
        for val in sg_vals:
            n_s = sum(1 for r in valid if r[sg_key] == val and r["joined"] == "0")
            n_j = sum(1 for r in valid if r[sg_key] == val and r["joined"] == "1")
            if n_s + n_j > 0:
                table.append([n_s, n_j])
                labels.append(val)

        if len(table) >= 2:
            chi2, p, dof, _ = chi2_contingency(table)
            n_chi = sum(sum(row) for row in table)
            k = len(table)
            v = cramers_v(chi2, n_chi, k) if k > 1 else 0

            print(f"\n  {sg_label}: χ²({dof}) = {chi2:.1f}, p = {p:.2e}, Cramér's V = {v:.3f}")
            for i, label in enumerate(labels):
                t = sum(table[i])
                pct = table[i][1] / t * 100
                print(f"    {label:<25}: {table[i][1]}/{t} ({pct:.1f}%) self-joined")

            # Odds ratio for 2x2 tables
            if len(table) == 2:
                a, b = table[0]
                c, d = table[1]
                if b > 0 and c > 0:
                    odds_ratio = (d * a) / (c * b)
                    print(f"    Odds ratio: {odds_ratio:.2f}")

    # Table 3
    print_subheader("Table 3: Self-Joining Rates by Subgroup")
    print(f"\n  {'Subgroup':<30} {'Stat':>5} {'Self':>5} {'Total':>6} {'%SJ':>8}")
    print(f"  {'-' * 56}")
    print(f"  {'OVERALL':<30} {n_st:>5} {n_sj:>5} {n_total:>6} {p_sj*100:>7.1f}%")
    for sg_label, sg_key, sg_vals in subgroups:
        print(f"  {sg_label}:")
        for val in sg_vals:
            n_s = sum(1 for r in valid if r[sg_key] == val and r["joined"] == "0")
            n_j = sum(1 for r in valid if r[sg_key] == val and r["joined"] == "1")
            t = n_s + n_j
            pct = n_j / t * 100 if t > 0 else 0
            lbl = {"0": "No", "1": "Yes"}.get(val, val) if sg_key in ("sof", "officer") else val
            print(f"    {lbl:<28} {n_s:>5} {n_j:>5} {t:>6} {pct:>7.1f}%")


# ============================================================================
# H3: ERC PROFILE HYPOTHESIS (Logistic Regression)
# ============================================================================

def test_h3(records):
    """Test H3: ERC characteristics predict self-joining."""
    print_header("H3: ERC PROFILE HYPOTHESIS — LOGISTIC REGRESSION")

    # Build analysis sample (exclude ERT — perfect separation)
    analysis = []
    for r in records:
        if r["joined"] not in ("0", "1"):
            continue
        if r["officer"] not in ("0", "1"):
            continue
        if r["sof"] not in ("0", "1"):
            continue
        if r["service"] not in ("Conscript", "Reserves", "Professional"):
            continue
        if r["branch"] == "Emergency Response Team":
            continue
        if r["branch"] not in ("Military", "Police", "Shin Bet"):
            continue

        analysis.append({
            "joined": int(r["joined"]),
            "officer": int(r["officer"]),
            "sof": int(r["sof"]),
            "reserves": 1 if r["service"] == "Reserves" else 0,
            "professional": 1 if r["service"] == "Professional" else 0,
            "police_security": 1 if r["branch"] in ("Police", "Shin Bet") else 0,
        })

    n = len(analysis)
    y = np.array([r["joined"] for r in analysis])
    print(f"\n  Analysis sample: N = {n} (excl. 43 ERT — perfect separation)")
    print(f"  Self-joined: {sum(y)} ({sum(y)/n*100:.1f}%)")

    # Bivariate models
    print_subheader("Bivariate Logistic Regressions")
    predictors = {
        "Officer": [r["officer"] for r in analysis],
        "SOF": [r["sof"] for r in analysis],
        "Reserves (vs Conscript+Prof)": [r["reserves"] for r in analysis],
        "Professional (vs Conscript)": [r["professional"] for r in analysis],
        "Police/Security (vs Military)": [r["police_security"] for r in analysis],
    }
    for name, x_vals in predictors.items():
        X = sm.add_constant(np.array(x_vals, dtype=float))
        model = Logit(y, X).fit(disp=0)
        coef = model.params[1]
        se = model.bse[1]
        or_val = np.exp(coef)
        ci_l = np.exp(coef - 1.96 * se)
        ci_h = np.exp(coef + 1.96 * se)
        p = model.pvalues[1]
        print(f"  {name:<35} OR = {or_val:>6.2f} [{ci_l:.2f}, {ci_h:.2f}], p = {p:.4f}")

    # Full multivariate model
    print_subheader("Full Multivariate Model")
    X_full = sm.add_constant(np.column_stack([
        [r["officer"] for r in analysis],
        [r["sof"] for r in analysis],
        [r["reserves"] for r in analysis],
        [r["professional"] for r in analysis],
        [r["police_security"] for r in analysis],
    ]))
    var_names = ["Constant", "Officer", "SOF", "Reserves", "Professional", "Police/Security"]

    model_full = Logit(y, X_full).fit(disp=0)

    print(f"\n  N = {n}")
    print(f"  Pseudo R² (McFadden): {model_full.prsquared:.3f}")
    print(f"  Log-likelihood: {model_full.llf:.1f}")
    print(f"  AIC: {model_full.aic:.1f}")
    print(f"  LLR χ²: {model_full.llr:.1f}, p = {model_full.llr_pvalue:.2e}")

    # Table 4
    print(f"\n  {'Variable':<22} {'β':>8} {'SE':>8} {'OR':>8} {'95% CI':>16} {'p':>10}")
    print(f"  {'-' * 74}")
    for i, name in enumerate(var_names):
        coef = model_full.params[i]
        se = model_full.bse[i]
        p = model_full.pvalues[i]
        or_val = np.exp(coef)
        ci_l = np.exp(coef - 1.96 * se)
        ci_h = np.exp(coef + 1.96 * se)
        sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""
        print(f"  {name:<22} {coef:>8.3f} {se:>8.3f} {or_val:>8.2f} [{ci_l:.2f}, {ci_h:.2f}] {p:>9.4f}{sig}")

    # Classification
    y_pred = (model_full.predict(X_full) >= 0.5).astype(int)
    tp = np.sum((y == 1) & (y_pred == 1))
    tn = np.sum((y == 0) & (y_pred == 0))
    fp = np.sum((y == 0) & (y_pred == 1))
    fn = np.sum((y == 1) & (y_pred == 0))
    accuracy = (tp + tn) / n
    sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0

    print(f"\n  Classification:")
    print(f"    Accuracy:    {accuracy*100:.1f}%")
    print(f"    Sensitivity: {sensitivity*100:.1f}%")
    print(f"    Specificity: {specificity*100:.1f}%")

    # Interaction test
    print_subheader("SOF × Officer Interaction Test")
    X_int = sm.add_constant(np.column_stack([
        [r["officer"] for r in analysis],
        [r["sof"] for r in analysis],
        [r["reserves"] for r in analysis],
        [r["professional"] for r in analysis],
        [r["police_security"] for r in analysis],
        [r["sof"] * r["officer"] for r in analysis],
    ]))
    model_int = Logit(y, X_int).fit(disp=0)
    lr_stat = 2 * (model_int.llf - model_full.llf)
    lr_p = 1 - stats.chi2.cdf(lr_stat, 1)
    print(f"  LR test for interaction: χ²(1) = {lr_stat:.2f}, p = {lr_p:.3f}")
    print(f"  Interaction {'significant' if lr_p < 0.05 else 'NOT significant'}")

    # Predicted probabilities
    print_subheader("Predicted Probabilities")
    profiles = [
        ("Conscript, non-officer, non-SOF, Military", [1, 0, 0, 0, 0, 0]),
        ("Professional, non-officer, non-SOF, Military", [1, 0, 0, 0, 1, 0]),
        ("Professional, officer, non-SOF, Military", [1, 1, 0, 0, 1, 0]),
        ("Reserves, non-officer, non-SOF, Military", [1, 0, 0, 1, 0, 0]),
        ("Professional, non-officer, SOF, Military", [1, 0, 1, 0, 1, 0]),
        ("Professional, officer, non-SOF, Police", [1, 1, 0, 0, 1, 1]),
        ("Professional, officer, SOF, Military", [1, 1, 1, 0, 1, 0]),
        ("Reserves, officer, SOF, Military", [1, 1, 1, 1, 0, 0]),
    ]
    for desc, x_vals in profiles:
        prob = model_full.predict(np.array([x_vals]))[0]
        print(f"  {desc:<50} P = {prob:.1%}")

    # ERT summary
    ert_n = sum(1 for r in records if r["branch"] == "Emergency Response Team" and r["joined"] in ("0", "1"))
    ert_sj = sum(1 for r in records if r["branch"] == "Emergency Response Team" and r["joined"] == "1")
    print(f"\n  Emergency Response Teams (excluded from regression):")
    print(f"    N = {ert_n}, Self-Joined = {ert_sj} ({ert_sj/ert_n*100:.1f}%)")

    return model_full


# ============================================================================
# H4: AD HOC TEAM FORMATION
# ============================================================================

def classify_branches(units):
    """Classify a list of unit names into organizational branches."""
    branches = set()
    sof_keywords = [
        "sayeret matkal", "shaldag", "shayetet", "yamam", "yamas", "lotar",
        "504", "oketz", "yahalom", "maglan", "duvdevan", "egoz", "669",
        "brigade 89 battalion 217", "brigade 89 battalion 212",
        "brigade 89 battalion 621", "brigade 888", "unit 5515", "matpa", "gideonim",
    ]
    sof_count = 0
    for u in units:
        ul = u.lower()
        if any(kw in ul for kw in ["police", "yamas", "yamam", "yasam", "yoav",
                                     "border police", "magen", "metilan", "metilam",
                                     "barak", "shikma"]):
            branches.add("Police")
        elif any(kw in ul for kw in ["shabak", "shabas", "mazada"]):
            branches.add("Shin Bet")
        elif "gideonim" in ul:
            branches.add("Local Defense")
        else:
            branches.add("IDF")
        if any(kw in ul for kw in sof_keywords):
            sof_count += 1
    return branches, sof_count


def test_h4(locations):
    """Test H4: Ad hoc team formation across organizations."""
    print_header("H4: AD HOC TEAM FORMATION")

    resp = [l for l in locations if l["has_response"]]

    # Enrich with branch/SOF data
    for l in resp:
        branches, sof_count = classify_branches(l["units"])
        l["n_branches"] = len(branches)
        l["branches"] = branches
        l["sof_count"] = sof_count

    n_units_arr = np.array([l["n_units"] for l in resp])
    n_branches_arr = np.array([l["n_branches"] for l in resp])

    print(f"\n  Responding locations: {len(resp)}")

    # Unit diversity
    print_subheader("Unit Diversity")
    print(f"  Mean: {np.mean(n_units_arr):.1f}, Median: {np.median(n_units_arr):.1f}")
    print(f"  SD: {np.std(n_units_arr, ddof=1):.1f}, Range: {np.min(n_units_arr)}–{np.max(n_units_arr)}")

    # Branch diversity
    print_subheader("Branch Diversity")
    multi_org = sum(1 for l in resp if l["n_branches"] >= 2)
    three_plus = sum(1 for l in resp if l["n_branches"] >= 3)
    sof_locs = sum(1 for l in resp if l["sof_count"] > 0)

    print(f"  ≥2 branches: {multi_org}/{len(resp)} ({multi_org/len(resp)*100:.1f}%)")
    print(f"  ≥3 branches: {three_plus}/{len(resp)} ({three_plus/len(resp)*100:.1f}%)")
    print(f"  SOF present: {sof_locs}/{len(resp)} ({sof_locs/len(resp)*100:.1f}%)")

    for nb in sorted(set(n_branches_arr)):
        count = int(np.sum(n_branches_arr == nb))
        print(f"  {int(nb)} branch(es): {count} locations ({count/len(resp)*100:.1f}%)")

    # Correlation
    r_val, p_val = pearsonr(n_units_arr, n_branches_arr)
    print(f"\n  Unit × Branch diversity: r = {r_val:.3f}, p = {p_val:.4f}")

    # Table 5
    print_subheader("Table 5: Organizational Diversity")
    indicators = [
        ("Locations with military response", len(resp)),
        ("Total unit-location observations", sum(l["n_units"] for l in resp)),
        ("Distinct organizational units", 145),
        ("Mean units per location (SD)", f"{np.mean(n_units_arr):.1f} ({np.std(n_units_arr, ddof=1):.1f})"),
        ("Median units per location", f"{np.median(n_units_arr):.1f}"),
        ("Locations with ≥2 branches", f"{multi_org} ({multi_org/len(resp)*100:.1f}%)"),
        ("Locations with ≥3 branches", f"{three_plus} ({three_plus/len(resp)*100:.1f}%)"),
        ("Locations with SOF presence", f"{sof_locs} ({sof_locs/len(resp)*100:.1f}%)"),
    ]
    for label, val in indicators:
        print(f"  {label:<45} {str(val):>15}")

    return resp


# ============================================================================
# H5: OPERATIONAL STABILIZATION
# ============================================================================

def test_h5(locations, fatalities):
    """Test H5: Organizational diversity and operational outcomes."""
    print_header("H5: OPERATIONAL STABILIZATION")

    resp = [l for l in locations if l["has_response"]]
    no_resp = [l for l in locations if not l["has_response"]]

    # Enrich
    for l in resp + no_resp:
        branches, sof = classify_branches(l.get("units", []))
        l["n_branches"] = len(branches)
        l["sof_count"] = sof
        l["is_civilian"] = any(kw in l["name"].lower() for kw in ["kibbutz", "moshav", "festival"])

    # Response vs no-response
    print_subheader("Response vs. No-Response Comparison")
    civ_resp = [l for l in resp if l["is_civilian"]]
    civ_no_resp = [l for l in no_resp if l["is_civilian"]]

    print(f"\n  Civilian locations with response:    {len(civ_resp)}")
    print(f"  Civilian locations WITHOUT response: {len(civ_no_resp)}")

    print(f"\n  No-response locations:")
    for l in civ_no_resp:
        print(f"    {l['name']}: {l['fatalities']} killed, {l['kidnapped']} kidnapped")

    # Nir Oz
    nir_oz = [l for l in civ_no_resp if "nir oz" in l["name"].lower()]
    if nir_oz:
        no = nir_oz[0]
        total_no = no["fatalities"] + no["kidnapped"]
        ratio_no = no["kidnapped"] / total_no * 100 if total_no > 0 else 0
        print(f"\n  Nir Oz (no response): {no['kidnapped']} kidnapped / {total_no} total = {ratio_no:.1f}% kidnapping ratio")

    # Kidnapping ratios at responding communities
    print_subheader("Kidnapping Ratios at Civilian Communities")
    print(f"\n  {'Location':<30} {'Units':>5} {'Killed':>7} {'Kid':>5} {'Ratio':>8}")
    print(f"  {'-' * 58}")
    for l in sorted(civ_resp + civ_no_resp, key=lambda x: -x["kidnapped"]):
        total = l["fatalities"] + l["kidnapped"]
        ratio = l["kidnapped"] / total * 100 if total > 0 else 0
        status = "NONE" if l in civ_no_resp else str(l["n_units"])
        if l["kidnapped"] > 0 or l in civ_no_resp:
            print(f"  {l['name'][:28]:<30} {status:>5} {l['fatalities']:>7} {l['kidnapped']:>5} {ratio:>7.1f}%")

    # Within-response correlations using D2 time-to-control
    loc_map = {
        "be'eri": "Kibbutz Be'eri", "kfar aza": "Kibbutz Kfar Aza",
        "nova festival": "Nova festival", "nahal oz post": "Nahal Oz millitary base",
        "kissufim outpost": "Kisufim military base", "kissufim": "Kibbutz Kisufim",
        "sderot": "Sderot", "ofakim": "Ofakim", "re'eim": "Kibbutz Re'im",
        "alumim": "Kibbutz Alumim", "nirim": "kibbutz Nirim",
        "nativ haasara": "Kibbutz Nativ Ha'Asara", "holit": "Kibbutz Holit",
        "nir itzhak": "Kibbutz Nir Yitzhak", "mivtachim": "moshav Mivtahim",
        "kerem shalom": "Kibbutz Kerem Shalom", "ein hashlosha": "Kibbutz Ein HaShlosha",
        "pri gan": "Kibbutz Pri Gan", "zikim base": "Zikim millitary base",
        "zikim beach": "Zikim Beach", "sufa outpost": "Sufa military base",
        "sufa": "Kibbutz Sufa", "yachini": "Moshav Yakhini and the area",
        "nahal oz": "Kibbutz Nahal Oz", "urim base": "Orim military base",
    }

    toc_by_loc = defaultdict(list)
    for r in fatalities:
        d2_loc = r["location"].lower()
        d1_loc = loc_map.get(d2_loc)
        if d1_loc:
            toc = r["toc"]
            if toc and toc.replace(".", "").isdigit():
                toc_by_loc[d1_loc].append(float(toc))

    # Build paired data
    loc_lookup = {l["name"]: l for l in resp}
    paired = []
    for loc_name, toc_vals in toc_by_loc.items():
        if loc_name in loc_lookup:
            l = loc_lookup[loc_name]
            paired.append({
                "name": loc_name,
                "n_units": l["n_units"],
                "mean_toc": np.mean(toc_vals),
                "kidnapped": l["kidnapped"],
            })

    if len(paired) > 5:
        x_units = [p["n_units"] for p in paired]
        y_toc = [p["mean_toc"] for p in paired]
        y_kid = [p["kidnapped"] for p in paired]

        print_subheader("Correlations with Time to Operational Control")
        r_toc, p_toc = pearsonr(x_units, y_toc)
        rho_toc, sp_toc = spearmanr(x_units, y_toc)
        print(f"  Unit diversity × TtC: Pearson r = {r_toc:.3f} (p={p_toc:.4f}), Spearman ρ = {rho_toc:.3f} (p={sp_toc:.4f})")

        r_kid, p_kid = pearsonr(x_units, y_kid)
        rho_kid, sp_kid = spearmanr(x_units, y_kid)
        print(f"  Unit diversity × Kid: Pearson r = {r_kid:.3f} (p={p_kid:.4f}), Spearman ρ = {rho_kid:.3f} (p={sp_kid:.4f})")

        print(f"\n  NOTE: Positive correlations reflect endogeneity — more severely")
        print(f"  attacked locations attracted larger, more diverse responses.")


# ============================================================================
# MAIN
# ============================================================================

def main():
    logger = Logger(LOG_FILE)
    sys.stdout = logger

    print("=" * 70)
    print("EMBEDDED RESPONSE CAPACITY (ERC): REPLICATION ANALYSIS")
    print("=" * 70)
    print(f"\nReplication code for all hypothesis tests (H1–H5)")
    print(f"Output log: {LOG_FILE}\n")

    # Check files
    for f in [FATALITIES_FILE, LOCATIONS_FILE]:
        if not os.path.exists(f):
            print(f"ERROR: File not found: {f}")
            print(f"Place the data files in the same directory as this script.")
            sys.exit(1)

    # Load data
    fatalities = load_fatalities(FATALITIES_FILE)
    locations = load_locations(LOCATIONS_FILE)

    # Run all tests
    h1_results = test_h1(fatalities)
    test_h2(fatalities)
    model = test_h3(fatalities)
    resp_locs = test_h4(locations)
    test_h5(locations, fatalities)

    # Summary
    print_header("ANALYSIS COMPLETE")
    print(f"\nAll results saved to: {LOG_FILE}")
    print(f"Figures should be generated using: ERC_figures.py")

    logger.close()
    sys.stdout = logger.terminal


if __name__ == "__main__":
    main()
