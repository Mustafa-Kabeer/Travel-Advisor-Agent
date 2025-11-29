"""
AI Travel Destination Planner - Tkinter GUI
=============================================
Modern Form-based GUI for the travel advisor agent.
Features:
- Tab-based workflow (Form -> Results -> Charts)
- Grouped input sections
- Embedded Matplotlib plots
- Rich text formatting
- Responsive layout
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Import the logic functions from the main file
from ai_travel_destination_planner_agent_main import (
    build_destination_facts,
    run_inference,
    compute_scores,
    build_explanations,
    compute_rule_frequency,
    compute_category_contributions,
    visualize_statistics_3d,
    compute_dest_category_matrices,
)

# Import static data from travel_info module
from travel_info import (
    TRAVEL_TIPS,
    DESTINATIONS,
)


class TravelPlannerGUI(tk.Tk):
    """
    Modern Form-based GUI for the Travel Planner.
    """

    def __init__(self):
        super().__init__()

        # Window setup
        self.title("AI Travel Destination Planner")
        self.geometry("1100x850")

        # Make main window responsive
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Configure styles
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Custom fonts and colors
        self.style.configure("TLabel", font=("Segoe UI", 10))
        self.style.configure("TButton", font=("Segoe UI", 11, "bold"), padding=10)
        self.style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"), foreground="#2c3e50")
        self.style.configure("Section.TLabelframe.Label", font=("Segoe UI", 11, "bold"), foreground="#2980b9")

        # Store inference results
        self.state = None
        self.scores = None

        # Build destination facts once
        self.dest_facts = build_destination_facts()

        # Main Layout: Notebook (Tabs)
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Create Tabs
        self.tab_form = ttk.Frame(self.notebook)
        self.tab_results = ttk.Frame(self.notebook)
        self.tab_charts = ttk.Frame(self.notebook)
        self.tab_reasoning = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_form, text="  Plan Your Trip  ")
        self.notebook.add(self.tab_results, text="  Recommendations  ")
        self.notebook.add(self.tab_charts, text="  Visualizations  ")
        self.notebook.add(self.tab_reasoning, text="  Reasoning Logic  ")

        # Initialize Components
        self.create_form_tab()
        self.create_results_tab()
        self.create_charts_tab()
        self.create_reasoning_tab()

    def create_form_tab(self):
        """
        Create the input form with grouped sections.
        """
        # Make tab responsive
        self.tab_form.columnconfigure(0, weight=1)
        self.tab_form.rowconfigure(0, weight=1)

        # Scrollable container for the form
        canvas = tk.Canvas(self.tab_form, borderwidth=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.tab_form, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Center the scrollable frame in the canvas
        def on_canvas_configure(event):
            canvas.itemconfig(window_id, width=event.width)

        canvas.bind("<Configure>", on_canvas_configure)
        window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="n")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Layout canvas and scrollbar
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Center container frame to hold the content
        center_frame = ttk.Frame(scrollable_frame)
        center_frame.pack(pady=20, padx=50, fill="x", expand=True)

        # Title
        ttk.Label(center_frame, text="Plan Your Dream Trip", style="Header.TLabel").pack(pady=(0, 20))

        # --- Section 1: Trip Details ---
        frame_details = ttk.LabelFrame(center_frame, text="Trip Details", style="Section.TLabelframe", padding=15)
        frame_details.pack(fill="x", pady=10)

        # Configure columns for responsiveness
        frame_details.columnconfigure(0, weight=1)
        frame_details.columnconfigure(1, weight=1)

        self.budget_var = self.create_combo(frame_details, "Budget Level:", ["low", "medium", "high"], "medium", 0, 0)
        self.season_var = self.create_combo(frame_details, "Preferred Season:", ["spring", "summer", "autumn", "winter"], "spring", 0, 1)
        self.duration_var = self.create_combo(frame_details, "Trip Duration:", ["short", "medium", "long"], "medium", 1, 0)
        self.companions_var = self.create_combo(frame_details, "Companions:", ["solo", "dual", "family"], "solo", 1, 1)

        # --- Section 2: Interests (Checkboxes) ---
        frame_interests = ttk.LabelFrame(center_frame, text="Interests & Activities", style="Section.TLabelframe", padding=15)
        frame_interests.pack(fill="x", pady=10)

        ttk.Label(frame_interests, text="Select all that apply:").pack(anchor="w", pady=(0, 10))

        checkbox_frame = ttk.Frame(frame_interests)
        checkbox_frame.pack(fill="x")

        self.exp_vars = {
            "nature_scenery": tk.BooleanVar(),
            "culture_history": tk.BooleanVar(),
            "city_life": tk.BooleanVar(),
            "shopping": tk.BooleanVar(),
            "adventure": tk.BooleanVar()
        }

        col = 0
        for key, var in self.exp_vars.items():
            label = key.replace("_", " ").title()
            ttk.Checkbutton(checkbox_frame, text=label, variable=var).grid(row=0, column=col, padx=15, sticky="w")
            checkbox_frame.columnconfigure(col, weight=1)
            col += 1

        # --- Section 3: Preferences ---
        frame_prefs = ttk.LabelFrame(center_frame, text="Travel Preferences", style="Section.TLabelframe", padding=15)
        frame_prefs.pack(fill="x", pady=10)

        frame_prefs.columnconfigure(0, weight=1)
        frame_prefs.columnconfigure(1, weight=1)

        self.crowd_var = self.create_combo(frame_prefs, "Crowd Tolerance:", ["likes_lively", "prefers_quiet"], "prefers_quiet", 0, 0)
        self.climate_var = self.create_combo(frame_prefs, "Climate:", ["cool", "mild", "warm"], "mild", 0, 1)
        self.transport_var = self.create_combo(frame_prefs, "Transport:", ["public_transport", "walking", "car_taxi"], "public_transport", 1, 0)
        self.traffic_var = self.create_combo(frame_prefs, "Traffic Sensitivity:", ["low_traffic", "mid_traffic", "high_traffic"], "low_traffic", 1, 1)
        self.food_var = self.create_combo(frame_prefs, "Food Preference:", ["LovesLocalCuisine", "PrefersFamiliarFood"], "LovesLocalCuisine", 2, 0)
        self.safety_var = self.create_combo(frame_prefs, "Safety Priority:", ["HighSafety", "MediumSafety", "LowSafetyConcern"], "HighSafety", 2, 1)

        # --- Action Button ---
        run_btn = ttk.Button(center_frame, text="Find My Destination  ➔", command=self.run_planner, cursor="hand2")
        run_btn.pack(pady=30, ipadx=20, ipady=5)

    def create_combo(self, parent, label_text, values, default, row, col):
        """Helper to create a label + combobox pair."""
        frame = ttk.Frame(parent)
        frame.grid(row=row, column=col, sticky="ew", padx=10, pady=5)

        ttk.Label(frame, text=label_text, font=("Segoe UI", 9, "bold")).pack(anchor="w")
        var = tk.StringVar(value=default)
        combo = ttk.Combobox(frame, textvariable=var, values=values, state="readonly")
        combo.pack(fill="x", pady=(2, 0))
        return var

    def create_results_tab(self):
        """
        Create rich text area for results.
        """
        self.tab_results.columnconfigure(0, weight=1)
        self.tab_results.rowconfigure(0, weight=1)

        self.results_text = scrolledtext.ScrolledText(self.tab_results, wrap="word", font=("Segoe UI", 10), padx=30, pady=30)
        self.results_text.grid(row=0, column=0, sticky="nsew")

        # Configure Tags
        self.results_text.tag_config("header", font=("Segoe UI", 18, "bold"), foreground="#2980b9", spacing3=15)
        self.results_text.tag_config("subheader", font=("Segoe UI", 14, "bold"), foreground="#2c3e50", spacing1=10)
        self.results_text.tag_config("score", font=("Segoe UI", 12, "bold"), foreground="#27ae60")
        self.results_text.tag_config("good", foreground="#27ae60")
        self.results_text.tag_config("bad", foreground="#c0392b")
        self.results_text.tag_config("tip", font=("Segoe UI", 10, "italic"), foreground="#8e44ad")
        self.results_text.tag_config("label_strong", background="#27ae60", foreground="white")
        self.results_text.tag_config("label_warn", background="#f39c12", foreground="white")
        self.results_text.tag_config("label_bad", background="#c0392b", foreground="white")

        self.results_text.insert(tk.END, "\n\nPlease fill out the form in the 'Plan Your Trip' tab and click 'Find My Destination'.")

    def create_charts_tab(self):
        """
        Setup the matplotlib canvas area.
        """
        self.tab_charts.columnconfigure(0, weight=1)
        self.tab_charts.rowconfigure(0, weight=1)

        self.figure = plt.Figure(figsize=(8, 8), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, self.tab_charts)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.ax_msg = self.figure.add_subplot(111)
        self.ax_msg.text(0.5, 0.5, "Run Planner to see statistics", ha='center', va='center')
        self.ax_msg.axis('off')

        # Button row for extra actions (e.g., 3D view)
        btn_frame = ttk.Frame(self.tab_charts)
        btn_frame.grid(row=1, column=0, sticky="e", padx=10, pady=(0, 10))

        ttk.Button(
            btn_frame,
            text="Open 3D View",
            command=self.open_3d_view,
            cursor="hand2"
        ).pack(side="right")


    def create_reasoning_tab(self):
        """
        Create text area for reasoning trace.
        """
        self.tab_reasoning.columnconfigure(0, weight=1)
        self.tab_reasoning.rowconfigure(0, weight=1)

        self.reasoning_text = scrolledtext.ScrolledText(self.tab_reasoning, wrap="word", font=("Consolas", 10), padx=20, pady=20)
        self.reasoning_text.grid(row=0, column=0, sticky="nsew")

        # Tags for formatting
        self.reasoning_text.tag_config("rule_name", foreground="#d35400", font=("Consolas", 10, "bold"))
        self.reasoning_text.tag_config("logic", foreground="#2c3e50")

        self.reasoning_text.insert(tk.END, "Run the planner to see the logic trace here.")

    def run_planner(self):
        """
        Execute inference and update UI.
        """
        # 1. Validate Inputs
        likes = [k for k, v in self.exp_vars.items() if v.get()]
        # if not likes:
        #     messagebox.showerror("Input Error", "Please select at least one Experience Type.")
        #     return

        # 2. Build User Profile
        user = {
            "budget": self.budget_var.get(),
            "prefers_season": self.season_var.get(),
            "trip_duration": self.duration_var.get(),
            "likes": likes,
            "crowd_tolerance": self.crowd_var.get(),
            "climate_preference": self.climate_var.get(),
            "transport": self.transport_var.get(),
            "traffic_preference": self.traffic_var.get(),
            "food_preference": self.food_var.get(),
            "safety_priority": self.safety_var.get(),
            "companions": self.companions_var.get(),
        }

        # 3. Run Inference
        self.state = run_inference(user, self.dest_facts)
        self.scores = compute_scores(self.state)
        explanations = build_explanations(self.state)
        ranked = sorted(DESTINATIONS, key=lambda d: self.scores[d], reverse=True)

        # 4. Update Results Tab
        self.update_results_text(ranked, explanations)

        # 5. Update Charts Tab
        self.update_charts()

        # 6. Update Reasoning Tab
        self.update_reasoning_tab()

        # 7. Auto-switch to Results Tab
        self.notebook.select(self.tab_results)

    def update_reasoning_tab(self):
        """
        Populate the reasoning tab with the trace log.
        """
        self.reasoning_text.config(state="normal") # Enable to write
        self.reasoning_text.delete(1.0, tk.END)
        self.reasoning_text.insert(tk.END, "Inference Engine Trace:\n\n", "header")

        trace = self.state.get("trace", [])
        for line in trace:
            # Try to split by first colon to separate Rule Name
            if ":" in line:
                rule_name, logic = line.split(":", 1)
                self.reasoning_text.insert(tk.END, rule_name + ":", "rule_name")
                self.reasoning_text.insert(tk.END, logic + "\n", "logic")
            else:
                self.reasoning_text.insert(tk.END, line + "\n", "logic")

        self.reasoning_text.config(state="disabled") # Disable to prevent editing

    def update_results_text(self, ranked, explanations):
        """
        Render formatted results.
        """
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "Your Travel Recommendations\n", "header")

        for d in ranked:
            score = self.scores[d]
            self.results_text.insert(tk.END, f"\n{d} ", "subheader")
            self.results_text.insert(tk.END, f"(Score: {score})\n", "score")

            # Status Labels
            if d in self.state["strongly_recommended"]:
                self.results_text.insert(tk.END, " STRONGLY RECOMMENDED ", "label_strong")
                self.results_text.insert(tk.END, " ")
            if d in self.state["not_recommended"]:
                self.results_text.insert(tk.END, " HAS WARNINGS ", "label_warn")
                self.results_text.insert(tk.END, " ")
            if d in self.state["strongly_not_recommended"]:
                self.results_text.insert(tk.END, " NOT RECOMMENDED ", "label_bad")
                self.results_text.insert(tk.END, " ")

            self.results_text.insert(tk.END, "\n")

            # Positives
            pos = explanations[d]["positives"]
            if pos:
                self.results_text.insert(tk.END, "  Why it's a match:\n", "good")
                for p in pos:
                    self.results_text.insert(tk.END, f"   • {p}\n")

            # Negatives
            neg = explanations[d]["negatives"]
            if neg:
                self.results_text.insert(tk.END, "  Concerns:\n", "bad")
                for n in neg:
                    self.results_text.insert(tk.END, f"   • {n}\n")

            self.results_text.insert(tk.END, "_"*60 + "\n")

        # Travel Tips
        if self.state["final_recommendation"]:
            top_dests = self.state["final_recommendation"]
        else:
            top_dests = [ranked[0]]

        self.results_text.insert(tk.END, "\nTravel Tips for Top Picks\n", "header")
        for d in top_dests:
            self.results_text.insert(tk.END, f"\n{d}:\n", "subheader")
            tips = TRAVEL_TIPS.get(d, [])
            for tip in tips:
                self.results_text.insert(tk.END, f"  💡 {tip}\n", "tip")

    def update_charts(self):
        """
        Draw matplotlib charts with better layout.
        """
        self.figure.clear()

        # Data Preparation
        destinations = DESTINATIONS
        score_values = [self.scores[d] for d in destinations]
        pos_counts = [len(self.state["recommended"][d]) for d in destinations]
        neg_counts = [len(self.state["not_recommended"][d]) for d in destinations]

        rule_freq = compute_rule_frequency(self.state)
        rules = sorted(rule_freq.keys())
        rule_values = [rule_freq[r] for r in rules]

        cat_counts = compute_category_contributions(self.state)
        categories = list(cat_counts.keys())
        cat_values = [cat_counts[c] for c in categories]

        # Create Subplots (2x2)
        axs = self.figure.subplots(2, 2)

        # Adjust spacing:
        # bottom=0.35: Space for rule names
        # wspace=0.2: Reduced horizontal space to let charts expand
        # hspace=0.6: Vertical space
        self.figure.subplots_adjust(left=0.08, right=0.95, top=0.92, bottom=0.35, hspace=0.6, wspace=0.2)

        # 1. Scores
        ax1 = axs[0, 0]
        ax1.bar(destinations, score_values, color='#3498db')
        ax1.set_title("Destination Scores", fontsize=10)
        ax1.tick_params(axis='x', rotation=45, labelsize=8)

        # 2. Pos vs Neg
        ax2 = axs[0, 1]
        x = range(len(destinations))
        width = 0.35
        ax2.bar([i - width/2 for i in x], pos_counts, width, label='Pos', color='#2ecc71')
        ax2.bar([i + width/2 for i in x], neg_counts, width, label='Neg', color='#e74c3c')
        ax2.set_xticks(list(x))
        ax2.set_xticklabels(destinations, rotation=45, fontsize=8)
        ax2.set_title("Evidence Count", fontsize=10)
        ax2.legend(fontsize=8)

        # 3. Rule Activity
        ax3 = axs[1, 0]
        ax3.plot(rules, rule_values, marker='o', color='#9b59b6')
        ax3.set_title("Rule Activity", fontsize=10)
        ax3.tick_params(axis='x', rotation=90, labelsize=7)

        # 4. Decision Factors (Pie Chart)
        ax4 = axs[1, 1]
        # radius=1.2: Make it bigger (default is 1.0)
        # pctdistance=0.8: Move % closer to center
        # labeldistance=1.15: Move labels slightly out
        ax4.pie(cat_values, labels=categories, autopct='%1.1f%%', startangle=90,
                textprops={'fontsize': 9}, radius=1.2, pctdistance=0.8, labeldistance=1.15)
        ax4.set_title("Decision Factors", fontsize=10, pad=20) # Add padding to title to avoid overlap

        self.canvas.draw()

    def open_3d_view(self):
        """
        Open a new Tkinter window containing 3D visualizations
        (scatter, heat cube, and bar landscape) using the current
        state and scores from the reasoning engine.
        """
        if self.state is None or self.scores is None:
            messagebox.showinfo(
                "3D Visualization",
                "Please run the planner first to generate data."
            )
            return

        # Prepare data from the existing state
        destinations = DESTINATIONS
        pos_counts = [len(self.state["recommended"][d]) for d in destinations]
        neg_counts = [len(self.state["not_recommended"][d]) for d in destinations]
        score_values = [self.scores[d] for d in destinations]

        # Destination-category matrices (for heat cube and bar landscape)
        categories, pos_matrix, neg_matrix = compute_dest_category_matrices(self.state)

        # Create a new top-level window
        win = tk.Toplevel(self)
        win.title("3D Systems Statistical Visualization")
        win.geometry("1100x600")

        # Create a new Matplotlib figure inside the Toplevel
        fig = plt.Figure(figsize=(12, 4), dpi=100)
        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.get_tk_widget().pack(fill="both", expand=True)

        # Indices for tick labels
        dest_indices = range(len(destinations))
        cat_indices = range(len(categories))

        # ==================================
        # 1) 3D Scatter: Positives vs Negatives vs Score
        # ==================================
        ax1 = fig.add_subplot(1, 3, 1, projection='3d')
        xs = pos_counts
        ys = neg_counts
        zs = score_values

        ax1.scatter(xs, ys, zs)

        for i, d in enumerate(destinations):
            ax1.text(xs[i], ys[i], zs[i], d)

        ax1.set_title("Positives vs Negatives vs Score", fontsize=9)
        ax1.set_xlabel("Positive rules")
        ax1.set_ylabel("Negative rules")
        ax1.set_zlabel("Score")

        # ==================================
        # 2) 3D Heat Cube: Dest × Category × Intensity
        # ==================================
        ax2 = fig.add_subplot(1, 3, 2, projection='3d')
        heat_x = []
        heat_y = []
        heat_z = []

        for i, d in enumerate(destinations):
            for j, c in enumerate(categories):
                total = pos_matrix[d].get(c, 0) + neg_matrix[d].get(c, 0)
                heat_x.append(i)
                heat_y.append(j)
                heat_z.append(total)

        ax2.scatter(heat_x, heat_y, heat_z)
        ax2.set_title("Dest × Category × Intensity", fontsize=9)
        ax2.set_xlabel("Destination")
        ax2.set_ylabel("Category")
        ax2.set_zlabel("Total rules")

        ax2.set_xticks(list(dest_indices))
        ax2.set_xticklabels(destinations, rotation=45, ha="right", fontsize=7)
        ax2.set_yticks(list(cat_indices))
        ax2.set_yticklabels(categories, rotation=45, ha="right", fontsize=7)

        # ==================================
        # 3) 3D Bar Landscape: Category Contribution Terrain
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
                net = pos_val - neg_val

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
        ax3.set_title("Category Contribution Terrain", fontsize=9)
        ax3.set_xlabel("Destination")
        ax3.set_ylabel("Category")
        ax3.set_zlabel("Net (pos - neg)")

        ax3.set_xticks(list(dest_indices))
        ax3.set_xticklabels(destinations, rotation=45, ha="right", fontsize=7)
        ax3.set_yticks(list(cat_indices))
        ax3.set_yticklabels(categories, rotation=45, ha="right", fontsize=7)

        fig.tight_layout()
        canvas.draw()




def main():
    app = TravelPlannerGUI()
    app.mainloop()

if __name__ == "__main__":
    main()
