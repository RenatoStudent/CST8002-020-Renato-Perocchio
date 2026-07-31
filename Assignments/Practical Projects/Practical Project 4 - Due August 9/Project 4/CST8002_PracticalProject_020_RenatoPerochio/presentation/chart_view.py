# ============================================================
# Course:      CST8002 - Programming Language Research Project
# Professor:   Daniel Cormier
# Due Date:    August 9, 2026
# Author:      Renato Perocchio
# References:
#   [1] Matplotlib Development Team. (2026). Embedding in Tk.
#       matplotlib.org. [online] Available at:
#       https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_tk_sgskip.html
#       [Accessed on Jul 30, 2026]
#
#   [2] Data to Fish. (2024). How to Place Matplotlib Charts on a tkinter GUI.
#       datatofish.com. [online] Available at: https://www.datatofish.com/matplotlib-charts-tkinter-gui/
#       [Accessed on Jul 30, 2026]
#
#   [3] Real Python. (2024). Python Plotting With Matplotlib (Guide). realpython.com. [online] Available at:
#       https://realpython.com/python-matplotlib-guide/ [Accessed on Jul 30, 2026]
# ============================================================

"""
Presentation layer helper: builds a matplotlib chart (bar or pie) from
already-aggregated counts and embeds it inside a Tkinter widget. Contains
no data-aggregation logic (that lives in RecordManager.count_by_column)
and no dialog/window management (that lives in gui.py's ChartDialog).
"""

import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

CHART_TYPES = ["Bar Chart", "Pie Chart"]

def build_chart(parent, counts, column_label, chart_type):
    """
    Creates a matplotlib Figure showing the given counts as a bar or pie
    chart and embeds it inside the given Tkinter parent widget.

    Args:
        parent (tk.Widget): The Tkinter container to draw the chart into.
        counts (dict): Maps each distinct column value to its record count.
        column_label (str): Display label of the charted column, used in
            the chart title and axis label.
        chart_type (str): One of the values in CHART_TYPES.

    Returns:
        FigureCanvasTkAgg: The embedded canvas widget, already packed
            into parent.
    """
    figure = Figure(figsize=(6, 4.5), dpi=100)
    axes = figure.add_subplot(111)

    labels = list(counts.keys())
    values = list(counts.values())

    if chart_type == "Pie Chart":
        axes.pie(values, labels=labels, autopct="%1.0f%%")
        axes.set_title(f"Record Count by {column_label}")
    else:
        bars = axes.bar(labels, values, color="steelblue")
        axes.bar_label(bars)
        axes.set_title(f"Record Count by {column_label}")
        axes.set_xlabel(column_label)
        axes.set_ylabel("Count")
        figure.autofmt_xdate(rotation=45)

    canvas = FigureCanvasTkAgg(figure, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    return canvas