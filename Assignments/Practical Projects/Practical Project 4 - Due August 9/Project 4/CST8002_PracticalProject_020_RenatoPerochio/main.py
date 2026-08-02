# ============================================================
# Course:      CST8002 - Programming Language Research Project
# Professor:   Daniel Cormier
# Due Date:    August 9, 2026
# Author:      Renato Perocchio
# References:
#   [1] Python Software Foundation. (2024). tkinter — Python interface to Tcl/Tk.
#       docs.python.org. [online] Available at: https://docs.python.org/3/library/tkinter.html
#       [Accessed on Jul 24, 2026]
# ============================================================

"""
Entry point for CST8002 Practical Project 4.
Wires together the business layer and the Tkinter presentation layer, loads
the dataset on startup, then launches the GUI.
"""

from business.record_manager import RecordManager
from presentation.gui import launch

# Displayed throughout the GUI (title bar, status bar) so the author's
# name always remains visible while the program runs.
AUTHOR = "Renato Perocchio"


def main():
    """
    Initializes the business layer, loads data from the CSV on startup,
    and launches the Tkinter GUI.
    """
    manager = RecordManager()
    count = manager.load_from_file()
    print(f"Startup: loaded {count} record(s) from dataset.")

    launch(manager, AUTHOR)


if __name__ == "__main__":
    main()