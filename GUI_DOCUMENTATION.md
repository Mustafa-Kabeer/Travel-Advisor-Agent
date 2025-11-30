# GUI Implementation Overview

This document provides a brief overview of the Graphical User Interface (GUI) for the **AI Travel Destination Planner**.

## 🛠️ Libraries Used

We used Python's standard libraries to keep the project lightweight and easy to run:

*   **`tkinter`**: The standard Python interface to the Tcl/Tk GUI toolkit. Used for windows, buttons, and layout.
*   **`tkinter.ttk`**: Themed Tkinter widgets (like Tabs, Comboboxes) for a modern look.
*   **`matplotlib`**: Used for generating the statistical charts.
*   **`matplotlib.backends.backend_tkagg`**: A specific backend that allows us to embed Matplotlib charts directly inside a Tkinter window.

## 🏗️ Structure

The entire GUI is encapsulated in a single class `TravelPlannerGUI` in `travel_gui.py`.

```python
class TravelPlannerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Travel Destination Planner")
        # ... setup code ...
```

## 🧩 Key Components

### 1. Tabs (Notebook)
We use `ttk.Notebook` to organize the application into logical sections. This keeps the interface clean.

```python
self.notebook = ttk.Notebook(self)
self.notebook.add(self.tab_form, text="Plan Your Trip")
self.notebook.add(self.tab_results, text="Recommendations")
# ...
```

### 2. Input Form
The "Plan Your Trip" tab uses a **Grid Layout** to organize inputs.
*   **Dropdowns**: `ttk.Combobox` for single-choice inputs (e.g., Budget).
*   **Checkboxes**: `ttk.Checkbutton` for multiple-choice interests (e.g., Nature, Shopping).

```python
# Example of creating a dropdown
self.budget_var = self.create_combo(frame, "Budget Level:", ["low", "medium", "high"], ...)
```

### 3. Rich Text Output
The "Recommendations" and "Reasoning" tabs use `scrolledtext.ScrolledText`. We use **Tags** to color-code the output (e.g., green for good matches, red for warnings).

```python
# Configuring a tag for green text
self.results_text.tag_config("good", foreground="#27ae60")

# Inserting text with that tag
self.results_text.insert(tk.END, "Why it's a match:\n", "good")
```

### 4. Embedded Charts
Instead of popping up a separate window, we embed the plots directly using `FigureCanvasTkAgg`.

```python
# Create a standard Matplotlib Figure
self.figure = plt.Figure(figsize=(8, 8), dpi=100)

# Embed it into the Tkinter frame
self.canvas = FigureCanvasTkAgg(self.figure, self.tab_charts)
self.canvas.get_tk_widget().grid(...)
```

## 🚀 How it Works
1.  **User Input**: The user fills out the form widgets.
2.  **Action**: Clicking "Find My Destination" triggers `self.run_planner()`.
3.  **Processing**: The GUI collects the data, calls `travel_core.run_inference()`, and gets the results.
4.  **Display**: The GUI updates the Text widgets and redraws the Matplotlib canvas with the new data.



a table for Tabs navigation with GUI:
| **Tab Name**                           | **Purpose**                                            | **Contents / Functions**                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| -------------------------------------- | ------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1. Travel Form**                     | Collect user preferences                               | • Budget level  <br>• Preferred season  <br>• Trip duration  <br>• Activity preferences (nature, adventure, culture, shopping, city life)  <br>• Crowd tolerance  <br>• Traffic preference (low/mid/high)  <br>• Transport mode (public transport, walking, car/taxi)  <br>• Food preference (local/familiar)  <br>• Safety priority (high/medium/low concern)  <br>• Travel companions (solo, dual, family)  <br>• **Submit button** triggers inference engine                                     |
| **2. Recommendations**                 | Display reasoning results to user                      | • **Final recommended destination(s)**  <br>• Ranked list of all destinations with scores  <br>• Positive reasoning explanations  <br>• Negative evidence explanations  <br>• Season match / weak match indicators  <br>• Strong recommendation indicators  <br>• **Travel Tips section** including:  <br> – Destination-specific guidance  <br> – Cultural etiquette  <br> – Costs  <br> – Transport guidance  <br> – Weather considerations  <br> – **Visa information** (for all 7 destinations) |
| **3. Charts & Analytics**              | Provide visual insights into reasoning                 | • **Systems Statistical Visualization (4 Subplots):**  <br> 1. Destination Score Bar Chart  <br> 2. Positive vs Negative Evidence Chart  <br> 3. Rule Firing Frequency (Line Plot with Dots)  <br> 4. Category Contributions (Pie Chart)  <br><br>• Visualization auto-renders after inference  <br>• **“Open 3D Charts” button** opens additional window                                                                                                                                           |
| **4. 3D Visualization (Popup Window)** | Advanced analysis for presentations or deeper insights | • 3D Scatter Plot (Score vs Positives vs Negatives)  <br>• 3D Heat Cube (Destination × Category × Intensity)  <br>• 3D Category Terrain (3D bar landscape)  <br>• Interactive camera controls                                                                                                                                                                                                                                                                                                       |
| **5. Reasoning Trace**                 | Transparency & explainable-AI output                   | • Full RAW reasoning trace  <br>• Each fired rule listed in order  <br>• Logical meaning                                                                                                                                                                                                                                                                                                                                                                                                            |
