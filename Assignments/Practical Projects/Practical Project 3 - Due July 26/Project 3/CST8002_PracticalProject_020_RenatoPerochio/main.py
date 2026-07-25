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
from presentation.gui import launch

AUTHOR = "Renato Perocchio"


def main():
    manager = RecordManager()
    count = manager.load_from_file()
    print(f"Startup: loaded {count} record(s) from dataset.")

    launch(manager, AUTHOR)


if __name__ == "__main__":
    main()