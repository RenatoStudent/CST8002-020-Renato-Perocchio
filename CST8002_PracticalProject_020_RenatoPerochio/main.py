from io_handler.csv_handler import load_records
from ui.display import show_records

AUTHOR = "Renato Perocchio"
DIVIDER = "=" * 55

def main():
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