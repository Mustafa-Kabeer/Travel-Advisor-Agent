# =============================================
# Travel Information - Static Data Module
# =============================================
# This file contains all static information used in the travel advisor system:
# - Destination list
# - Destination facts/knowledge base
# - Travel tips
# - Rule categories and logic
# - Human-readable explanations

# ===========================
# 1. Destinations
# ===========================

DESTINATIONS = [
    "Switzerland",
    "Italy",
    "Japan",
    "United_Kingdom",
    "Turkey",
]


# ===========================
# 2. Destination Facts
# ===========================

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


# ===========================
# 3. Travel Tips
# ===========================

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
        "Cashless is more common now, but it's still useful to carry some cash for small places.",
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


# ===========================
# 4. Rule Categories
# ===========================

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


# ===========================
# 5. Rule Logic Definitions
# ===========================

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
# 6. Human-Readable Explanations
# ===========================

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
