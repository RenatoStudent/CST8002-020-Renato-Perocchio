# ============================================================
# Course:      CST8002 - Programming Language Research Project
# Professor:   Daniel Cormier
# Due Date:    July 26, 2026
# Author:      Renato Perocchio
# References:
#   [1] Python Software Foundation. (2024). tkinter — Python interface to Tcl/Tk.
#       docs.python.org. [online] Available at: https://docs.python.org/3/library/tkinter.html
#       [Accessed on Jul 24, 2026]
#   [2] Python Software Foundation. (2024). tkinter.ttk — Tk themed widgets.
#       docs.python.org. [online] Available at: https://docs.python.org/3/library/tkinter.ttk.html
#       [Accessed on Jul 24, 2026]
#   [3] Python Software Foundation. (2024). tkinter.messagebox — Tkinter message prompts.
#       docs.python.org. [online] Available at: https://docs.python.org/3/library/tkinter.messagebox.html
#       [Accessed on Jul 24, 2026]
# ============================================================

"""
Presentation layer: Tkinter graphical user interface for CST8002 Practical
Project 3. Replaces the console menu from Practical Project 2 with a windowed
GUI. All create, read, update, delete, reload, and save operations are
delegated to the existing RecordManager business-layer object; no business
or persistence code is modified.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from model.prey_record import PreyRecord
from presentation.chart_view import build_chart, CHART_TYPES

RECORD_FIELDS = [
    ("year",                 "Year"),
    ("species",              "Species"),
    ("common_name",          "Common Name"),
    ("study_site",           "Study Site"),
    ("associated_community", "Associated Community"),
    ("lat",                  "Lat"),
    ("long",                 "Long"),
    ("delta13C",             "delta13C"),
    ("delta13Cc",            "delta13Cc"),
    ("delta15N",             "delta15N"),
    ("delta15Nc",            "delta15Nc"),
    ("tp",                   "TP"),
    ("cn",                   "C:N"),
    ("astaxanthin",          "Astaxanthin (mg/kg)"),
    ("canthaxanthin",        "Canthaxanthin (mg/kg)"),
    ("retinol",              "Retinol (mg/kg)"),
]

'''A subset of the above fields to display in the main table; all fields are shown in the record dialog.'''
COLUMN_FIELDS = ["year", "species", "common_name", "study_site", "lat", "long"]

# Fields with a manageable number of repeating values, suitable for
# grouping into a bar or pie chart. Numeric measurement columns (delta13C,
# tp, astaxanthin, etc.) are excluded since nearly every value is unique.
CHARTABLE_FIELDS = ["year", "species", "common_name", "study_site", "associated_community"]


class RecordDialog(tk.Toplevel):
    """
    Modal dialog window used for creating, editing, or viewing a record.
    Builds one labeled entry field per dataset column. In readonly mode,
    fields are disabled and only a Close button is shown.
    """

    def __init__(self, parent, title, existing=None, readonly=False):
        """
        Builds the dialog's entry fields and buttons.

        Args:
            parent (tk.Tk): The main application window.
            title (str): Window title, e.g. "New Record" or "Edit Record".
            existing (PreyRecord, optional): Record to pre-fill fields from, or
                None to start with blank fields.
            readonly (bool): If True, fields cannot be edited and only a
                Close button is shown (used for "View" mode).
        """
        super().__init__(parent)
        self.title(title)               # Pulls the title text passed in from the calling button.
        self.resizable(False, False)    # Makes the window non-resizable.
        self.transient(parent)          # Makes the dialog appear on top of the parent window.
        self.grab_set()                 # Prevents interaction with the parent window until the dialog is closed.

        self.result = None
        self._entries = {}

        # The frame below holds the form contents; sticky="nsew" makes the
        # form take up all available space in the dialog window.
        form = ttk.Frame(self, padding=12)
        form.grid(row=0, column=0, sticky="nsew")

        for row, (attr, label) in enumerate(RECORD_FIELDS):
            # row=row stacks each label below the last as enumerate counts up;
            # column=0 lines every row up at the same grid position.
            # sticky="e" means "stick to the east", right-aligning the label
            # text against the entry field beside it.
            ttk.Label(form, text=label + ":").grid(row=row, column=0, sticky="e", pady=2, padx=(0, 8))
            entry = ttk.Entry(form, width=40)       # Sets the width of the entry field to 40 characters.
            entry.grid(row=row, column=1, pady=2)   # Places the entry field in the second column of the grid.
            if existing is not None:
                entry.insert(0, getattr(existing, attr))       # If an existing record was passed in, pre-fill this field.
            if readonly:
                entry.configure(state="readonly")               # In View mode, lock the field that now holds existing data.
            self._entries[attr] = entry

        button_row = len(RECORD_FIELDS)
        button_frame = ttk.Frame(form)
        button_frame.grid(row=button_row, column=0, columnspan=2, pady=(12, 0))

        if readonly:
            ttk.Button(button_frame, text="Close", command=self.destroy).pack(side="left", padx=4)
        else:
            ttk.Button(button_frame, text="Save", command=self._on_save).pack(side="left", padx=4)
            ttk.Button(button_frame, text="Cancel", command=self.destroy).pack(side="left", padx=4)

        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def _on_save(self):
        """Validates that no field was left blank, then builds a PreyRecord and closes."""
        values = {}
        for attr, label in RECORD_FIELDS:
            value = self._entries[attr].get().strip()
            if not value:
                messagebox.showerror("Missing Value", f"'{label}' cannot be blank.", parent=self)
                return
            values[attr] = value
        self.result = PreyRecord(**values)
        self.destroy()

class ChartDialog(tk.Toplevel):
    """
    Modal dialog that lets the user pick a dataset column and a chart
    type, then displays a matplotlib chart of record counts for that
    column. Delegates counting to RecordManager and drawing to
    chart_view.build_chart; this class only wires the two together with
    Tkinter controls.
    """

    def __init__(self, parent, manager, author):
        """
        Builds the chart dialog's controls and draws an initial chart.

        Args:
            parent (tk.Tk): The main application window.
            manager (RecordManager): Business layer object used to
                aggregate counts.
            author (str): Author's full name, shown in this window too so
                it remains visible while the dialog is open.
        """
        super().__init__(parent)
        self.title("Chart Records")
        self.geometry("650x600")
        self.transient(parent)

        self._manager = manager
        self._canvas_widget = None
        self._field_labels = {attr: label for attr, label in RECORD_FIELDS}

        controls = ttk.Frame(self, padding=10)
        controls.pack(side="top", fill="x")

        ttk.Label(controls, text="Column:").pack(side="left")
        self._column_var = tk.StringVar(value=CHARTABLE_FIELDS[0])
        ttk.Combobox(
            controls, textvariable=self._column_var, state="readonly",
            values=CHARTABLE_FIELDS, width=20
        ).pack(side="left", padx=(4, 12))

        ttk.Label(controls, text="Chart Type:").pack(side="left")
        self._chart_type_var = tk.StringVar(value=CHART_TYPES[0])
        ttk.Combobox(
            controls, textvariable=self._chart_type_var, state="readonly",
            values=CHART_TYPES, width=12
        ).pack(side="left", padx=4)

        ttk.Button(controls, text="Generate Chart", command=self._generate).pack(side="left", padx=12)

        self._chart_frame = ttk.Frame(self)
        self._chart_frame.pack(side="top", fill="both", expand=True)

        ttk.Label(
            self, text=f"Program by {author}", anchor="w", relief="sunken", padding=6
        ).pack(side="bottom", fill="x")

        self._generate()

    def _generate(self):
        """Aggregates the selected column via RecordManager and (re)draws the chart."""
        if self._canvas_widget is not None:
            self._canvas_widget.get_tk_widget().destroy()

        attr = self._column_var.get()
        counts = self._manager.count_by_column(attr)
        self._canvas_widget = build_chart(
            self._chart_frame, counts, self._field_labels[attr], self._chart_type_var.get()
        )

class PreyRecordApp(tk.Tk):
    """
    Main application window. Presentation-layer class for the Tkinter GUI.
    Talks only to the RecordManager (business layer); contains no file I/O
    or data-structure logic of its own.
    """

    def __init__(self, manager, author):
        """
        Builds the main window: toolbar, record table, and status bar.

        Args:
            manager (RecordManager): Business layer object providing CRUD operations.
            author (str): Author's full name, shown at all times in the title bar
                and status bar so it always remains visible.
        """
        super().__init__()
        self._manager = manager
        self._author = author

        self.title(f"CST8002 Practical Project 3 - Program by {self._author}")
        self.geometry("900x520")
        self.minsize(780, 420)

        self._build_toolbar()
        self._build_table()
        self._build_status_bar()

        self._refresh_table()

    # ── layout builders ──────────────────────────────────────────────────

    def _build_toolbar(self):
        """Creates the row of action buttons across the top of the window."""
        toolbar = ttk.Frame(self, padding=8)
        toolbar.pack(side="top", fill="x")

        ttk.Button(toolbar, text="Reload from File", command=self._reload).pack(side="left", padx=4)
        ttk.Button(toolbar, text="Save (New UUID File)", command=self._save).pack(side="left", padx=4)
        ttk.Button(toolbar, text="New Record", command=self._create).pack(side="left", padx=4)
        ttk.Button(toolbar, text="View Selected", command=self._view_selected).pack(side="left", padx=4)
        ttk.Button(toolbar, text="Edit Selected", command=self._edit_selected).pack(side="left", padx=4)
        ttk.Button(toolbar, text="Delete Selected", command=self._delete_selected).pack(side="left", padx=4)
        #Added for Practical Project 4: Chart Records button to open the chart dialog
        ttk.Button(toolbar, text="Chart Records", command=self._chart).pack(side="left", padx=4)

    def _build_table(self):
        """Creates the scrollable Treeview widget that lists all in-memory records."""
        container = ttk.Frame(self, padding=(8, 0, 8, 8))
        container.pack(side="top", fill="both", expand=True)

        columns = [attr for attr, _ in RECORD_FIELDS if attr in COLUMN_FIELDS]
        self._table = ttk.Treeview(container, columns=columns, show="headings", selectmode="browse")

        headings = {attr: label for attr, label in RECORD_FIELDS}
        for attr in columns:
            self._table.heading(attr, text=headings[attr])
            self._table.column(attr, width=130, anchor="w")

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self._table.yview)
        self._table.configure(yscrollcommand=scrollbar.set)

        self._table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self._table.bind("<Double-1>", lambda event: self._view_selected())

    def _build_status_bar(self):
        """Creates the bottom status bar that always shows the author name and record count."""
        self._status = tk.StringVar()
        status_bar = ttk.Label(self, textvariable=self._status, anchor="w", relief="sunken", padding=6)
        status_bar.pack(side="bottom", fill="x")
        self._update_status()

    # ── helpers ─────────────────────────────────────────────────────────────

    def _update_status(self):
        """Refreshes the status bar text with the current record count and author name."""
        self._status.set(f"Records in memory: {self._manager.count()}    |    Program by {self._author}")

    def _refresh_table(self):
        """Clears and repopulates the Treeview from the RecordManager's current records."""
        self._table.delete(*self._table.get_children())
        columns = [attr for attr, _ in RECORD_FIELDS if attr in COLUMN_FIELDS]
        for index, record in enumerate(self._manager.get_all_records()):
            values = [getattr(record, attr) for attr in columns]
            self._table.insert("", "end", iid=str(index), values=values)
        self._update_status()

    # ── button handlers ────────────────────────────────────────────────────

    def _reload(self):
        """Reloads records from the CSV dataset, replacing all in-memory data."""
        count = self._manager.load_from_file()
        self._refresh_table()
        messagebox.showinfo("Reload Complete", f"Loaded {count} record(s) from the dataset.")

    def _save(self):
        """Saves all in-memory records to a new UUID-named CSV file."""
        filename = self._manager.save_to_file()
        messagebox.showinfo("Save Complete", f"Records saved to:\n{filename}")

    def _selected_index(self):
        """
        Returns the zero-based record index of the currently selected table row.

        Returns:
            int: The selected record's index, or None if nothing is selected.
        """
        selection = self._table.selection()
        if not selection:
            messagebox.showinfo("No Selection", "Select a record in the table first.")
            return None
        return int(selection[0])

    def _create(self):
        """Opens a blank RecordDialog and adds the resulting record on save."""
        dialog = RecordDialog(self, "New Record")
        self.wait_window(dialog)
        if dialog.result is not None:
            self._manager.add_record(dialog.result)
            self._refresh_table()

    def _view_selected(self):
        """Opens a read-only dialog showing the selected record's values."""
        index = self._selected_index()
        if index is None:
            return
        record = self._manager.get_record(index)
        RecordDialog(self, f"Viewing Record {index + 1}", existing=record, readonly=True)

    def _edit_selected(self):
        """Opens a RecordDialog pre-filled with the selected record, then saves changes."""
        index = self._selected_index()
        if index is None:
            return
        existing = self._manager.get_record(index)
        dialog = RecordDialog(self, f"Edit Record {index + 1}", existing=existing)
        self.wait_window(dialog)
        if dialog.result is not None:
            self._manager.update_record(index, dialog.result)
            self._refresh_table()

    def _delete_selected(self):
        """Confirms with the user, then deletes the selected record."""
        index = self._selected_index()
        if index is None:
            return
        record = self._manager.get_record(index)
        confirm = messagebox.askyesno(
            "Confirm Delete", f"Delete record {index + 1} ({record.species})?"
        )
        if confirm:
            self._manager.delete_record(index)
            self._refresh_table()

    #Added for Practical Project 4
    def _chart(self):
        """Opens the ChartDialog for visualizing record counts by a chosen column."""
        ChartDialog(self, self._manager, self._author)


def launch(manager, author):
    """
    Builds and runs the Tkinter GUI application.

    Args:
        manager (RecordManager): Business layer object providing CRUD operations.
        author (str): Author's full name, shown throughout the GUI.
    """
    app = PreyRecordApp(manager, author)
    app.mainloop()