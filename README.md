# AI Travel Planner – Knowledge-Based Reasoning Agent

This project is a **knowledge-based AI Travel Planner agent** written in Python.  
It recommends one of seven destinations based on user preferences using **logical rules**, not machine learning.

Supported destinations:

- 🇨🇭 Switzerland  
- 🇮🇹 Italy  
- 🇯🇵 Japan  
- 🇬🇧 United Kingdom  
- 🇹🇷 Turkey  
- 🇦🇪 Dubai (UAE)  
- 🇸🇦 Saudi Arabia  

The agent:

- Provides both a **GUI** (graphical user interface) and **CLI** (command-line interface).  
- Uses a **hand-crafted knowledge base** (facts about destinations).  
- Applies **inference rules** to derive recommendations.  
- Computes a **score per destination**.  
- Explains *why* each place is good or bad for the user.  
- Shows a **reasoning trace** (which rules fired).  
- Provides **travel tips** for the final recommended destination(s).  
- Includes **comprehensive visa requirements and entry conditions** for all destinations.
- Includes **statistical visualizations** (2D and 3D charts).
- Is backed by an **OWL ontology** for graphical knowledge representation.

---

## 1. Project Structure

The project has been refactored into a modular architecture for better organization and maintainability:

```text
.
├── travel_core.py                               # Core inference engine and rule logic
├── travel_info.py                               # Static knowledge base (facts, rules, tips, explanations)
├── travel_plot.py                               # Visualization and plotting functions
├── travel_gui.py                                # Tkinter GUI for interactive use
├── travel_planner.owl                           # OWL ontology for graphical representation
├── README.md                                    # This documentation file
└── (optional) docs/                             # Report, diagrams, etc.
```

### Module Breakdown:

#### 📌 `travel_core.py`
The **core inference engine** containing:
- State management (`init_state()`)
- Rule implementations (R1–R25)
- Inference orchestration (`run_inference()`)
- Scoring logic (`compute_scores()`)
- Explanation building (`build_explanations()`)
- CLI helpers for interactive terminal mode

#### 📊 `travel_info.py`
**Static knowledge repository** containing:
- Destination list (`DESTINATIONS`) - Now includes 7 destinations
- Destination facts (`build_destination_facts()`) - Comprehensive attributes for each destination
- Travel tips for each destination (`TRAVEL_TIPS`) - Including visa requirements and entry conditions
- Rule categories (`RULE_CATEGORY`)
- Rule logic definitions (`RULE_LOGIC`)
- Human-readable explanations (`EXPLANATIONS`)

#### 📈 `travel_plot.py`
**Visualization module** containing:
- Helper functions for data aggregation
  - `compute_rule_frequency()` - Counts rule firings
  - `compute_category_contributions()` - Groups rules by category
  - `compute_dest_category_matrices()` - Builds matrices for 3D plots
- 2D visualization (`visualize_statistics()`)
  - Destination scores bar chart
  - Positive vs negative Evidence
  - Rule firing frequency
  - Category contributions pie chart
- 3D visualization (`visualize_statistics_3d()`)
  - 3D scatter plot: positives vs negatives vs score
  - 3D heat cube: destination × category × intensity
  - 3D bar landscape: category contribution terrain

#### 🖥️ `travel_gui.py`
**Graphical user interface** providing:
- Modern form-based input with grouped sections
- Tab-based workflow (Form → Results → Charts → Reasoning)
- Embedded matplotlib visualizations
- Rich text formatting for recommendations
- **Dedicated visa information display** with special formatting
- Visa requirements shown prominently for each destination
- 3D visualization window
- Responsive layout

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
        "expensive": ["Switzerland", "Japan", "Dubai"],
        "medium_cost": ["Italy", "United_Kingdom", "Saudi"],
        "budget_friendly": ["Turkey"],

        "excellent_public_transport": ["Switzerland", "Japan", "Dubai"],
        "good_public_transport": ["Italy", "United_Kingdom"],

        "good_for_nature_scenery": ["Switzerland", "Saudi"],
        "good_for_culture_history": ["Italy", "Switzerland", "United_Kingdom", "Saudi"],
        "good_for_city_life": ["Italy", "Japan", "United_Kingdom", "Dubai"],
        "good_for_shopping": ["Italy", "Japan", "Turkey", "Dubai", "Saudi"],
        "good_for_adventure": ["Switzerland", "Japan", "Turkey", "Dubai", "Saudi"],

        "good_local_cuisine": ["Italy", "Turkey", "Dubai", "Saudi"],

        "very_safe_destination": ["Switzerland", "Japan", "Dubai", "Saudi"],
        "mid_safety": ["Italy", "United_Kingdom", "Turkey"],

        "high_traffic_peak": ["Italy", "Japan", "Dubai"],
        "mid_traffic_in_cities": ["Switzerland", "United_Kingdom", "Turkey", "Saudi"],
        "low_traffic_outside_cities": ["Switzerland", "Saudi"],

        "best_season": {
            "Switzerland": ["spring", "summer"],
            "Italy": ["spring", "autumn"],
            "Japan": ["spring", "autumn"],
            "United_Kingdom": ["summer"],
            "Turkey": ["spring"],
            "Dubai": ["winter", "spring"],
            "Saudi": ["winter", "spring"],
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

## 10. Travel Tips with Visa Requirements (`TRAVEL_TIPS` and final output)

For each destination, there is a comprehensive set of **travel tips including visa requirements and entry conditions**:

```python
TRAVEL_TIPS = {
    "Switzerland": [
        "Pack layers and a warm jacket – weather can change quickly.",
        "Public transport is excellent – consider a travel pass.",
        "Bring comfortable shoes; many scenic spots involve walking.",
        "Food can be expensive; plan your budget.",
        "Respect quiet hours and local etiquette.",
        "Visa: Switzerland is part of the Schengen Area. Many nationalities can visit visa-free for up to 90 days within 180 days.",
        "EU/EEA/Swiss citizens only need a valid ID card. Others should check if they need a Schengen visa.",
        "Apply for a Schengen visa at least 15 days before travel; processing can take up to 15 working days."
    ],
    "Dubai": [
        "Dress modestly in public areas; swimwear is fine at beaches and pools but cover up elsewhere.",
        "The metro and taxis are clean, efficient, and affordable for getting around the city.",
        "Avoid visiting during peak summer (June-August) as temperatures can exceed 40°C/104°F.",
        "Visa: UAE offers visa-on-arrival for many nationalities (30-90 days). Others can apply for e-Visa online.",
        "Check if your nationality is eligible for free visa-on-arrival or needs pre-approval through UAE immigration.",
        "Passport must be valid for at least 6 months from entry date; return ticket may be required."
    ],
    "Saudi": [
        "Dress modestly – women should wear an abaya in public, and men should avoid shorts in religious sites.",
        "Respect prayer times; many shops and restaurants close briefly during these periods.",
        "Visit historical sites like Al-Ula, Diriyah, and the ancient Nabatean city of Madain Saleh.",
        "Visa: Saudi now offers e-Visa and visa-on-arrival for tourists from eligible countries (1-year validity, 90-day stay).",
        "Apply online through the official Saudi visa portal; approval usually takes 5-30 minutes for e-Visa.",
        "Passport must be valid for at least 6 months; travel insurance is mandatory for visa approval."
    ],
    # ... Italy, Japan, United_Kingdom, Turkey (all include visa information)
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

### Prerequisites

1. Make sure you have **Python 3** installed.
2. Install required dependencies:

```bash
pip install matplotlib
```

### Running the GUI (Recommended)

The easiest way to use the travel planner is through the graphical interface:

```bash
python travel_gui.py
```

Or directly run the main file (which launches the GUI by default):

```bash
python travel_core.py
```

**Using the GUI:**
1. Fill out the form in the "Plan Your Trip" tab with your preferences
2. Click "Find My Destination ➔"
3. View results in the "Recommendations" tab
4. Explore statistical charts in the "Visualizations" tab
5. Click "Open 3D View" for interactive 3D visualizations
6. Check the "Reasoning Logic" tab to see the inference trace
7. Review visa requirements prominently displayed for each destination

### Running CLI Mode

To use the command-line interface instead:

1. Open `travel_core.py`
2. Uncomment the CLI code section at the bottom (currently commented out)
3. Comment out the GUI launch code
4. Run:

```bash
python travel_core.py
```

5. Answer the questions in the terminal (budget, season, preferences, etc.)
6. Read the output:
   * Ranked destinations
   * Reason explanations
   * Travel tips
   * Global flags
   * Raw reasoning trace

---

## 13. Benefits of Modular Architecture

The project has been refactored into separate modules for improved maintainability:

### 🎯 **Separation of Concerns**
- **Data** (`travel_info.py`) - All static information in one place
- **Logic** (`ai_travel_destination_planner_agent_main.py`) - Pure inference rules
- **Visualization** (`travel_plot.py`) - Plotting code isolated
- **Interface** (`travel_gui.py`) - GUI separate from business logic

### ✨ **Advantages**

1. **Easier Maintenance**: Changes to facts/tips don't require touching inference logic
2. **Better Organization**: ~500 lines of code properly separated into focused modules
3. **Reusability**: Plotting functions can be used by both GUI and CLI
4. **Testability**: Each module can be tested independently
5. **Scalability**: Easy to add new destinations, rules, or visualization types
6. **Collaboration**: Multiple developers can work on different modules simultaneously

### 📦 **Import Structure**
```python
# travel_gui.py imports from all modules:
from travel_core import run_inference, compute_scores
from travel_info import DESTINATIONS, TRAVEL_TIPS
from travel_plot import visualize_statistics, visualize_statistics_3d
```

---

## 14. How to Customize

With the modular structure, customization is straightforward:

### 1. Add new facts (edit `travel_info.py`)

* Add new activities (e.g., `nightlife`) to destination facts
* Add more detailed traffic or safety levels
* Add new destinations to `DESTINATIONS` list (currently supports 7 destinations)
* Update `TRAVEL_TIPS` with tips and visa requirements for new destinations
* Update destination facts in `build_destination_facts()` to include new destinations

### 2. Add new rules (edit `travel_core.py`)

* Create new rule functions (e.g., `rule_weather_preferences`)
* Add their logic to `RULE_LOGIC` in `travel_info.py`
* Add to `RULE_CATEGORY` in `travel_info.py`
* Call them inside `run_inference()`
* Add human explanations to `EXPLANATIONS` in `travel_info.py`

### 3. Customize visualizations (edit `travel_plot.py`)

* Modify existing chart types
* Add new plot types (e.g., heatmaps, network graphs)
* Change colors, styles, or layouts
* Add export functionality for charts

### 4. Enhance the GUI (edit `travel_gui.py`)

* Add new input fields for additional preferences
* Customize color schemes and styling
* Add new tabs or sections
* Implement export/save functionality

### 5. Tweak scoring (edit `travel_core.py`)

* Change weights in `compute_scores()` if you want different behavior.
* Adjust scoring logic to prioritize different factors

### 6. Localize wording

* Change explanations and tips to another language.
* Customize EXPLANATIONS to match your report style.

---

## 15. Summary

This project demonstrates a **small but complete knowledge-based AI system** with modern software engineering practices:

* Clear **PEAS model** (Performance, Environment, Actuators, Sensors)
* Explicit **facts and rules** instead of hidden ML
* Transparent reasoning with **full rule traces**
* A matching **OWL ontology** for graphical representation
* **Modular architecture** with separated concerns (data, logic, visualization, interface)
* **Dual interface**: User-friendly GUI and CLI options
* **Rich visualizations**: 2D charts and interactive 3D plots
* Comprehensive explanations with travel tips

### Key Features:

✅ **Knowledge-Based Reasoning** - Uses logical inference, not machine learning  
✅ **Explainable AI** - Every recommendation comes with clear reasoning  
✅ **Modular Design** - Clean separation into 4 focused modules  
✅ **Visual Analytics** - Statistical charts showing decision factors  
✅ **Interactive GUI** - Modern Tkinter interface with tabs and visualizations  
✅ **Comprehensive Visa Information** - Detailed visa requirements and entry conditions for all 7 destinations  
✅ **Ontology Integration** - OWL file for semantic representation  
✅ **Expanded Coverage** - Now supports 7 destinations across Europe, Asia, and Middle East  

It is ideal for:

* AI / Knowledge-Based Systems coursework
* Demonstrating logical inference, Modus Ponens, and entailment
* Showcasing explainable AI in a small, understandable domain
* Learning modular Python project architecture
* Understanding rule-based expert systems   



here is an example of the truth table:
| Destination      | Exp | MedCost | Budget | ExPT | GoodPT | GoodCuisine | VerySafe | MidSafe | HighTraffic | MidTraffic | LowTrafficOut |
|------------------|:---:|:-------:|:------:|:----:|:------:|:-----------:|:--------:|:-------:|:-----------:|:----------:|:-------------:|
| Switzerland      |  T  |    F    |   F    |  T   |   F    |      F      |    T     |    F    |      F      |     T      |       T       |
| Italy            |  F  |    T    |   F    |  F   |   T    |      T      |    F     |    T    |      T      |     F      |       F       |
| Japan            |  T  |    F    |   F    |  T   |   F    |      F      |    T     |    F    |      T      |     F      |       F       |
| United_Kingdom   |  F  |    T    |   F    |  F   |   T    |      F      |    F     |    T    |      F      |     T      |       F       |
| Turkey           |  F  |    F    |   T    |  F   |   F    |      T      |    F     |    T    |      F      |     T      |       F       |
| Dubai            |  T  |    F    |   F    |  T   |   F    |      T      |    T     |    F    |      T      |     F      |       F       |
| Saudi            |  F  |    T    |   F    |  F   |   F    |      T      |    T     |    F    |      F      |     T      |       T       |


a table for Tabs navigation with GUI:
| **Tab Name**                           | **Purpose**                                            | **Contents / Functions**                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| -------------------------------------- | ------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1. Travel Form**                     | Collect user preferences                               | • Budget level  <br>• Preferred season  <br>• Trip duration  <br>• Activity preferences (nature, adventure, culture, shopping, city life)  <br>• Crowd tolerance  <br>• Traffic preference (low/mid/high)  <br>• Transport mode (public transport, walking, car/taxi)  <br>• Food preference (local/familiar)  <br>• Safety priority (high/medium/low concern)  <br>• Travel companions (solo, dual, family)  <br>• **Submit button** triggers inference engine                                     |
| **2. Recommendations**                 | Display reasoning results to user                      | • **Final recommended destination(s)**  <br>• Ranked list of all destinations with scores  <br>• Positive reasoning explanations  <br>• Negative evidence explanations  <br>• Season match / weak match indicators  <br>• Strong recommendation indicators  <br>• **Travel Tips section** including:  <br> – Destination-specific guidance  <br> – Cultural etiquette  <br> – Costs  <br> – Transport guidance  <br> – Weather considerations  <br> – **Visa information** (for all 7 destinations) |
| **3. Charts & Analytics**              | Provide visual insights into reasoning                 | • **Systems Statistical Visualization (4 Subplots):**  <br> 1. Destination Score Bar Chart  <br> 2. Positive vs Negative Evidence Chart  <br> 3. Rule Firing Frequency (Line Plot with Dots)  <br> 4. Category Contributions (Pie Chart)  <br><br>• Visualization auto-renders after inference  <br>• **“Open 3D Charts” button** opens additional window                                                                                                                                           |
| **4. 3D Visualization (Popup Window)** | Advanced analysis for presentations or deeper insights | • 3D Scatter Plot (Score vs Positives vs Negatives)  <br>• 3D Heat Cube (Destination × Category × Intensity)  <br>• 3D Category Terrain (3D bar landscape)  <br>• Interactive camera controls                                                                                                                                                                                                                                                                                                       |
| **5. Reasoning Trace**                 | Transparency & explainable-AI output                   | • Full RAW reasoning trace  <br>• Each fired rule listed in order  <br>• Logical meaning                                                                                                                                                                                                                                                                                                                                                                                                            |
