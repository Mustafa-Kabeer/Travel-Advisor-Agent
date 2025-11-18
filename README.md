---
marp: false
---


````markdown
# AI Travel Planner – Knowledge-Based Reasoning Agent

This project is a **knowledge-based AI Travel Planner agent** written in Python.  
It recommends one of five destinations based on user preferences using **logical rules**, not machine learning.

Supported destinations:

- 🇨🇭 Switzerland  
- 🇮🇹 Italy  
- 🇯🇵 Japan  
- 🇬🇧 United Kingdom  
- 🇹🇷 Turkey  

The agent:

- Asks the user questions in the **CLI** (terminal).  
- Uses a **hand-crafted knowledge base** (facts about destinations).  
- Applies **inference rules** to derive recommendations.  
- Computes a **score per destination**.  
- Explains *why* each place is good or bad for the user.  
- Shows a **reasoning trace** (which rules fired).  
- Provides **travel tips** for the final recommended destination(s).  
- Is backed by an **OWL ontology** for graphical knowledge representation.

---

## 1. Project Structure

Depending on how you organized your files, a typical structure might look like:

```text
.
├── travel_advisor_agent.py             # Main Python file (KB, rules, CLI, reasoning)
├── travel_planner.owl          # OWL ontology for graphical representation
├── README.md                   # This documentation file
└── (optional) docs/            # Report, diagrams, etc.
````

All the core logic lives in **`travel_advisor_agent.py`**.

---

## 2. High-Level Overview

This agent is designed as a **knowledge-based system**, not a data-driven model.

### Key ideas:

* The agent **does not learn** from data.
* Instead, it uses:

  * A **fixed set of facts** about destinations.
  * A **fixed set of logical rules** (IF–THEN).
* The system performs **forward-chaining**:
  it starts from the facts + user preferences and **derives new conclusions**.

### Main components:

1. **Destination knowledge base**
2. **User preference model (from CLI)**
3. **Inference engine with rules (R1–R25)**
4. **Scoring and ranking**
5. **Explanation & reasoning trace**
6. **Travel tips output**
7. **OWL ontology** (for graphical / semantic representation)

Each of these is explained in detail in the sections below.

---

## 3. Destination Knowledge Base (`build_destination_facts`)

This part defines **what the agent knows** about each country.

### Function:

```python
def build_destination_facts():
    dest_facts = {
        "expensive": ["Switzerland", "Japan"],
        "medium_cost": ["Italy", "United_Kingdom"],
        "budget_friendly": ["Turkey"],

        "excellent_public_transport": ["Switzerland", "Japan"],
        "good_public_transport": ["Italy", "United_Kingdom"],

        "good_for_nature_scenery": ["Switzerland"],
        "good_for_culture_history": ["Italy", "Switzerland", "United_Kingdom"],
        "good_for_city_life": ["Italy", "Japan", "United_Kingdom"],
        "good_for_shopping": ["Italy", "Japan", "Turkey"],
        "good_for_adventure": ["Switzerland", "Japan", "Turkey"],

        "good_local_cuisine": ["Italy", "Turkey"],

        "very_safe_destination": ["Switzerland", "Japan"],
        "mid_safety": ["Italy", "United_Kingdom", "Turkey"],

        "high_traffic_peak": ["Italy", "Japan"],
        "mid_traffic_in_cities": ["Switzerland", "United_Kingdom", "Turkey"],
        "low_traffic_outside_cities": ["Switzerland"],

        "best_season": {
            "Switzerland": ["spring", "summer"],
            "Italy": ["spring", "autumn"],
            "Japan": ["spring", "autumn"],
            "United_Kingdom": ["summer"],
            "Turkey": ["spring"],
        },
    }
    return dest_facts
```

### What this means:

* The KB is a **Python dictionary** of lists and nested dictionaries.

* Each key corresponds to a **predicate** from logic:

  * `expensive`: list of expensive destinations
  * `good_for_adventure`: list of adventure destinations
  * `best_season`: maps each destination → list of best seasons

* This KB is **static**: it doesn’t change at runtime.

In logical terms, a fact like:

```python
"good_for_adventure": ["Switzerland", "Japan", "Turkey"]
```

is equivalent to:

* `good_for_adventure(Switzerland)`
* `good_for_adventure(Japan)`
* `good_for_adventure(Turkey)`

---

## 4. User Preferences & CLI Questionnaire (`build_user_from_cli`)

The agent collects preferences from the user via the command line.

### User representation

A user is stored as a **dictionary**:

```python
user = {
    "budget": "medium",
    "prefers_season": "spring",
    "trip_duration": "medium",
    "likes": ["culture_history", "shopping"],
    "crowd_tolerance": "prefers_quiet",
    "climate_preference": "mild",
    "transport": "public_transport",
    "traffic_preference": "low_traffic",
    "food_preference": "LovesLocalCuisine",
    "safety_priority": "HighSafety",
    "companions": "dual",
}
```

### How it is built

The function `build_user_from_cli()` interacts with the user:

* It uses small helpers like `ask_choice` and `ask_multi_choice`:

  * `ask_choice()` → choose one option from a list (`low/medium/high`, etc.).
  * `ask_multi_choice()` → choose several activities (`shopping, adventure, ...`).

Example questions:

* *“What is your budget level? (low/medium/high)”*
* *“Which season do you prefer to travel in? (spring/summer/autumn/winter)”*
* *“What types of experiences do you enjoy? (nature_scenery, culture_history, ...)”*
* *“How important is safety to you? (HighSafety/MediumSafety/LowSafetyConcern)”*

The answers are stored in the `user` dict and passed to the reasoning engine.

---

## 5. Inference State (`init_state`)

The agent keeps track of derived conclusions in a **state dictionary**.

```python
def init_state():
    state = {
        "recommended": {},            # dest -> [rule names]
        "not_recommended": {},        # dest -> [rule names]
        "strongly_recommended": [],   # [dest]
        "strongly_not_recommended": [], # [dest]
        "neutral": [],                # [dest]
        "season_matched": [],         # [dest]
        "weak_recommendation": [],    # [dest]
        "contradictions": [],         # [dest]
        "flags": [],                  # e.g. ["flag_inconsistency"]
        "trace": [],                  # list of reasoning steps (strings)
        "final_recommendation": [],   # [dest]
    }

    for d in DESTINATIONS:
        state["recommended"][d] = []
        state["not_recommended"][d] = []

    return state
```

### Meaning:

* `recommended[d]` → which rules **support** recommending destination `d`.
* `not_recommended[d]` → which rules **argue against** `d`.
* `season_matched` → destinations that match user’s chosen season.
* `strongly_recommended` → destinations that are recommended + season matched.
* `contradictions` → destinations with both positive and negative evidence.
* `trace` → human-readable log of all rules that fired.
* `final_recommendation` → final top destination(s).

---

## 6. Inference Rules (R1–R25)

The core intelligence is in the **rule functions**.
Each rule is a logical sentence like:

> IF budget = low AND destination is expensive → NOT recommended(destination)

In code, rules are implemented as functions:

* `rule_budget_vs_cost`
* `rule_food_preferences`
* `rule_activity_preferences`
* `rule_season_matching`
* `rule_traffic_and_transport`
* `rule_safety`
* `rule_companions`
* `rule_strong_recommendations`
* `rule_contradictions`
* `rule_neutral_and_final`

### Example: Budget vs Cost (R1, R2)

```python
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
```

### Example: Activities (R4–R8)

```python
def rule_activity_preferences(user, dest_facts, state):
    likes = user["likes"]

    if "culture_history" in likes:
        for d in DESTINATIONS:
            if d in dest_facts["good_for_culture_history"]:
                add_rec(state, d, "R4_culture_history")

    if "adventure" in likes:
        for d in DESTINATIONS:
            if d in dest_facts["good_for_adventure"]:
                add_rec(state, d, "R5_adventure")

    if "shopping" in likes:
        for d in DESTINATIONS:
            if d in dest_facts["good_for_shopping"]:
                add_rec(state, d, "R6_shopping")

    if "nature_scenery" in likes:
        for d in DESTINATIONS:
            if d in dest_facts["good_for_nature_scenery"]:
                add_rec(state, d, "R7_nature")

    if "city_life" in likes:
        for d in DESTINATIONS:
            if d in dest_facts["good_for_city_life"]:
                add_rec(state, d, "R8_city_life")
```

Each rule implements **Modus Ponens** in code:

> IF conditions are true in `user` and `dest_facts`
> THEN call `add_rec` or `add_not_rec`.

---

## 7. Rule Explanations & Reasoning Trace (`RULE_LOGIC`, `add_rec`, `add_not_rec`)

To make the system explainable, each rule has a **logic statement**:

```python
RULE_LOGIC = {
    "R4_culture_history":
        "IF likes(culture_history) AND good_for_culture_history(X) THEN recommended(X)",
    # ...
}
```

Whenever a rule fires, the system logs a detailed trace line:

```python
def add_rec(state, dest, rule_name):
    if rule_name not in state["recommended"][dest]:
        state["recommended"][dest].append(rule_name)
        logic = RULE_LOGIC.get(rule_name, "")
        if logic != "":
            msg = rule_name + ": " + logic + "; applied with X = " + dest
        else:
            msg = rule_name + ": recommended(" + dest + ")"
        state["trace"].append(msg)
```

Example trace output:

```text
R4_culture_history: IF likes(culture_history) AND good_for_culture_history(X) THEN recommended(X); applied with X = Italy
R13_public_transport: IF transport = public_transport AND excellent_public_transport(X) THEN recommended(X); applied with X = Japan
R9_season_match: IF prefers_season(S) AND best_season(X,S) THEN season_matched(X); applied with X = Japan
R20_strong_recommendation: IF recommended(X) AND season_matched(X) THEN strongly_recommended(X); applied with X = Japan
R25_final_recommendation: IF strongly_recommended(X) THEN final_recommendation(X); applied with X = Japan
```

This is **perfect for your report** as a reasoning trace example.

---

## 8. Scoring & Ranking (`compute_scores`, sorting)

After inference, each destination gets a **numeric score**:

```python
def compute_scores(state):
    scores = {}
    for d in DESTINATIONS:
        score = 0

        score += 2 * len(state["recommended"][d])      # positive evidence
        score -= 2 * len(state["not_recommended"][d])  # negative evidence

        if d in state["season_matched"]:
            score += 1
        if d in state["weak_recommendation"]:
            score -= 1

        if d in state["strongly_recommended"]:
            score += 3
        if d in state["strongly_not_recommended"]:
            score -= 3

        scores[d] = score

    return scores
```

Then the destinations are sorted:

```python
ranked = sorted(DESTINATIONS, key=lambda d: scores[d], reverse=True)
```

The higher the score, the better the match.

---

## 9. User-Friendly Explanations (`build_explanations`)

Instead of only showing rule names, the agent translates them into **human sentences**.

```python
EXPLANATIONS = {
    "R4_culture_history": "Strong in culture and historical attractions.",
    "R5_adventure": "Offers good opportunities for adventure activities.",
    "R13_public_transport": "Has excellent public transport, matching your preference.",
    # ...
}
```

`build_explanations(state)` collects the **positives** and **negatives** for each destination:

* Positives → reasons to go there
* Negatives → warnings or conflicts with preferences

These are printed under:

```text
Why this destination might be GOOD for you:
Things to be careful about:
```

---

## 10. Travel Tips (`TRAVEL_TIPS` and final output)

For each destination, there is a set of **5 static travel tips**:

```python
TRAVEL_TIPS = {
    "Switzerland": [
        "Pack layers and a warm jacket – weather can change quickly.",
        "Public transport is excellent – consider a travel pass.",
        "Bring comfortable shoes; many scenic spots involve walking.",
        "Food can be expensive; plan your budget.",
        "Respect quiet hours and local etiquette."
    ],
    "Italy": [
        "Carry a light scarf for churches.",
        "Book tickets in advance for popular attractions.",
        "Watch for pickpockets in crowded areas.",
        "Check opening hours; some places close midday.",
        "Try local food in smaller family-run places."
    ],
    # ... Japan, United_Kingdom, Turkey
}
```

At the end of the program, the agent:

* Looks at `state["final_recommendation"]`.
* Prints **tips for each strongly recommended destination**.
* If no strong recommendation exists, it shows tips for the **highest scoring** destination.

---

## 11. OWL Ontology (`travel_planner.owl`)

The OWL file **mirrors the Python KB** in a formal, graphical way:

* Classes: `Destination`, `Activity`, `Season`, `UserPreference`, `InferenceRule`, `RecommendationOutcome`, etc.
* Individuals: `Switzerland`, `Italy`, `Japan`, `ExampleUserPref`, `Rule_R4_CultureHistory`, `RecommendItaly`, etc.
* Object properties: `goodForActivity`, `hasBestSeason`, `hasCostLevel`, `triggersRecommendation`, `leadsTo`, `influences`, etc.

You can open it in **Protégé** to visualize the semantic network:

* `Destination` nodes in the center
* `UserPreference` on the left
* `InferenceRule` and `RecommendationOutcome` on the right

This satisfies the requirement of:

* ≥ 20 nodes
* ≥ 30 labeled links
* Clear “causes / leads to / influences / part of” relationships.

---

## 12. How to Run the Agent

1. Make sure you have **Python 3** installed.
2. Put all code in `travel_advisor_agent.py`.
3. Open a terminal in the project directory.
4. Run:

```bash
python travel_advisor_agent.py
```
or just use an editor.

5. Answer the questions in the CLI (budget, season, preferences, etc.).
6. Read the output:

   * Ranked destinations
   * Reason explanations
   * Travel tips
   * Global flags
   * Raw reasoning trace

---

## 13. How to Customize

You can easily extend the system:

### 1. Add new facts

* Add new activities (e.g., `nightlife`) and destinations that are good for them.
* Add more detailed traffic or safety levels.

### 2. Add new rules

* Create new rule functions.
* Add their logic to `RULE_LOGIC`.
* Call them inside `run_inference()`.

### 3. Tweak scoring

* Change weights in `compute_scores()` if you want different behavior.

### 4. Localize wording

* Change explanations and tips to another language.
* Customize EXPLANATIONS to match your report style.

---

## 14. Summary

This project demonstrates a **small but complete knowledge-based AI system**:

* Clear **PEAS model** (Performance, Environment, Actuators, Sensors).
* Explicit **facts and rules** instead of hidden ML.
* Transparent reasoning with **full rule traces**.
* A matching **OWL ontology** for graphical representation.
* User-friendly CLI and explanations.

It is ideal for:

* AI / Knowledge-Based Systems coursework
* Demonstrating logical inference, Modus Ponens, and entailment
* Showcasing explainable AI in a small, understandable domain   
* 
| Destination      | Exp | MedCost | Budget | ExPT | GoodPT | GoodCuisine | VerySafe | MidSafe | HighTraffic | MidTraffic | LowTrafficOut |
|------------------|:---:|:-------:|:------:|:----:|:------:|:-----------:|:--------:|:-------:|:-----------:|:----------:|:-------------:|
| Switzerland      |  T  |    F    |   F    |  T   |   F    |      F      |    T     |    F    |      F      |     T      |       T       |
| Italy            |  F  |    T    |   F    |  F   |   T    |      T      |    F     |    T    |      T      |     F      |       F       |
| Japan            |  T  |    F    |   F    |  T   |   F    |      F      |    T     |    F    |      T      |     F      |       F       |
| United_Kingdom   |  F  |    T    |   F    |  F   |   T    |      F      |    F     |    T    |      F      |     T      |       F       |
| Turkey           |  F  |    F    |   T    |  F   |   F    |      T      |    F     |    T    |      F      |     T      |       F       |
