# ============================================================
# Course:      CST8002 - Programming Language Research Project
# Professor:   Stanley Pieda
# Due Date:    May 31, 2026
# Author:      Renato Perocchio
# ============================================================

"""
Starting point for the CST8002 Practical Project 1.
Loads prey collection records from a CSV dataset and displays them to the console.
"""

from io_handler.csv_handler import load_records
from ui.display import show_records

AUTHOR = "Renato Perocchio"
DIVIDER = "=" * 55

def main():
    """
    Main function that runs the program.
    Prints the program header, loads records from the dataset, and displays them on screen.
    """
    print(f"\n{DIVIDER}")
    print(f"  CST8002 Practical Project 1  |  Author: {AUTHOR}")
    print(f"{DIVIDER}")

    records = load_records()

    if records:
        show_records(records, AUTHOR)
    else:
        print(f"No records loaded. Review the dataset file and path.")

if __name__ == "__main__":
    main()