"""
Embedded Response Capacity (ERC): Figure Generation
====================================================
Generates all publication-ready figures for the manuscript.

Requirements:
    pip install numpy matplotlib scipy

Input files (relative to repository root):
    1. data/fatalities.csv
    2. data/locations_units.csv

Usage (from repository root):
    python scripts/ERC_figures.py

Output:
    figures/ directory containing PDF and PNG versions of all figures.
"""

import csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from collections import defaultdict
import os

# ============================================================================
# CONFIG
# ============================================================================

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FATALITIES_FILE = os.path.join(_REPO_ROOT, "data", "fatalities.csv")
LOCATIONS_FILE = os.path.join(_REPO_ROOT, "data", "locations_units.csv")
FIG_DIR = os.path.join(_REPO_ROOT, "figures")
os.makedirs(FIG_DIR, exist_ok=True)

DPI = 300
COLOR_STATIONED = "#2C5F8A"
COLOR_SELFJOINED = "#C44E52"
COLOR_GRAY = "#888888"


def save_fig(fig, name):
    fig.savefig(os.path.join(FIG_DIR, f"{name}.pdf"), bbox_inches="tight")
    fig.savefig(os.path.join(FIG_DIR, f"{name}.png"), dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {name}.pdf / .png")


# ============================================================================
# DATA LOADING (shared with ERC_analysis.py)
# ============================================================================

def load_fatalities(filepath):
    with open(filepath, "r", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def load_locations(filepath):
    with open(filepath, "r", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def get_time_arrays(records):
    """Extract time arrays for stationed and self-joined."""
    s, sj = [], []
    for r in records:
        j = r.get("Joined", "").strip()
        t = r.get("Time", "").strip()
        if j not in ("0", "1") or not t or not t.replace(".", "").isdigit():
            continue
        t_val = float(t)
        if j == "0":
            s.append(t_val)
        else:
            sj.append(t_val)
    return np.array(s), np.array(sj)


# ============================================================================
# FIGURE 2: Temporal Distribution (H1)
# ============================================================================

def fig_temporal_distribution(records):
    s, sj = get_time_arrays(records)
    fig, ax = plt.subplots(figsize=(10, 5.5))

    bins = np.arange(0.5, 19.5, 1)
    ax.hist(s, bins=bins, alpha=0.65, label=f"Stationed (n={len(s)})",
            color=COLOR_STATIONED, edgecolor="white", linewidth=0.5)
    ax.hist(sj, bins=bins, alpha=0.65, label=f"Self-Joined (n={len(sj)})",
            color=COLOR_SELFJOINED, edgecolor="white", linewidth=0.5)

    ax.axvline(np.mean(s), color=COLOR_STATIONED, linestyle="--", linewidth=1.5,
               label=f"Stationed mean ({np.mean(s):.1f}h)")
    ax.axvline(np.mean(sj), color=COLOR_SELFJOINED, linestyle="--", linewidth=1.5,
               label=f"Self-Joined mean ({np.mean(sj):.1f}h)")

    ax.set_xlabel("Hours After Attack Onset", fontsize=12)
    ax.set_ylabel("Number of Fatalities", fontsize=12)
    ax.set_title("Figure 2. Temporal Distribution of Fatalities by Mode of Joining",
                 fontsize=13, fontweight="bold")
    ax.legend(fontsize=10, loc="upper right")
    ax.set_xlim(0.5, 18.5)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    save_fig(fig, "Fig2_Temporal_Distribution")


# ============================================================================
# FIGURE 3: Cumulative Distribution (H1)
# ============================================================================

def fig_cumulative_distribution(records):
    s, sj = get_time_arrays(records)
    fig, ax = plt.subplots(figsize=(10, 5.5))

    hours = np.arange(1, 19)
    s_cum = [np.sum(s <= h) / len(s) * 100 for h in hours]
    sj_cum = [np.sum(sj <= h) / len(sj) * 100 for h in hours]

    ax.step(hours, s_cum, where="mid", color=COLOR_STATIONED, linewidth=2,
            label=f"Stationed (n={len(s)})")
    ax.step(hours, sj_cum, where="mid", color=COLOR_SELFJOINED, linewidth=2,
            label=f"Self-Joined (n={len(sj)})")
    ax.fill_between(hours, s_cum, sj_cum, alpha=0.15, color="gray", step="mid")
    ax.axhline(50, color="gray", linestyle=":", linewidth=1, alpha=0.5)
    ax.text(16.5, 52, "50%", fontsize=9, color="gray")

    ax.set_xlabel("Hours After Attack Onset", fontsize=12)
    ax.set_ylabel("Cumulative Percentage of Fatalities", fontsize=12)
    ax.set_title("Figure 3. Cumulative Distribution of Fatalities by Mode of Joining",
                 fontsize=13, fontweight="bold")
    ax.legend(fontsize=10, loc="lower right")
    ax.set_xlim(1, 18)
    ax.set_ylim(0, 105)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    save_fig(fig, "Fig3_Cumulative_Distribution")


# ============================================================================
# FIGURE 4: Composition Stacked Bar (H2)
# ============================================================================

def fig_composition(records):
    valid = [r for r in records if r.get("Joined", "").strip() in ("0", "1")]
    combat = [r for r in valid if r.get("Combat", "").strip() == "1"]

    n_st_all = sum(1 for r in valid if r["Joined"].strip() == "0")
    n_sj_all = sum(1 for r in valid if r["Joined"].strip() == "1")
    n_st_combat = sum(1 for r in combat if r["Joined"].strip() == "0")
    n_sj_combat = sum(1 for r in combat if r["Joined"].strip() == "1")

    fig, ax = plt.subplots(figsize=(8, 5))
    labels = [f"All Fatalities\n(N={n_st_all+n_sj_all})",
              f"Combat\nParticipants\n(N={n_st_combat+n_sj_combat})"]
    stationed = [n_st_all, n_st_combat]
    selfjoined = [n_sj_all, n_sj_combat]
    x = np.arange(len(labels))
    width = 0.5

    ax.bar(x, stationed, width, label="Stationed", color=COLOR_STATIONED, alpha=0.75)
    ax.bar(x, selfjoined, width, bottom=stationed, label="Self-Joined",
           color=COLOR_SELFJOINED, alpha=0.75)

    for i in range(len(labels)):
        total = stationed[i] + selfjoined[i]
        ax.text(i, stationed[i] / 2,
                f"{stationed[i]}\n({stationed[i]/total*100:.1f}%)",
                ha="center", va="center", fontsize=10, color="white", fontweight="bold")
        ax.text(i, stationed[i] + selfjoined[i] / 2,
                f"{selfjoined[i]}\n({selfjoined[i]/total*100:.1f}%)",
                ha="center", va="center", fontsize=10, color="white", fontweight="bold")

    ax.set_ylabel("Number of Personnel", fontsize=12)
    ax.set_title("Figure 4. Composition of Responding Forces by Mode of Joining",
                 fontsize=13, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=11)
    ax.legend(loc="upper right", fontsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    save_fig(fig, "Fig4_Composition")


# ============================================================================
# FIGURE 5: Self-Joining Rates by Subgroup (H2)
# ============================================================================

def fig_subgroup_rates(records):
    valid = [r for r in records if r.get("Joined", "").strip() in ("0", "1")]

    categories = [
        ("Branch", [
            ("Military", sum(1 for r in valid if r.get("Branch ","").strip()=="Military" and r["Joined"].strip()=="1") /
                         max(1, sum(1 for r in valid if r.get("Branch ","").strip()=="Military")) * 100),
            ("Police", sum(1 for r in valid if r.get("Branch ","").strip()=="Police" and r["Joined"].strip()=="1") /
                       max(1, sum(1 for r in valid if r.get("Branch ","").strip()=="Police")) * 100),
            ("Shin Bet", sum(1 for r in valid if r.get("Branch ","").strip()=="Shin Bet" and r["Joined"].strip()=="1") /
                         max(1, sum(1 for r in valid if r.get("Branch ","").strip()=="Shin Bet")) * 100),
            ("Emergency\nResponse", 100.0),
        ]),
        ("Service Status", [
            ("Conscript", sum(1 for r in valid if r.get("Conscript/Reserves/ Professional","").strip()=="Conscript" and r["Joined"].strip()=="1") /
                          max(1, sum(1 for r in valid if r.get("Conscript/Reserves/ Professional","").strip()=="Conscript")) * 100),
            ("Professional", sum(1 for r in valid if r.get("Conscript/Reserves/ Professional","").strip()=="Professional" and r["Joined"].strip()=="1") /
                             max(1, sum(1 for r in valid if r.get("Conscript/Reserves/ Professional","").strip()=="Professional")) * 100),
            ("Reserves", sum(1 for r in valid if r.get("Conscript/Reserves/ Professional","").strip()=="Reserves" and r["Joined"].strip()=="1") /
                         max(1, sum(1 for r in valid if r.get("Conscript/Reserves/ Professional","").strip()=="Reserves")) * 100),
        ]),
        ("SOF Status", [
            ("Non-SOF", sum(1 for r in valid if r.get("SOF","").strip()=="0" and r["Joined"].strip()=="1") /
                        max(1, sum(1 for r in valid if r.get("SOF","").strip()=="0")) * 100),
            ("SOF", sum(1 for r in valid if r.get("SOF","").strip()=="1" and r["Joined"].strip()=="1") /
                   max(1, sum(1 for r in valid if r.get("SOF","").strip()=="1")) * 100),
        ]),
        ("Officer Status", [
            ("Non-Officer", sum(1 for r in valid if r.get("Officer","").strip()=="0" and r["Joined"].strip()=="1") /
                            max(1, sum(1 for r in valid if r.get("Officer","").strip()=="0")) * 100),
            ("Officer", sum(1 for r in valid if r.get("Officer","").strip()=="1" and r["Joined"].strip()=="1") /
                        max(1, sum(1 for r in valid if r.get("Officer","").strip()=="1")) * 100),
        ]),
    ]

    fig, axes = plt.subplots(1, 4, figsize=(16, 5.5), sharey=True)
    for idx, (title, data) in enumerate(categories):
        ax = axes[idx]
        labels = [d[0] for d in data]
        vals = [d[1] for d in data]
        colors = [COLOR_SELFJOINED if v > 50 else COLOR_STATIONED for v in vals]
        ax.barh(range(len(labels)), vals, color=colors, alpha=0.75, height=0.6)
        ax.set_yticks(range(len(labels)))
        ax.set_yticklabels(labels, fontsize=10)
        ax.set_xlim(0, 110)
        ax.set_xlabel("% Self-Joined", fontsize=10)
        ax.set_title(title, fontsize=11, fontweight="bold")
        ax.axvline(40.8, color="gray", linestyle=":", linewidth=1, alpha=0.7)
        for i, v in enumerate(vals):
            ax.text(v + 2, i, f"{v:.1f}%", va="center", fontsize=9)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.invert_yaxis()

    plt.suptitle("Figure 5. Self-Joining Rates Across Subgroups",
                 fontsize=13, fontweight="bold", y=1.02)
    plt.tight_layout()
    save_fig(fig, "Fig5_SelfJoining_Subgroups")


# ============================================================================
# FIGURE 6: Predicted Probabilities (H3)
# ============================================================================

def fig_predicted_probabilities():
    profiles = [
        "Conscript\nnon-SOF\nnon-officer\nMilitary",
        "Professional\nnon-SOF\nnon-officer\nMilitary",
        "Professional\nnon-SOF\nofficer\nMilitary",
        "Reserves\nnon-SOF\nnon-officer\nMilitary",
        "Professional\nnon-SOF\nSOF\nMilitary",
        "Professional\nofficer\nnon-SOF\nPolice",
        "Professional\nofficer\nSOF\nMilitary",
        "Reserves\nofficer\nSOF\nMilitary",
    ]
    probs = [7.1, 12.3, 30.4, 50.7, 66.4, 75.4, 86.0, 97.8]

    fig, ax = plt.subplots(figsize=(12, 6))
    colors = [COLOR_STATIONED if p < 50 else COLOR_SELFJOINED for p in probs]
    ax.barh(range(len(profiles)), probs, color=colors, alpha=0.75, height=0.65,
            edgecolor="white")
    ax.set_yticks(range(len(profiles)))
    ax.set_yticklabels(profiles, fontsize=9)
    ax.set_xlabel("Predicted Probability of Self-Joining (%)", fontsize=11)
    ax.set_title("Figure 6. Predicted Probability of Self-Joining by Personnel Profile\n"
                 "(Logistic Regression Model)", fontsize=12, fontweight="bold")
    ax.set_xlim(0, 110)
    ax.axvline(50, color="gray", linestyle=":", linewidth=1, alpha=0.5)
    for i, v in enumerate(probs):
        ax.text(v + 1.5, i, f"{v:.1f}%", va="center", fontsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.invert_yaxis()
    plt.tight_layout()
    save_fig(fig, "Fig6_Predicted_Probabilities")


# ============================================================================
# FIGURE 7: Forest Plot (H3)
# ============================================================================

def fig_forest_plot():
    var_names = ["Officer", "SOF", "Reserves\n(vs Conscript)",
                 "Professional\n(vs Conscript)", "Police/Security\n(vs Military)"]
    ors = [3.11, 14.06, 13.48, 1.84, 7.04]
    ci_lows = [1.20, 5.79, 3.25, 0.59, 2.49]
    ci_highs = [8.03, 34.14, 55.86, 5.75, 19.92]
    pvals = [0.0192, 0.0000, 0.0003, 0.2948, 0.0002]

    fig, ax = plt.subplots(figsize=(9, 5))
    colors_f = [COLOR_SELFJOINED if p < 0.05 else COLOR_GRAY for p in pvals]

    for i in range(len(var_names)):
        ax.plot([ci_lows[i], ci_highs[i]], [i, i], color=colors_f[i], linewidth=2)
        ax.plot(ors[i], i, "o", color=colors_f[i], markersize=8)
        sig = "***" if pvals[i] < 0.001 else "**" if pvals[i] < 0.01 else "*" if pvals[i] < 0.05 else "n.s."
        ax.text(max(ci_highs[i], ors[i]) + 1, i, f"OR={ors[i]:.2f} {sig}",
                va="center", fontsize=9)

    ax.axvline(1, color="gray", linestyle="--", linewidth=1)
    ax.set_yticks(range(len(var_names)))
    ax.set_yticklabels(var_names, fontsize=10)
    ax.set_xlabel("Odds Ratio (log scale)", fontsize=11)
    ax.set_xscale("log")
    ax.set_xlim(0.3, 80)
    ax.set_title("Figure 7. Logistic Regression: Predictors of Self-Joining\n"
                 "(Odds Ratios with 95% Confidence Intervals)",
                 fontsize=12, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.invert_yaxis()
    plt.tight_layout()
    save_fig(fig, "Fig7_Forest_Plot")


# ============================================================================
# FIGURE 8: Organizational Diversity (H4)
# ============================================================================

def fig_diversity(loc_rows):
    resp = []
    for r in loc_rows:
        units = []
        for col in ["Units"] + [f"Units {i}" for i in range(2, 36)]:
            if col in r and r[col] and r[col].strip() and r[col].strip() != "No military response":
                units.append(r[col].strip())
        if len(units) > 0:
            # Count branches
            branches = set()
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
            resp.append({"n_units": len(units), "n_branches": len(branches)})

    n_units = [l["n_units"] for l in resp]
    n_branches = [l["n_branches"] for l in resp]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))

    ax1.hist(n_units, bins=range(1, 38, 2), color=COLOR_STATIONED, alpha=0.75, edgecolor="white")
    ax1.axvline(np.mean(n_units), color=COLOR_SELFJOINED, linestyle="--", linewidth=1.5,
                label=f"Mean = {np.mean(n_units):.1f}")
    ax1.axvline(np.median(n_units), color=COLOR_STATIONED, linestyle=":", linewidth=1.5,
                label=f"Median = {np.median(n_units):.1f}")
    ax1.set_xlabel("Number of Distinct Units", fontsize=11)
    ax1.set_ylabel("Number of Locations", fontsize=11)
    ax1.set_title("A. Unit Diversity per Location", fontsize=12, fontweight="bold")
    ax1.legend(fontsize=9)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)

    branch_counts = [sum(1 for l in resp if l["n_branches"] == b) for b in [1, 2, 3, 4]]
    ax2.bar([1, 2, 3, 4], branch_counts,
            color=[COLOR_STATIONED, "#5B8DB8", COLOR_SELFJOINED, "#E07B7E"],
            alpha=0.75, edgecolor="white")
    ax2.set_xlabel("Number of Organizational Branches", fontsize=11)
    ax2.set_ylabel("Number of Locations", fontsize=11)
    ax2.set_title("B. Branch Diversity per Location", fontsize=12, fontweight="bold")
    ax2.set_xticks([1, 2, 3, 4])
    ax2.set_xticklabels(["1\n(IDF only)", "2\n(e.g., IDF+Police)",
                          "3\n(e.g., IDF+Police\n+Shin Bet)", "4\n(All branches)"])
    for i, v in enumerate(branch_counts):
        ax2.text(i + 1, v + 0.3, str(v), ha="center", fontsize=11, fontweight="bold")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)

    plt.suptitle("Figure 8. Organizational Diversity Across Combat Locations (N = 32)",
                 fontsize=13, fontweight="bold", y=1.02)
    plt.tight_layout()
    save_fig(fig, "Fig8_Diversity")


# ============================================================================
# FIGURE 9: Response and Kidnapping (H5)
# ============================================================================

def fig_response_kidnapping(loc_rows):
    locs = []
    for r in loc_rows:
        loc = r["Location"].strip()
        units = [r[col].strip() for col in ["Units"] + [f"Units {i}" for i in range(2, 36)]
                 if col in r and r[col] and r[col].strip() and r[col].strip() != "No military response"]
        try:
            kid = int(r.get("Kidnapped", "0").strip() or "0")
        except ValueError:
            kid = 0
        is_civ = any(kw in loc.lower() for kw in ["kibbutz", "moshav"])
        if is_civ:
            locs.append({"name": loc, "n_units": len(units), "kidnapped": kid})

    locs.sort(key=lambda x: -x["n_units"])

    fig, ax = plt.subplots(figsize=(10, 6))
    names = [l["name"].replace("Kibbutz ", "").replace("kibbutz ", "")
             .replace("Moshav ", "").replace("moshav ", "")[:18] for l in locs]
    units_vals = [l["n_units"] for l in locs]
    kid_vals = [l["kidnapped"] for l in locs]

    x = np.arange(len(locs))
    width = 0.35
    ax.bar(x - width / 2, units_vals, width, label="Responding Units",
           color=COLOR_STATIONED, alpha=0.75)
    ax.bar(x + width / 2, kid_vals, width, label="Kidnapped",
           color=COLOR_SELFJOINED, alpha=0.75)

    for i, l in enumerate(locs):
        if "nir oz" in l["name"].lower() and l["n_units"] == 0:
            ax.annotate("No military\nresponse", xy=(i, kid_vals[i]),
                        xytext=(i + 2, kid_vals[i] + 5), fontsize=9,
                        color=COLOR_SELFJOINED, fontweight="bold",
                        arrowprops=dict(arrowstyle="->", color=COLOR_SELFJOINED))

    ax.set_ylabel("Count", fontsize=11)
    ax.set_title("Figure 9. Responding Units and Kidnappings at Civilian Communities",
                 fontsize=12, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(names, rotation=45, ha="right", fontsize=8)
    ax.legend(fontsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    save_fig(fig, "Fig9_Response_Kidnapping")


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("Generating figures for ERC manuscript...")

    fat_records = load_fatalities(FATALITIES_FILE)
    loc_rows = load_locations(LOCATIONS_FILE)

    fig_temporal_distribution(fat_records)
    fig_cumulative_distribution(fat_records)
    fig_composition(fat_records)
    fig_subgroup_rates(fat_records)
    fig_predicted_probabilities()
    fig_forest_plot()
    fig_diversity(loc_rows)
    fig_response_kidnapping(loc_rows)

    print(f"\nAll figures saved to: {FIG_DIR}/")


if __name__ == "__main__":
    main()
