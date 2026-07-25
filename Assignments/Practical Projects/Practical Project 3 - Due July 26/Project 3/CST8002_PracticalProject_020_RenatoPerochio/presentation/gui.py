# ============================================================
# Course:      CST8002 - Programming Language Research Project
# Professor:   Stanley Pieda
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
#
# NOTE: swap these references for whatever tkinter docs/tutorials you actually
# read while building this — the IEEE list must reflect your real sources.

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

COLUMN_FIELDS = ["year", "species", "common_name", "study_site", "lat", "long"]


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

    # ── layout builders ────────────────────────────────────────────────────

    def _build_toolbar(self):
        """Creates the row of action buttons across the top of the window."""
        toolbar = ttk.Frame(self, padding=8)
        toolbar.pack(side="top", fill="x")

        ttk.Button(toolbar, text="Reload from File", command=self._reload).pack(side="left", padx=4)
        ttk.Button(toolbar, text="Save (New UUID File)", command=self._save).pack(side="left", padx=4)

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


def launch(manager, author):
    """
    Builds and runs the Tkinter GUI application.

    Args:
        manager (RecordManager): Business layer object providing CRUD operations.
        author (str): Author's full name, shown throughout the GUI.
    """
    app = PreyRecordApp(manager, author)
    app.mainloop()