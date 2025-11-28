# =============================================
# AI - Travel Destination Planner Agent
# =============================================
import matplotlib.pyplot as plt

DESTINATIONS = [
    "Switzerland",
    "Italy",
    "Japan",
    "United_Kingdom",
    "Turkey",
]



def build_destination_facts():
    """
    Structured knowledge base about destinations.
    Uses only dicts and lists.
    """
    dest_facts = {
        # Cost level
        "expensive": ["Switzerland", "Japan"],
        "medium_cost": ["Italy", "United_Kingdom"],
        "budget_friendly": ["Turkey"],

        # Transport quality
        "excellent_public_transport": ["Switzerland", "Japan"],
        "good_public_transport": ["Italy", "United_Kingdom"],

        # Activities / experiences
        "good_for_nature_scenery": ["Switzerland"],
        "good_for_culture_history": ["Italy", "Switzerland", "United_Kingdom"],
        "good_for_city_life": ["Italy", "Japan", "United_Kingdom"],
        "good_for_shopping": ["Italy", "Japan", "Turkey"],
        "good_for_adventure": ["Switzerland", "Japan", "Turkey"],

        # Food
        "good_local_cuisine": ["Italy", "Turkey"],

        # Safety
        "very_safe_destination": ["Switzerland", "Japan"],
        "mid_safety": ["Italy", "United_Kingdom", "Turkey"],

        # Traffic
        "high_traffic_peak": ["Italy", "Japan"],
        "mid_traffic_in_cities": ["Switzerland", "United_Kingdom", "Turkey"],
        "low_traffic_outside_cities": ["Switzerland"],

        # Seasons: destination -> list of best seasons
        "best_season": {
            "Switzerland": ["spring", "summer"],
            "Italy": ["spring", "autumn"],
            "Japan": ["spring", "autumn"],
            "United_Kingdom": ["summer"],
            "Turkey": ["spring"],
        },
    }

    return dest_facts

TRAVEL_TIPS = {
    "Switzerland": [
        "Pack layers and a warm jacket – weather can change quickly, even in summer.",
        "Public transport is excellent – consider getting a travel pass for trains and buses.",
        "Bring comfortable shoes; many scenic spots involve walking and light hiking.",
        "Food and services can be expensive; plan your budget for meals and activities.",
        "Respect quiet hours and local etiquette, especially in small towns and on trains.",
    ],
    "Italy": [
        "Carry a light scarf or shawl for visiting churches with dress codes.",
        "Book tickets in advance for popular attractions to avoid long queues.",
        "Be mindful of pickpockets in crowded tourist areas and on public transport.",
        "Many shops and small restaurants may close midday; check opening hours.",
        "Try local dishes in smaller, family-run places away from the main tourist streets.",
    ],
    "Japan": [
        "Consider getting a transport card (like a regional IC card) for easy metro and train travel.",
        "Learn a few basic phrases and be mindful of etiquette (quiet trains, no loud calls).",
        "Cashless is more common now, but it’s still useful to carry some cash for small places.",
        "Trash bins can be rare outdoors; carry a small bag for your rubbish.",
        "Queuing and personal space are important – follow local cues in stations and shops.",
    ],
    "United_Kingdom": [
        "Weather is unpredictable – pack layers and a compact umbrella or raincoat.",
        "Contactless card payments are widely accepted, even on buses and trains.",
        "Look both ways and be careful crossing roads; traffic keeps to the left.",
        "Trains can be expensive; check off-peak times or railcards for better prices.",
        "Pubs often have their own customs (order at the bar, keep your tab organized).",
    ],
    "Turkey": [
        "Dress modestly when visiting mosques and religious sites; bring a light scarf.",
        "In bazaars and markets, bargaining is common – be polite but firm.",
        "Use licensed taxis or well-known ride apps, and check the meter is running.",
        "Tap water quality can vary; consider bottled water if you are unsure.",
        "Try local foods like kebabs and meze, but be cautious with street food if you have a sensitive stomach.",
    ],
}

RULE_CATEGORY = {
    "R1_budget_low_avoid_expensive": "Budget",
    "R2_budget_allows_expensive": "Budget",

    "R3_food_local_cuisine": "Food",

    "R4_culture_history": "Activity",
    "R5_adventure": "Activity",
    "R6_shopping": "Activity",
    "R7_nature": "Activity",
    "R8_city_life": "Activity",

    "R9_season_match": "Season",
    "R10_season_weak": "Season",

    "R11_low_traffic_avoid_high": "Traffic",
    "R12_high_traffic_ok": "Traffic",

    "R13_public_transport": "Transport",
    "R14_walking_avoid_high_traffic": "Transport",

    "R15_high_safety_avoid_mid": "Safety",
    "R16_high_safety_prefers_very_safe": "Safety",
    "R17_low_safety_concern": "Safety",

    "R18_family_avoid_risky_adventure_city": "Companions",
    "R19_solo_city_life": "Companions",

    "R20_strong_recommendation": "Meta",
    "R21_strong_not_recommendation": "Meta",
    "R22_contradiction_detection": "Meta",
    "R23_flag_inconsistency": "Meta",
    "R24_neutral_default": "Meta",
    "R25_final_recommendation": "Meta",
}


RULE_LOGIC = {
    "R1_budget_low_avoid_expensive":
        "IF budget = low AND expensive(X) THEN not_recommended(X)",

    "R2_budget_allows_expensive":
        "IF budget ∈ {medium, high} AND expensive(X) THEN recommended(X)",

    "R3_food_local_cuisine":
        "IF loves_local_cuisine AND good_local_cuisine(X) THEN recommended(X)",

    "R4_culture_history":
        "IF likes(culture_history) AND good_for_culture_history(X) THEN recommended(X)",

    "R5_adventure":
        "IF likes(adventure) AND good_for_adventure(X) THEN recommended(X)",

    "R6_shopping":
        "IF likes(shopping) AND good_for_shopping(X) THEN recommended(X)",

    "R7_nature":
        "IF likes(nature_scenery) AND good_for_nature_scenery(X) THEN recommended(X)",

    "R8_city_life":
        "IF likes(city_life) AND good_for_city_life(X) THEN recommended(X)",

    "R9_season_match":
        "IF prefers_season(S) AND best_season(X,S) THEN season_matched(X)",

    "R10_season_weak":
        "IF prefers_season(S) AND best_season(X,S) is false BUT X has some best season THEN weak_recommendation(X)",

    "R11_low_traffic_avoid_high":
        "IF traffic_preference = low_traffic AND high_traffic_peak(X) THEN not_recommended(X)",

    "R12_high_traffic_ok":
        "IF traffic_preference = high_traffic AND high_traffic_peak(X) THEN recommended(X)",

    "R13_public_transport":
        "IF transport = public_transport AND excellent_public_transport(X) THEN recommended(X)",

    "R14_walking_avoid_high_traffic":
        "IF transport = walking AND high_traffic_peak(X) THEN not_recommended(X)",

    "R15_high_safety_avoid_mid":
        "IF safety_priority = HighSafety AND mid_safety(X) THEN not_recommended(X)",

    "R16_high_safety_prefers_very_safe":
        "IF safety_priority = HighSafety AND very_safe_destination(X) THEN recommended(X)",

    "R17_low_safety_concern":
        "IF safety_priority = LowSafetyConcern THEN safety_not_a_constraint",

    "R18_family_avoid_risky_adventure_city":
        "IF companions = family AND good_for_adventure(X) AND high_traffic_peak(X) THEN not_recommended(X)",

    "R19_solo_city_life":
        "IF companions = solo AND good_for_city_life(X) THEN recommended(X)",

    "R20_strong_recommendation":
        "IF recommended(X) AND season_matched(X) THEN strongly_recommended(X)",

    "R21_strong_not_recommendation":
        "IF not_recommended(X) AND weak_recommendation(X) THEN strongly_not_recommended(X)",

    "R22_contradiction_detection":
        "IF recommended(X) AND not_recommended(X) THEN contradiction(X)",

    "R23_flag_inconsistency":
        "IF contradiction(X) THEN flag_inconsistency",

    "R24_neutral_default":
        "IF no recommendation info for X THEN neutral(X)",

    "R25_final_recommendation":
        "IF strongly_recommended(X) THEN final_recommendation(X)",
}


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

def compute_rule_frequency(state):
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
    rule_freq = compute_rule_frequency(state)
    cat_counts = {}
    for rule, count in rule_freq.items():
        category = RULE_CATEGORY.get(rule, "Other")
        cat_counts[category] = cat_counts.get(category, 0) + count
    return cat_counts



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

import matplotlib.pyplot as plt

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

# Map rule names to human-friendly explanation snippets
EXPLANATIONS = {
    "R1_budget_low_avoid_expensive": "May be too expensive for your current budget.",
    "R2_budget_allows_expensive": "Your budget can handle more expensive destinations.",
    "R3_food_local_cuisine": "Famous for local cuisine that matches your food preferences.",
    "R4_culture_history": "Strong in culture and historical attractions.",
    "R5_adventure": "Offers good opportunities for adventure activities.",
    "R6_shopping": "Good destination for shopping and commercial areas.",
    "R7_nature": "Known for beautiful natural scenery.",
    "R8_city_life": "Has vibrant city life that matches your interests.",
    "R9_season_match": "Good match for your preferred travel season.",
    "R10_season_weak": "Not at its best during your preferred season.",
    "R11_low_traffic_avoid_high": "Can be very crowded / high-traffic, which conflicts with your low-traffic preference.",
    "R12_high_traffic_ok": "Lively and busy, matching your preference for active, crowded places.",
    "R13_public_transport": "Has excellent public transport, matching your preference.",
    "R14_walking_avoid_high_traffic": "High traffic makes walking less comfortable.",
    "R15_high_safety_avoid_mid": "Safety level may be lower than your high safety preference.",
    "R16_high_safety_prefers_very_safe": "Very safe and fits your high safety requirements.",
    "R17_low_safety_concern": "You are flexible about safety constraints.",
    "R18_family_avoid_risky_adventure_city": "May be too risky/crowded for a family trip with adventure focus.",
    "R19_solo_city_life": "Good for solo travelers who enjoy active city life.",
    "R20_strong_recommendation": "Overall fit is strong considering your preferences and season.",
    "R21_strong_not_recommendation": "Overall, it is strongly not recommended for this trip profile.",
    "R22_contradiction_detection": "There is a logical conflict in the reasoning about this place.",
    "R23_flag_inconsistency": "The system detected some inconsistency in the rules.",
    "R24_neutral_default": "No strong evidence for or against this destination.",
    "R25_final_recommendation": "Chosen as one of the top recommendations.",
}

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
