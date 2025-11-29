# =============================================
# AI - Travel Destination Planner Agent
# =============================================
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # needed for 3D plots in some Matplotlib versions

# Import all static travel information from travel_info module
from travel_info import (
    DESTINATIONS,
    build_destination_facts,
    TRAVEL_TIPS,
    RULE_CATEGORY,
    RULE_LOGIC,
    EXPLANATIONS,
)


# ===========================
# 2. User profile dictionary
# ===========================

def build_sample_user():
    """
    Example user; later you can replace this with input() prompts.
    """
    user = {
        "budget": "medium",            # "low" | "medium" | "high"
        "prefers_season": "spring",    # "spring" | "summer" | "autumn" | "winter"
        "trip_duration": "medium",     # "short" | "medium" | "long"

        "likes": ["culture_history", "shopping"],  # list of experience types
        "crowd_tolerance": "prefers_quiet",        # "likes_lively" | "prefers_quiet"
        "climate_preference": "mild",              # "cool" | "mild" | "warm"

        "transport": "public_transport",           # "public_transport" | "walking" | "car_taxi"
        "traffic_preference": "low_traffic",       # "low_traffic" | "mid_traffic" | "high_traffic"

        "food_preference": "LovesLocalCuisine",    # "LovesLocalCuisine" | "PrefersFamiliarFood"
        "safety_priority": "HighSafety",           # "HighSafety" | "MediumSafety" | "LowSafetyConcern"
        "companions": "dual",                      # "solo" | "dual" | "family"
    }
    return user

# ===========================
# 3. Inference state dict
# ===========================

def init_state():
    state = {
        "recommended": {},
        "not_recommended": {},
        "strongly_recommended": [],
        "strongly_not_recommended": [],
        "neutral": [],
        "season_matched": [],
        "weak_recommendation": [],
        "contradictions": [],
        "flags": [],
        "trace": [],
        "final_recommendation": [],   # new: list of final recommended destinations
    }

    for d in DESTINATIONS:
        state["recommended"][d] = []
        state["not_recommended"][d] = []

    return state


# ===========================
# 4. Helper functions
# ===========================
def add_rec(state, dest, rule_name):
    """
    Add positive recommendation evidence if not already present,
    and append a readable rule-based trace line.
    """
    if rule_name not in state["recommended"][dest]:
        state["recommended"][dest].append(rule_name)
        logic = RULE_LOGIC.get(rule_name, "")
        if logic != "":
            msg = rule_name + ": " + logic + "; applied with X = " + dest
        else:
            msg = rule_name + ": recommended(" + dest + ")"
        state["trace"].append(msg)


def add_not_rec(state, dest, rule_name):
    """
    Add negative recommendation evidence if not already present,
    and append a readable rule-based trace line.
    """
    if rule_name not in state["not_recommended"][dest]:
        state["not_recommended"][dest].append(rule_name)
        logic = RULE_LOGIC.get(rule_name, "")
        if logic != "":
            msg = rule_name + ": " + logic + "; applied with X = " + dest
        else:
            msg = rule_name + ": not_recommended(" + dest + ")"
        state["trace"].append(msg)



def add_once(lst, value):
    """
    Add value to list if not already present.
    """
    if value not in lst:
        lst.append(value)


# Import plotting functions from travel_plot module
from travel_plot import (
    compute_rule_frequency,
    compute_category_contributions,
    compute_dest_category_matrices,
    visualize_statistics,
    visualize_statistics_3d,
)


# ===========================
# 5. Rule implementations
# ===========================
def rule_budget_vs_cost(user, dest_facts, state):
    # R1: budget(low) ∧ expensive(X) → not_recommended(X)
    if user["budget"] == "low":
        for d in DESTINATIONS:
            if d in dest_facts["expensive"]:
                add_not_rec(state, d, "R1_budget_low_avoid_expensive")

    # R2: budget(medium|high) ∧ expensive(X) → recommended(X)
    if user["budget"] == "medium" or user["budget"] == "high":
        for d in DESTINATIONS:
            if d in dest_facts["expensive"]:
                add_rec(state, d, "R2_budget_allows_expensive")


def rule_food_preferences(user, dest_facts, state):
    # R3: loves_local_cuisine ∧ good_local_cuisine(X) → recommended(X)
    if user["food_preference"] == "LovesLocalCuisine":
        for d in DESTINATIONS:
            if d in dest_facts["good_local_cuisine"]:
                add_rec(state, d, "R3_food_local_cuisine")


def rule_activity_preferences(user, dest_facts, state):
    likes = user["likes"]

    # R4: likes(culture_history) ∧ good_for_culture_history(X) → recommended(X)
    if "culture_history" in likes:
        for d in DESTINATIONS:
            if d in dest_facts["good_for_culture_history"]:
                add_rec(state, d, "R4_culture_history")

    # R5: likes(adventure) ∧ good_for_adventure(X) → recommended(X)
    if "adventure" in likes:
        for d in DESTINATIONS:
            if d in dest_facts["good_for_adventure"]:
                add_rec(state, d, "R5_adventure")

    # R6: likes(shopping) ∧ good_for_shopping(X) → recommended(X)
    if "shopping" in likes:
        for d in DESTINATIONS:
            if d in dest_facts["good_for_shopping"]:
                add_rec(state, d, "R6_shopping")

    # R7: likes(nature_scenery) ∧ good_for_nature_scenery(X) → recommended(X)
    if "nature_scenery" in likes:
        for d in DESTINATIONS:
            if d in dest_facts["good_for_nature_scenery"]:
                add_rec(state, d, "R7_nature")

    # R8: likes(city_life) ∧ good_for_city_life(X) → recommended(X)
    if "city_life" in likes:
        for d in DESTINATIONS:
            if d in dest_facts["good_for_city_life"]:
                add_rec(state, d, "R8_city_life")


def rule_season_matching(user, dest_facts, state):
    best_season = dest_facts["best_season"]
    pref = user["prefers_season"]

    # R9: prefers_season(S) ∧ best_season(X,S) → season_matched(X)
    for d in DESTINATIONS:
        if d in best_season and pref in best_season[d]:
            if d not in state["season_matched"]:
                state["season_matched"].append(d)
                logic = RULE_LOGIC.get("R9_season_match", "")
                if logic != "":
                    msg = "R9_season_match: " + logic + "; applied with X = " + d
                else:
                    msg = "R9_season_match: season_matched(" + d + ")"
                state["trace"].append(msg)

    # R10: prefers_season(S) ∧ ¬best_season(X,S) but X has some best season → weak_recommendation(X)
    for d in DESTINATIONS:
        if d in best_season:
            if pref not in best_season[d] and d not in state["weak_recommendation"]:
                state["weak_recommendation"].append(d)
                logic = RULE_LOGIC.get("R10_season_weak", "")
                if logic != "":
                    msg = "R10_season_weak: " + logic + "; applied with X = " + d
                else:
                    msg = "R10_season_weak: weak_recommendation(" + d + ")"
                state["trace"].append(msg)


def rule_traffic_and_transport(user, dest_facts, state):
    traffic_pref = user["traffic_preference"]
    transport = user["transport"]

    # R11: prefers_low_traffic ∧ high_traffic_peak(X) → not_recommended(X)
    if traffic_pref == "low_traffic":
        for d in DESTINATIONS:
            if d in dest_facts["high_traffic_peak"]:
                add_not_rec(state, d, "R11_low_traffic_avoid_high")

    # R12: prefers_high_traffic ∧ high_traffic_peak(X) → recommended(X)
    if traffic_pref == "high_traffic":
        for d in DESTINATIONS:
            if d in dest_facts["high_traffic_peak"]:
                add_rec(state, d, "R12_high_traffic_ok")

    # R13: prefers public transport & excellent_public_transport(X) → recommended(X)
    if transport == "public_transport":
        for d in DESTINATIONS:
            if d in dest_facts["excellent_public_transport"]:
                add_rec(state, d, "R13_public_transport")

    # R14: prefers walking & high_traffic_peak(X) → not_recommended(X)
    if transport == "walking":
        for d in DESTINATIONS:
            if d in dest_facts["high_traffic_peak"]:
                add_not_rec(state, d, "R14_walking_avoid_high_traffic")


def rule_safety(user, dest_facts, state):
    safety = user["safety_priority"]

    # R15: high_safety ∧ mid_safety(X) → not_recommended(X)
    if safety == "HighSafety":
        for d in DESTINATIONS:
            if d in dest_facts["mid_safety"]:
                add_not_rec(state, d, "R15_high_safety_avoid_mid")

    # R16: high_safety ∧ very_safe_destination(X) → recommended(X)
    if safety == "HighSafety":
        for d in DESTINATIONS:
            if d in dest_facts["very_safe_destination"]:
                add_rec(state, d, "R16_high_safety_prefers_very_safe")

    # R17: low_safety_concern → safety_not_a_constraint
    if safety == "LowSafetyConcern":
        add_once(state["flags"], "safety_not_a_constraint")
        logic = RULE_LOGIC.get("R17_low_safety_concern", "")
        if logic != "":
            msg = "R17_low_safety_concern: " + logic
        else:
            msg = "R17_low_safety_concern: safety_not_a_constraint"
        state["trace"].append(msg)


def rule_companions(user, dest_facts, state):
    companions = user["companions"]

    # R18: family ∧ good_for_adventure(X) ∧ high_traffic_peak(X) → not_recommended(X)
    if companions == "family":
        for d in DESTINATIONS:
            if d in dest_facts["good_for_adventure"] and d in dest_facts["high_traffic_peak"]:
                add_not_rec(state, d, "R18_family_avoid_risky_adventure_city")

    # R19: solo ∧ good_for_city_life(X) → recommended(X)
    if companions == "solo":
        for d in DESTINATIONS:
            if d in dest_facts["good_for_city_life"]:
                add_rec(state, d, "R19_solo_city_life")


def rule_strong_recommendations(state):
    # R20: recommended(X) ∧ season_matched(X) → strongly_recommended(X)
    for d in DESTINATIONS:
        if len(state["recommended"][d]) > 0 and d in state["season_matched"]:
            if d not in state["strongly_recommended"]:
                state["strongly_recommended"].append(d)
                logic = RULE_LOGIC.get("R20_strong_recommendation", "")
                if logic != "":
                    msg = "R20_strong_recommendation: " + logic + "; applied with X = " + d
                else:
                    msg = "R20_strong_recommendation: strongly_recommended(" + d + ")"
                state["trace"].append(msg)

    # R21: not_recommended(X) ∧ weak_recommendation(X) → strongly_not_recommended(X)
    for d in DESTINATIONS:
        if len(state["not_recommended"][d]) > 0 and d in state["weak_recommendation"]:
            if d not in state["strongly_not_recommended"]:
                state["strongly_not_recommended"].append(d)
                logic = RULE_LOGIC.get("R21_strong_not_recommendation", "")
                if logic != "":
                    msg = "R21_strong_not_recommendation: " + logic + "; applied with X = " + d
                else:
                    msg = "R21_strong_not_recommendation: strongly_not_recommended(" + d + ")"
                state["trace"].append(msg)


def rule_contradictions(state):
    # R22: recommended(X) ∧ not_recommended(X) → contradiction(X)
    for d in DESTINATIONS:
        if len(state["recommended"][d]) > 0 and len(state["not_recommended"][d]) > 0:
            if d not in state["contradictions"]:
                state["contradictions"].append(d)
                logic = RULE_LOGIC.get("R22_contradiction_detection", "")
                if logic != "":
                    msg = "R22_contradiction_detection: " + logic + "; applied with X = " + d
                else:
                    msg = "R22_contradiction_detection: contradiction(" + d + ")"
                state["trace"].append(msg)

    # R23: contradiction(X) → flag_inconsistency
    if len(state["contradictions"]) > 0 and "flag_inconsistency" not in state["flags"]:
        state["flags"].append("flag_inconsistency")
        logic = RULE_LOGIC.get("R23_flag_inconsistency", "")
        if logic != "":
            msg = "R23_flag_inconsistency: " + logic
        else:
            msg = "R23_flag_inconsistency: flag_inconsistency"
        state["trace"].append(msg)


def rule_neutral_and_final(state):
    # R24: ¬recommended(X) ∧ ¬not_recommended(X) → neutral(X)
    for d in DESTINATIONS:
        if len(state["recommended"][d]) == 0 and len(state["not_recommended"][d]) == 0:
            if d not in state["neutral"]:
                state["neutral"].append(d)
                logic = RULE_LOGIC.get("R24_neutral_default", "")
                if logic != "":
                    msg = "R24_neutral_default: " + logic + "; applied with X = " + d
                else:
                    msg = "R24_neutral_default: neutral(" + d + ")"
                state["trace"].append(msg)

    # R25: strongly_recommended(X) → final_recommendation(X)
    for d in state["strongly_recommended"]:
        if d not in state["final_recommendation"]:
            state["final_recommendation"].append(d)

        logic = RULE_LOGIC.get("R25_final_recommendation", "")
        if logic != "":
            msg = "R25_final_recommendation: " + logic + "; applied with X = " + d
        else:
            msg = "R25_final_recommendation: final_recommendation(" + d + ")"
        state["trace"].append(msg)

# ===========================
# 6. Main Ploting
# ===========================


def visualize_statistics(state, scores):
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



# ===========================
# 7. Run inference
# ===========================

def run_inference(user, dest_facts):
    state = init_state()

    # Base rules
    rule_budget_vs_cost(user, dest_facts, state)
    rule_food_preferences(user, dest_facts, state)
    rule_activity_preferences(user, dest_facts, state)
    rule_season_matching(user, dest_facts, state)
    rule_traffic_and_transport(user, dest_facts, state)
    rule_safety(user, dest_facts, state)
    rule_companions(user, dest_facts, state)

    # Higher-level rules
    rule_strong_recommendations(state)
    rule_contradictions(state)
    rule_neutral_and_final(state)

    return state



def compute_scores(state):
    scores = {}
    for d in DESTINATIONS:
        score = 0

        # +2 per positive rule
        score += 2 * len(state["recommended"][d])

        # -2 per negative rule
        score -= 2 * len(state["not_recommended"][d])

        # Season influence
        if d in state["season_matched"]:
            score += 1
        if d in state["weak_recommendation"]:
            score -= 1

        # Strong labels
        if d in state["strongly_recommended"]:
            score += 3
        if d in state["strongly_not_recommended"]:
            score -= 3

        scores[d] = score

    return scores

def build_explanations(state):
    """
    Build user-friendly explanation lists for each destination.
    Returns a dict: dest -> {"positives": [...], "negatives": [...]}
    """
    explanations = {}
    for d in DESTINATIONS:
        explanations[d] = {
            "positives": [],
            "negatives": [],
        }

        # From recommended rules
        for rule_name in state["recommended"][d]:
            if rule_name in EXPLANATIONS:
                if EXPLANATIONS[rule_name] not in explanations[d]["positives"]:
                    explanations[d]["positives"].append(EXPLANATIONS[rule_name])

        # From not_recommended rules
        for rule_name in state["not_recommended"][d]:
            if rule_name in EXPLANATIONS:
                if EXPLANATIONS[rule_name] not in explanations[d]["negatives"]:
                    explanations[d]["negatives"].append(EXPLANATIONS[rule_name])

        # Season matched
        if d in state["season_matched"]:
            text = "The timing of your trip matches one of the best seasons to visit."
            if text not in explanations[d]["positives"]:
                explanations[d]["positives"].append(text)

        # Weak season
        if d in state["weak_recommendation"]:
            text = "This destination is not at its peak in your preferred season."
            if text not in explanations[d]["negatives"]:
                explanations[d]["negatives"].append(text)

        # Strong labels
        if d in state["strongly_recommended"]:
            text = "Overall fit is strong based on your preferences."
            if text not in explanations[d]["positives"]:
                explanations[d]["positives"].append(text)

        if d in state["strongly_not_recommended"]:
            text = "Overall, it is strongly discouraged for this specific trip profile."
            if text not in explanations[d]["negatives"]:
                explanations[d]["negatives"].append(text)

    return explanations

# ===========================
# CLI helper functions
# ===========================

def ask_choice(prompt, options, default=None):
    """
    Ask the user to choose one value from options.
    Example: ask_choice("Choose budget", ["low","medium","high"], "medium")
    """
    while True:
        text_options = "/".join(options)
        if default is not None:
            raw = input(f"{prompt} ({text_options}) [default={default}]: ").strip().lower()
            if raw == "":
                return default
        else:
            raw = input(f"{prompt} ({text_options}): ").strip().lower()

        for opt in options:
            if raw == opt.lower():
                return opt

        print("  Invalid choice. Please enter one of:", ", ".join(options))


def ask_multi_choice(prompt, options):
    """
    Ask the user to select multiple values from a list.
    User can enter comma-separated options or leave blank for 'none'.
    Returns a list of chosen options.
    """
    print(prompt)
    print("Available options:", ", ".join(options))
    print("Type them separated by commas (e.g., nature_scenery,shopping) or press Enter for none.")
    raw = input("Your choices: ").strip().lower()

    if raw == "":
        return []

    parts = [p.strip() for p in raw.split(",") if p.strip() != ""]
    chosen = []
    for p in parts:
        for opt in options:
            if p == opt.lower() and opt not in chosen:
                chosen.append(opt)

    if len(chosen) == 0:
        print("  No valid options recognized, treating as 'none'.")
    return chosen

def build_user_from_cli():
    print("=== Travel Preference Questionnaire ===")

    # 1) Budget
    budget = ask_choice(
        "What is your budget level?",
        ["low", "medium", "high"],
        default="medium"
    )

    # 2) Preferred season
    prefers_season = ask_choice(
        "Which season do you prefer to travel in?",
        ["spring", "summer", "autumn", "winter"],
        default="spring"
    )

    # 3) Trip duration
    trip_duration = ask_choice(
        "How long is your trip?",
        ["short", "medium", "long"],
        default="medium"
    )

    # 4) Experience types
    likes_options = ["nature_scenery", "culture_history", "city_life", "shopping", "adventure"]
    likes = ask_multi_choice(
        "What types of experiences do you enjoy?",
        likes_options
    )

    # 5) Crowd tolerance
    crowd_tolerance = ask_choice(
        "How do you feel about crowds?",
        ["likes_lively", "prefers_quiet"],
        default="prefers_quiet"
    )

    # 6) Climate preference
    climate_preference = ask_choice(
        "What climate do you prefer?",
        ["cool", "mild", "warm"],
        default="mild"
    )

    # 7) Transport preference
    transport = ask_choice(
        "How do you prefer to move inside a city?",
        ["public_transport", "walking", "car_taxi"],
        default="public_transport"
    )

    # 8) Traffic preference
    traffic_preference = ask_choice(
        "How sensitive are you to traffic / crowded streets?",
        ["low_traffic", "mid_traffic", "high_traffic"],
        default="low_traffic"
    )

    # 9) Food preference
    food_pref_choice = ask_choice(
        "Food preference?",
        ["LovesLocalCuisine", "PrefersFamiliarFood"],
        default="LovesLocalCuisine"
    )

    # 10) Safety priority
    safety_priority = ask_choice(
        "How important is safety to you?",
        ["HighSafety", "MediumSafety", "LowSafetyConcern"],
        default="HighSafety"
    )

    # 11) Companions
    companions = ask_choice(
        "Who are you traveling with?",
        ["solo", "dual", "family"],
        default="solo"
    )

    user = {
        "budget": budget,
        "prefers_season": prefers_season,
        "trip_duration": trip_duration,
        "likes": likes,
        "crowd_tolerance": crowd_tolerance,
        "climate_preference": climate_preference,
        "transport": transport,
        "traffic_preference": traffic_preference,
        "food_preference": food_pref_choice,
        "safety_priority": safety_priority,
        "companions": companions,
    }

    print("\nThank you! Running the reasoning engine based on your answers...\n")
    return user

if __name__ == "__main__":
    # Launch GUI by default
    from travel_gui import main as gui_main
    gui_main()
    
    # ===== OLD CLI CODE (PRESERVED FOR REFERENCE) =====
    # Uncomment the section below to use CLI mode instead of GUI
    """
    dest_facts = build_destination_facts()
    # user = build_sample_user()   # old hardcoded example
    user = build_user_from_cli()   # new interactive version

    state = run_inference(user, dest_facts)

    # 1) Compute scores and explanations
    scores = compute_scores(state)
    explanations = build_explanations(state)

    # 2) Sort destinations by score (high to low)
    ranked = sorted(DESTINATIONS, key=lambda d: scores[d], reverse=True)

    print("=== RANKED DESTINATIONS (BEST FIRST) ===")
    for d in ranked:
        print("\n----------------------------------------")
        print("Destination:", d)
        print("Score:", scores[d])

        # Status labels
        labels = []
        if d in state["strongly_recommended"]:
            labels.append("STRONGLY RECOMMENDED")
        elif len(state["recommended"][d]) > 0:
            labels.append("RECOMMENDED")

        if d in state["strongly_not_recommended"]:
            labels.append("STRONGLY NOT RECOMMENDED")
        elif len(state["not_recommended"][d]) > 0:
            labels.append("HAS WARNINGS")

        if d in state["neutral"]:
            labels.append("NEUTRAL")

        if d in state["contradictions"]:
            labels.append("CONTRADICTING RULES")

        if len(labels) == 0:
            labels.append("NO STRONG EVIDENCE")

        print("Status:", ", ".join(labels))

        pos = explanations[d]["positives"]
        neg = explanations[d]["negatives"]

        if len(pos) > 0:
            print("\n  Why this destination might be GOOD for you:")
            for reason in pos:
                print("   -", reason)



        if len(neg) > 0:
            print("\n  Things to be careful about:")
            for reason in neg:
                print("   -", reason)


    # 3) Show travel tips for final recommendations
    print("\n========================================")
    if len(state["final_recommendation"]) > 0:
        print("=== TRAVEL TIPS FOR YOUR TOP DESTINATION(S) ===")
        for d in state["final_recommendation"]:
            print("\nDestination:", d)
            tips = TRAVEL_TIPS.get(d, [])
            if len(tips) == 0:
                print("  (No specific tips stored for this destination.)")
            else:
                for i, tip in enumerate(tips, start=1):
                    print("  Tip", i, ":", tip)
    else:
        # Fallback: if no strongly_recommended destination, suggest best-scoring one
        print("=== TRAVEL TIPS ===")
        print("No strongly recommended destination, showing tips for your highest-scoring option.")
        # pick best by score
        best_dest = ranked[0]
        print("\nDestination:", best_dest)
        tips = TRAVEL_TIPS.get(best_dest, [])
        if len(tips) == 0:
            print("  (No specific tips stored for this destination.)")
        else:
            for i, tip in enumerate(tips, start=1):
                print("  Tip", i, ":", tip)


    print("\n========================================")
    print("=== GLOBAL FLAGS ===")
    print(state["flags"])

    print("\n=== RAW REASONING TRACE (for report / debugging) ===")
    for step in state["trace"]:
        print(step)

    ENABLE_PLOTS = True

    if ENABLE_PLOTS:
        visualize_statistics(state, scores)
    """
