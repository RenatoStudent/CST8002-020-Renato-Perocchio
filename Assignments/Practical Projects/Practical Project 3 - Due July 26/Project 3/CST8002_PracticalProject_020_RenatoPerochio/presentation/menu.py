# ============================================================
# Course:      CST8002 - Programming Language Research Project
# Professor:   Stanley Pieda
# Due Date:    June 21, 2026
# Author:      Renato Perocchio
# References:
#   [1] Python Software Foundation. (2024). Input and Output. docs.python.org.
#       [online] Available at: https://docs.python.org/3/tutorial/inputoutput.html
#       [Accessed on June 19, 2026]
#   [2] Python Software Foundation. (2024). Classes. docs.python.org.
#       [online] Available at: https://docs.python.org/3/tutorial/classes.html
#       [Accessed on June 19, 2026]
# ============================================================

"""
Presentation layer: handles all console user interaction.
Displays menus, collects input, and shows records to the user.
The author name is displayed on every screen so it is always visible.
"""

from model.prey_record import PreyRecord

DIVIDER = "=" * 60

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


class Menu:
    """
    Presentation layer class that drives the interactive console menu.
    All user-facing input and output is handled here.
    """

    def __init__(self, manager, author):
        """
        Initializes the Menu with a RecordManager and the author's name.

        Args:
            manager (RecordManager): The business layer object to call for data operations.
            author (str): The author's full name shown on every screen.
        """
        self._manager = manager
        self._author = author

    def run(self):
        """
        Starts the main menu loop. Continues until the user chooses to quit.
        The author name and current record count are shown before every prompt.
        """
        while True:
            self._print_header()
            self._print_menu()
            choice = input("  Enter choice (1-8): ").strip()

            if choice == "1":
                self._reload()
            elif choice == "2":
                self._save()
            elif choice == "3":
                self._view_all()
            elif choice == "4":
                self._view_one()
            elif choice == "5":
                self._create()
            elif choice == "6":
                self._edit()
            elif choice == "7":
                self._delete()
            elif choice == "8":
                print(f"\n  Goodbye! Program by {self._author}")
                print(DIVIDER)
                break
            else:
                print("  Invalid choice. Please enter a number between 1 and 8.")

    # ── private helpers ────────────────────────────────────────────────────────

    def _print_header(self):
        """Prints the standard header with author name and record count."""
        print(f"\n{DIVIDER}")
        print(f"  CST8002 Practical Project 2  |  Program by {self._author}")
        print(f"  Records in memory: {self._manager.count()}")
        print(DIVIDER)

    def _print_menu(self):
        """Prints the main menu options."""
        print("  1. Reload data from file")
        print("  2. Save data to file  (new UUID filename)")
        print("  3. View all records")
        print("  4. View one record")
        print("  5. Create a new record")
        print("  6. Edit a record")
        print("  7. Delete a record")
        print("  8. Quit")

    def _reload(self):
        """Reloads records from the CSV, replacing all current in-memory data."""
        count = self._manager.load_from_file()
        print(f"\n  Reloaded {count} record(s) from the dataset.")

    def _save(self):
        """Saves all in-memory records to a new UUID-named CSV file."""
        filename = self._manager.save_to_file()
        print(f"\n  File saved: {filename}")

    def _view_all(self):
        """
        Displays every record currently in memory.
        Prints the author name as a sub-header every 10 records so the
        name remains visible throughout long output.
        """
        records = self._manager.get_all_records()
        if not records:
            print("\n  No records in memory. Use option 1 to load the dataset.")
            return

        for i, record in enumerate(records):
            if i % 10 == 0:
                print(f"\n  -- Program by {self._author} --")
            self._print_record(i, record)

        print(f"\n{DIVIDER}")
        print(f"  End of list.  Total: {len(records)} record(s).")
        print(f"  Program by {self._author}")
        print(DIVIDER)

    def _view_one(self):
        """Prompts the user for a record number and displays that single record."""
        index = self._get_index("view")
        if index is None:
            return
        record = self._manager.get_record(index)
        if record:
            print(f"\n  -- Program by {self._author} --")
            self._print_record(index, record)

    def _create(self):
        """Prompts the user to enter all 16 fields and adds the new record to memory."""
        print(f"\n  -- Create New Record | Program by {self._author} --")
        record = self._prompt_record()
        self._manager.add_record(record)
        print(f"\n  Record added. Total records in memory: {self._manager.count()}")

    def _edit(self):
        """
        Prompts the user for a record number, displays current values, then
        lets the user overwrite any field (blank input keeps the current value).
        """
        index = self._get_index("edit")
        if index is None:
            return
        existing = self._manager.get_record(index)
        if existing is None:
            print("  Record not found.")
            return
        print(f"\n  Editing record {index + 1}. Press Enter to keep the current value.")
        print(f"  -- Program by {self._author} --")
        updated_record = self._prompt_record(existing)
        self._manager.update_record(index, updated_record)
        print(f"\n  Record {index + 1} updated successfully.")

    def _delete(self):
        """
        Prompts the user for a record number, asks for confirmation,
        then removes that record from the in-memory list.
        """
        index = self._get_index("delete")
        if index is None:
            return
        record = self._manager.get_record(index)
        if record is None:
            print("  Record not found.")
            return
        confirm = input(
            f"  Delete record {index + 1} ({record.species})? (y/n): "
        ).strip().lower()
        if confirm == "y":
            self._manager.delete_record(index)
            print(f"  Record deleted. Total records in memory: {self._manager.count()}")
        else:
            print("  Delete cancelled.")

    def _get_index(self, action):
        """
        Prompts the user to enter a record number and converts it to a
        zero-based list index.

        Args:
            action (str): Descriptive word for the prompt (e.g. "view", "edit").

        Returns:
            int: Zero-based index, or None if input was invalid or list is empty.
        """
        total = self._manager.count()
        if total == 0:
            print("\n  No records in memory. Use option 1 to load the dataset.")
            return None
        try:
            number = int(input(f"  Enter record number to {action} (1-{total}): "))
            return number - 1
        except ValueError:
            print("  Invalid input. Please enter a whole number.")
            return None

    def _prompt_record(self, existing=None):
        """
        Prompts the user to enter values for all 16 dataset fields.
        If an existing record is provided, the current value is shown in brackets
        and pressing Enter keeps it unchanged.

        Args:
            existing (PreyRecord, optional): The record being edited, or None for a new record.

        Returns:
            PreyRecord: A new PreyRecord built from the user's input.
        """
        values = {}
        for attr, label in RECORD_FIELDS:
            if existing is not None:
                current = getattr(existing, attr)
                entry = input(f"  {label} [{current}]: ").strip()
                values[attr] = entry if entry else current
            else:
                values[attr] = input(f"  {label}: ").strip()

        return PreyRecord(**values)

    def _print_record(self, index, record):
        """
        Prints all 16 fields of a single PreyRecord to the console.

        Args:
            index (int): Zero-based list position (displayed as index + 1).
            record (PreyRecord): The record to display.
        """
        print(f"\n  --- RECORD {index + 1} ---")
        print(f"  Year:                  {record.year}")
        print(f"  Species:               {record.species}")
        print(f"  Common Name:           {record.common_name}")
        print(f"  Study Site:            {record.study_site}")
        print(f"  Associated Community:  {record.associated_community}")
        print(f"  Latitude:              {record.lat}")
        print(f"  Longitude:             {record.long}")
        print(f"  delta13C:              {record.delta13C}")
        print(f"  delta13Cc:             {record.delta13Cc}")
        print(f"  delta15N:              {record.delta15N}")
        print(f"  delta15Nc:             {record.delta15Nc}")
        print(f"  TP:                    {record.tp}")
        print(f"  C:N:                   {record.cn}")
        print(f"  Astaxanthin (mg/kg):   {record.astaxanthin}")
        print(f"  Canthaxanthin (mg/kg): {record.canthaxanthin}")
        print(f"  Retinol (mg/kg):       {record.retinol}")
