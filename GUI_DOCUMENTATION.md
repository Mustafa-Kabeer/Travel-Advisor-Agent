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
