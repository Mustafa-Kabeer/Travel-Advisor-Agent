# =============================================
# Travel Plotting - Visualization Module
# =============================================
# This file contains all plotting and visualization functions for the travel advisor system

import matplotlib.pyplot as plt

# Import static data needed for plotting
from travel_info import DESTINATIONS, RULE_CATEGORY


# ===========================
# Helper Functions for Plotting Data
# ===========================

def compute_rule_frequency(state):
    """
    Count how many times each rule fired during inference.
    Returns a dict: rule_name -> count
    """
    counts = {}
    for entry in state["trace"]:
        # Each trace line starts with something like: "R4_culture_history: ..."
        parts = entry.split(":", 1)
        if len(parts) > 0:
            rule = parts[0].strip()
            if rule != "":
                counts[rule] = counts.get(rule, 0) + 1
    return counts


def compute_category_contributions(state):
    """
    Group rule firings by category and count total contributions.
    Returns a dict: category -> count
    """
    rule_freq = compute_rule_frequency(state)
    cat_counts = {}
    for rule, count in rule_freq.items():
        category = RULE_CATEGORY.get(rule, "Other")
        cat_counts[category] = cat_counts.get(category, 0) + count
    return cat_counts


def compute_dest_category_matrices(state):
    """
    Build matrices counting how many positive / negative rules
    fired per (destination, category).

    Returns:
      categories   -> list of category names
      pos_matrix   -> dict: dest -> dict: category -> count
      neg_matrix   -> dict: dest -> dict: category -> count
    """
    # Collect all categories used in RULE_CATEGORY
    categories = []
    for rule_name in RULE_CATEGORY:
        cat = RULE_CATEGORY[rule_name]
        if cat not in categories:
            categories.append(cat)

    # Initialize matrices
    pos_matrix = {}
    neg_matrix = {}
    for d in DESTINATIONS:
        pos_matrix[d] = {}
        neg_matrix[d] = {}
        for c in categories:
            pos_matrix[d][c] = 0
            neg_matrix[d][c] = 0

    # Count positive rules per category per destination
    for d in DESTINATIONS:
        for rule_name in state["recommended"][d]:
            cat = RULE_CATEGORY.get(rule_name, "Other")
            if cat not in pos_matrix[d]:
                pos_matrix[d][cat] = 0
            pos_matrix[d][cat] = pos_matrix[d][cat] + 1

    # Count negative rules per category per destination
    for d in DESTINATIONS:
        for rule_name in state["not_recommended"][d]:
            cat = RULE_CATEGORY.get(rule_name, "Other")
            if cat not in neg_matrix[d]:
                neg_matrix[d][cat] = 0
            neg_matrix[d][cat] = neg_matrix[d][cat] + 1

    return categories, pos_matrix, neg_matrix


# ===========================
# Main Visualization Functions
# ===========================

def visualize_statistics(state, scores):
    """
    Create a 2x2 grid of statistical visualizations:
    1. Destination scores (bar chart)
    2. Positive vs negative evidence (grouped bar chart)
    3. Rule firing frequency (line chart)
    4. Category contributions (pie chart)
    """
    destinations = DESTINATIONS

    # -----------------------------
    # 1) Destination Scores
    # -----------------------------
    score_values = []
    for d in destinations:
        score_values.append(scores[d])

    # -----------------------------
    # 2) Positive / Negative Evidence
    # -----------------------------
    pos_counts = []
    neg_counts = []
    for d in destinations:
        pos_counts.append(len(state["recommended"][d]))
        neg_counts.append(len(state["not_recommended"][d]))

    # -----------------------------
    # 3) Rule Firing Frequency
    # -----------------------------
    rule_freq = compute_rule_frequency(state)
    rules = sorted(rule_freq.keys())
    rule_values = []
    for r in rules:
        rule_values.append(rule_freq[r])

    # -----------------------------
    # 4) Category Contributions
    # -----------------------------
    cat_counts = compute_category_contributions(state)
    categories = list(cat_counts.keys())
    cat_values = []
    for c in categories:
        cat_values.append(cat_counts[c])

    # -----------------------------
    # Create 2x2 Subplot Figure
    # -----------------------------
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Systems Statistical Visualization")

    # ---- Subplot 1: Destination Scores ----
    ax = axs[0][0]
    ax.bar(destinations, score_values)
    ax.set_title("Destination Scores")
    ax.set_ylabel("Score")
    ax.set_xlabel("Destination")

    # ---- Subplot 2: Positive vs Negative Evidence ----
    ax = axs[0][1]
    x_positions = range(len(destinations))
    width = 0.35

    left_positions = []
    right_positions = []

    for i in x_positions:
        left_positions.append(i - width / 2.0)
        right_positions.append(i + width / 2.0)

    ax.bar(left_positions, pos_counts, width, label="Positive")
    ax.bar(right_positions, neg_counts, width, label="Negative")

    ax.set_xticks(list(x_positions))
    ax.set_xticklabels(destinations, rotation=15)
    ax.set_title("Positive vs Negative Evidence")
    ax.set_ylabel("Rule Count")
    ax.set_xlabel("Destination")
    ax.legend()

    # ---- Subplot 3: Rule Firing Frequency (line + dots) ----
    ax = axs[1][0]
    ax.plot(rules, rule_values, marker='o', linestyle='-', linewidth=2)
    ax.set_title("Rule Firing Frequency")
    ax.set_ylabel("Count")
    ax.set_xlabel("Rule")
    ax.tick_params(axis="x", rotation=90)

    # ---- Subplot 4: Category Contributions (Pie Chart) ----
    ax = axs[1][1]
    ax.pie(
        cat_values,
        labels=categories,
        autopct='%1.1f%%',
        startangle=140
    )
    ax.set_title("Category Contributions")

    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()


def visualize_statistics_3d(state, scores):
    """
    Show a 3D figure with three subplots:
    1) 3D scatter: positives vs negatives vs score
    2) 3D "heat cube": destination × category × total rule intensity
    3) 3D bar landscape: net category contribution (pos - neg) by destination
    """
    destinations = DESTINATIONS

    # ----------------------------------
    # Common data: positives / negatives / scores
    # ----------------------------------
    pos_counts = []
    neg_counts = []
    score_values = []

    for d in destinations:
        pos_counts.append(len(state["recommended"][d]))
        neg_counts.append(len(state["not_recommended"][d]))
        score_values.append(scores[d])

    dest_indices = range(len(destinations))

    # Destination-category matrices
    categories, pos_matrix, neg_matrix = compute_dest_category_matrices(state)
    cat_indices = range(len(categories))

    # ----------------------------------
    # Create figure with 3D subplots
    # ----------------------------------
    fig = plt.figure(figsize=(16, 5))
    fig.suptitle("3D Systems Statistical Visualization")

    # ==================================
    # 1) 3D Scatter: Positives vs Negatives vs Score
    # ==================================
    ax1 = fig.add_subplot(1, 3, 1, projection='3d')
    xs = pos_counts
    ys = neg_counts
    zs = score_values

    ax1.scatter(xs, ys, zs)

    # Label each point with destination name
    for i, d in enumerate(destinations):
        ax1.text(xs[i], ys[i], zs[i], d)

    ax1.set_title("3D: Positives vs Negatives vs Score")
    ax1.set_xlabel("Positive rule count")
    ax1.set_ylabel("Negative rule count")
    ax1.set_zlabel("Score")

    # ==================================
    # 2) 3D Heat Cube: Dest × Category × Intensity
    #    Intensity = pos + neg per dest/category
    # ==================================
    ax2 = fig.add_subplot(1, 3, 2, projection='3d')

    heat_x = []   # destination index
    heat_y = []   # category index
    heat_z = []   # total intensity (pos + neg)

    for i, d in enumerate(destinations):
        for j, c in enumerate(categories):
            total = pos_matrix[d].get(c, 0) + neg_matrix[d].get(c, 0)
            heat_x.append(i)
            heat_y.append(j)
            heat_z.append(total)

    ax2.scatter(heat_x, heat_y, heat_z)
    ax2.set_title("3D Heat Cube: Dest × Category × Intensity")
    ax2.set_xlabel("Destination")
    ax2.set_ylabel("Category")
    ax2.set_zlabel("Total rules fired")

    ax2.set_xticks(list(dest_indices))
    ax2.set_xticklabels(destinations, rotation=45, ha="right")

    ax2.set_yticks(list(cat_indices))
    ax2.set_yticklabels(categories, rotation=45, ha="right")

    # ==================================
    # 3) 3D Bar Landscape: Category Contribution Terrain
    #    Net contribution = pos - neg per category
    # ==================================
    ax3 = fig.add_subplot(1, 3, 3, projection='3d')

    bar_x = []
    bar_y = []
    bar_z = []
    bar_dx = []
    bar_dy = []
    bar_dz = []

    width_x = 0.4
    width_y = 0.4

    for i, d in enumerate(destinations):
        for j, c in enumerate(categories):
            pos_val = pos_matrix[d].get(c, 0)
            neg_val = neg_matrix[d].get(c, 0)
            net = pos_val - neg_val  # net "vote" of that category

            if net >= 0:
                z_base = 0
                dz = net
            else:
                z_base = net
                dz = -net

            bar_x.append(i - width_x / 2.0)
            bar_y.append(j - width_y / 2.0)
            bar_z.append(z_base)
            bar_dx.append(width_x)
            bar_dy.append(width_y)
            bar_dz.append(dz)

    ax3.bar3d(bar_x, bar_y, bar_z, bar_dx, bar_dy, bar_dz)
    ax3.set_title("3D Bar Landscape: Category Contribution Terrain")
    ax3.set_xlabel("Destination")
    ax3.set_ylabel("Category")
    ax3.set_zlabel("Net contribution (pos - neg)")

    ax3.set_xticks(list(dest_indices))
    ax3.set_xticklabels(destinations, rotation=45, ha="right")

    ax3.set_yticks(list(cat_indices))
    ax3.set_yticklabels(categories, rotation=45, ha="right")

    fig.tight_layout(rect=[0, 0.03, 1, 0.92])
    plt.show()
