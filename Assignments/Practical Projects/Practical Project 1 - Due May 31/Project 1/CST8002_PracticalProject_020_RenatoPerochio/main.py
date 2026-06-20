# ============================================================
# Course:      CST8002 - Programming Language Research Project
# Professor:   Stanley Pieda
# Due Date:    June 21, 2026
# Author:      Renato Perocchio
# References:
#   [1] Python Software Foundation. (2024). Classes. docs.python.org.
#       [online] Available at: https://docs.python.org/3/tutorial/classes.html
#       [Accessed on June 19, 2026]

#   [2] Python Software Foundation. (2024). Input and Output. docs.python.org.
#       [online] Available at: https://docs.python.org/3/tutorial/inputoutput.html
#       [Accessed on June 19, 2026]
# ============================================================

"""
Entry point for CST8002 Practical Project 2.
Wires together the business and presentation layers, loads the dataset
on startup, then hands control to the interactive menu.
"""

from business.record_manager import RecordManager
from presentation.menu import Menu

AUTHOR = "Renato Perocchio"


def main():
    """
    Initializes the business layer, loads data from the CSV on startup,
    and launches the interactive menu.
    """
    manager = RecordManager()
    count = manager.load_from_file()
    print(f"\n  Startup: loaded {count} record(s) from dataset.")

    menu = Menu(manager, AUTHOR)
    menu.run()


if __name__ == "__main__":
    main()
