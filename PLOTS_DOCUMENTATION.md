# Travel Plotting Module Documentation

## Overview

The **Travel Plotting Module** ([travel_plot.py](file:///c:/Users/ibrah/PyCharmMiscProject/Travel-Advisor-Agent/travel_plot.py)) is a comprehensive visualization system for the Travel Advisor Agent. It provides advanced statistical visualizations to analyze and display the expert system's decision-making process, including rule firing frequencies, category contributions, and destination scoring analysis.

---

## Table of Contents

1. [Dependencies](#dependencies)
2. [Module Architecture](#module-architecture)
3. [Helper Functions](#helper-functions)
4. [Visualization Functions](#visualization-functions)
5. [Usage Examples](#usage-examples)
6. [Data Structures](#data-structures)

---

## Dependencies

### External Libraries
- **matplotlib.pyplot**: For creating all visualizations (2D and 3D plots)

### Internal Imports
- **DESTINATIONS**: List of all available travel destinations
- **RULE_CATEGORY**: Mapping of rule names to their categories (from `travel_info` module)

---

## Module Architecture

The module is organized into two main sections:

```
travel_plot.py
├── Helper Functions (Data Processing)
│   ├── compute_rule_frequency()
│   ├── compute_category_contributions()
│   └── compute_dest_category_matrices()
│
└── Visualization Functions (Chart Generation)
    ├── visualize_statistics()
    └── visualize_statistics_3d()
```

---

## Helper Functions

### `compute_rule_frequency(state)`

**Purpose**: Counts how many times each rule fired during the inference process.

**Parameters**:
- `state` (dict): The inference state containing a `trace` list

**Returns**:
- `dict`: Mapping of rule names to their firing counts
  - Key: Rule name (str)
  - Value: Number of times the rule fired (int)

**Algorithm**:
1. Iterates through each entry in `state["trace"]`
2. Parses each trace line to extract the rule name (before the colon)
3. Increments the count for each rule occurrence

**Example Output**:
```python
{
    "R4_culture_history": 3,
    "R7_beach_paradise": 2,
    "R10_budget_friendly": 1
}
```

---

### `compute_category_contributions(state)`

**Purpose**: Groups rule firings by category and counts total contributions per category.

**Parameters**:
- `state` (dict): The inference state containing trace information

**Returns**:
- `dict`: Mapping of categories to their total rule firing counts
  - Key: Category name (str)
  - Value: Total number of rule firings in that category (int)

**Algorithm**:
1. Calls `compute_rule_frequency()` to get individual rule counts
2. Uses `RULE_CATEGORY` to map each rule to its category
3. Aggregates counts by category
4. Rules without a category mapping are grouped under "Other"

**Example Output**:
```python
{
    "Culture & History": 5,
    "Beach & Relaxation": 3,
    "Budget": 2,
    "Adventure": 1
}
```

---

### `compute_dest_category_matrices(state)`

**Purpose**: Builds matrices tracking positive and negative rule firings per destination-category combination.

**Parameters**:
- `state` (dict): The inference state with `recommended` and `not_recommended` data

**Returns**:
- **Tuple** of three elements:
  1. `categories` (list): List of all category names
  2. `pos_matrix` (dict): Positive rule counts per destination per category
  3. `neg_matrix` (dict): Negative rule counts per destination per category

**Matrix Structure**:
```python
pos_matrix = {
    "Paris": {"Culture & History": 3, "Adventure": 1, ...},
    "Tokyo": {"Culture & History": 2, "Beach & Relaxation": 0, ...},
    ...
}
```

**Algorithm**:
1. Collects all unique categories from `RULE_CATEGORY`
2. Initializes both matrices with zeros for all destination-category pairs
3. Counts positive rules from `state["recommended"][destination]`
4. Counts negative rules from `state["not_recommended"][destination]`

---

## Visualization Functions

### `visualize_statistics(state, scores)`

**Purpose**: Creates a comprehensive 2×2 grid of statistical visualizations showing different aspects of the recommendation system.

**Parameters**:
- `state` (dict): The inference state containing trace and recommendation data
- `scores` (dict): Destination scores (destination name → score value)

**Output**: A matplotlib figure with four subplots in a 2×2 layout

#### Subplot 1: Destination Scores (Top-Left)

**Chart Type**: Bar Chart

**Purpose**: Displays the final score for each destination

**Axes**:
- X-axis: Destinations
- Y-axis: Score values

**Visual Elements**:
- Simple vertical bars showing relative scores
- Higher bars indicate better matches

---

#### Subplot 2: Positive vs Negative Evidence (Top-Right)

**Chart Type**: Grouped Bar Chart

**Purpose**: Compares the number of positive and negative rules that fired for each destination

**Axes**:
- X-axis: Destinations (rotated 15° for readability)
- Y-axis: Rule count

**Visual Elements**:
- Blue bars: Positive evidence (rules recommending the destination)
- Orange bars: Negative evidence (rules against the destination)
- Bars grouped side-by-side with width=0.35
- Legend distinguishing positive vs negative

**Interpretation**: Large positive-to-negative ratio suggests strong recommendation

---

#### Subplot 3: Rule Firing Frequency (Bottom-Left)

**Chart Type**: Line Chart with Markers

**Purpose**: Shows how frequently each individual rule fired during inference

**Axes**:
- X-axis: Rule names (rotated 90° for readability)
- Y-axis: Firing count

**Visual Elements**:
- Line connecting data points with linewidth=2
- Circular markers ('o') at each data point
- Helps identify most influential rules

---

#### Subplot 4: Category Contributions (Bottom-Right)

**Chart Type**: Pie Chart

**Purpose**: Shows the proportional contribution of each category to the overall reasoning

**Visual Elements**:
- Slices representing each category
- Percentages displayed on each slice (autopct='%1.1f%%')
- Start angle at 140° for optimal label positioning

**Interpretation**: Larger slices indicate categories that played a bigger role in the decision

---

**Figure Properties**:
- Size: 14×10 inches
- Title: "Systems Statistical Visualization"
- Layout: Tight layout with margin for title (rect=[0, 0.03, 1, 0.95])

---

### `visualize_statistics_3d(state, scores)`

**Purpose**: Creates advanced 3D visualizations showing multi-dimensional relationships in the recommendation data.

**Parameters**:
- `state` (dict): The inference state
- `scores` (dict): Destination scores

**Output**: A matplotlib figure with three 3D subplots in a 1×3 layout

#### Subplot 1: 3D Scatter - Positives vs Negatives vs Score

**Chart Type**: 3D Scatter Plot

**Purpose**: Visualizes the relationship between positive evidence, negative evidence, and final score

**Axes**:
- X-axis: Positive rule count
- Y-axis: Negative rule count
- Z-axis: Final score

**Visual Elements**:
- Each point represents a destination
- Text labels showing destination names at each point
- Spatial positioning reveals scoring patterns

**Interpretation**:
- High X, low Y, high Z: Strong recommendation
- Low X, high Y, low Z: Strong rejection
- Balanced X and Y: Mixed signals

---

#### Subplot 2: 3D Heat Cube - Destination × Category × Intensity

**Chart Type**: 3D Scatter Plot (representing a heat cube)

**Purpose**: Shows the total rule activity (positive + negative) for each destination-category combination

**Axes**:
- X-axis: Destination (categorical, indexed 0-n)
- Y-axis: Category (categorical, indexed 0-n)
- Z-axis: Total intensity (pos + neg rules fired)

**Visual Elements**:
- Scattered points in 3D space
- X and Y tick labels show actual destination and category names
- Rotated labels (45°, right-aligned) for readability
- Higher Z-values indicate more rules fired for that combination

**Interpretation**: Identifies which destination-category pairs had the most activity during reasoning

---

#### Subplot 3: 3D Bar Landscape - Category Contribution Terrain

**Chart Type**: 3D Bar Chart

**Purpose**: Visualizes the net contribution (positive minus negative) of each category for each destination

**Axes**:
- X-axis: Destination
- Y-axis: Category
- Z-axis: Net contribution (pos - neg)

**Visual Elements**:
- 3D bars rising from the base plane
- Bar width: 0.4 units in both X and Y directions
- Positive net contributions extend upward from Z=0
- Negative net contributions extend upward from their negative value

**Algorithm for Bar Positioning**:
```python
net = pos_val - neg_val
if net >= 0:
    z_base = 0
    dz = net
else:
    z_base = net
    dz = -net
```

**Interpretation**: 
- Tall bars indicate strong category influence
- Bars above zero: Category supports the destination
- Bars below zero: Category argues against the destination

---

**Figure Properties**:
- Size: 16×5 inches (wider for three side-by-side plots)
- Title: "3D Systems Statistical Visualization"
- Layout: Tight layout with margin for title (rect=[0, 0.03, 1, 0.92])

---

## Data Structures

### Input State Structure

The `state` dictionary is expected to have the following structure:

```python
state = {
    "trace": [
        "R4_culture_history: User interested in culture...",
        "R7_beach_paradise: User wants relaxation...",
        ...
    ],
    "recommended": {
        "Paris": ["R4_culture_history", "R12_art_museums"],
        "Tokyo": ["R4_culture_history", "R20_tech_innovation"],
        ...
    },
    "not_recommended": {
        "Paris": ["R7_beach_paradise"],
        "Tokyo": ["R7_beach_paradise", "R15_budget_strict"],
        ...
    }
}
```

### Scores Structure

```python
scores = {
    "Paris": 85,
    "Tokyo": 72,
    "Bali": 45,
    ...
}
```

---

## Usage Examples

### Example 1: Basic 2D Visualization

```python
from travel_plot import visualize_statistics

# After running inference
visualize_statistics(state, scores)
```

This will display a window with four charts showing:
1. Bar chart of destination scores
2. Grouped bars comparing positive/negative evidence
3. Line chart of rule firing frequencies
4. Pie chart of category contributions

### Example 2: Advanced 3D Visualization

```python
from travel_plot import visualize_statistics_3d

# After running inference
visualize_statistics_3d(state, scores)
```

This will display a window with three 3D visualizations:
1. Scatter plot showing the relationship between evidence and scores
2. Heat cube showing destination-category activity
3. Bar landscape showing net category contributions

### Example 3: Using Helper Functions

```python
from travel_plot import compute_rule_frequency, compute_category_contributions

# Get rule firing counts
rule_freq = compute_rule_frequency(state)
print(f"Rule R4 fired {rule_freq.get('R4_culture_history', 0)} times")

# Get category contributions
cat_contrib = compute_category_contributions(state)
print(f"Culture category contributed {cat_contrib.get('Culture & History', 0)} rules")
```

---

## Design Patterns

### Separation of Concerns
- **Helper functions**: Focus solely on data processing and aggregation
- **Visualization functions**: Focus solely on rendering and display
- This separation allows reuse of data processing logic

### Consistent Styling
- All charts use default matplotlib styling for consistency
- Titles are descriptive and informative
- Axis labels clearly indicate what is being measured
- Rotated labels prevent overlap and improve readability

### Comprehensive Coverage
- Both 2D and 3D visualizations provided
- Multiple perspectives on the same data
- Statistical, comparative, and relational views

---

## Notes and Best Practices

### Performance Considerations
- The 3D visualizations can be computationally intensive for large datasets
- Consider limiting the number of destinations or categories if performance is an issue

### Customization
To customize chart appearance:
1. Modify figure sizes in `figsize` parameters
2. Adjust colors using matplotlib color parameters
3. Change bar widths, marker styles, or line styles as needed

### Integration
This module is designed to work seamlessly with:
- The inference engine (provides `state` data)
- The scoring system (provides `scores` data)
- The rule system (defines `RULE_CATEGORY` mapping)

---

## Related Files

- [travel_info.py](file:///c:/Users/ibrah/PyCharmMiscProject/Travel-Advisor-Agent/travel_info.py): Contains `DESTINATIONS` and `RULE_CATEGORY` definitions
- Expert system core: Generates the `state` and `scores` data structures

---

## Future Enhancements

Potential improvements for this module:
1. Interactive visualizations using plotly
2. Export functionality to save charts as images
3. Animation showing rule firing sequence
4. Heatmap visualizations for category matrices
5. Customizable color schemes and themes
6. Real-time updating during inference
