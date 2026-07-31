# ============================================================
# Course:      CST8002 - Programming Language Research Project
# Professor:   Daniel Cormier
# Due Date:    August 9, 2026
# Author:      Renato Perocchio
# References:
#   [1] Python Software Foundation. (2024). Classes. docs.python.org.
#       [online] Available at: https://docs.python.org/3/tutorial/classes.html
#       [Accessed on June 19, 2026]
#   [2] Python Software Foundation. (2024). Data Structures. docs.python.org.
#       [online] Available at: https://docs.python.org/3/tutorial/datastructures.html
#       [Accessed on June 19, 2026]
#   [3] Python Software Foundation. (2024). Classes. docs.python.org.
#       [online] Available at: https://docs.python.org/3/tutorial/classes.html
#       [Accessed on June 19, 2026]
#   [4] Python Software Foundation. (2024). Data Structures. docs.python.org.
#       [online] Available at: https://docs.python.org/3/tutorial/datastructures.html
#       [Accessed on June 19, 2026]
#   [5] Python Software Foundation. (2024). collections — Container datatypes.
#       docs.python.org. [online] Available at:
#       https://docs.python.org/3/library/collections.html
#       [Accessed on Jul 30, 2026]
# ============================================================

"""
Business layer: manages the in-memory list of PreyRecord objects.
All add, update, delete, and retrieval operations go through this class.
The presentation layer calls RecordManager; RecordManager calls persistence.
"""

from collections import Counter
from persistence.csv_handler import read_records, write_records

class RecordManager:
    """
    Manages the in-memory sequential data structure (list) of PreyRecord objects.
    Acts as the business layer between the presentation and persistence layers.
    """

    def __init__(self):
        """Initializes an empty in-memory records list."""
        self._records = []

    def load_from_file(self):
        """
        Loads records from the CSV dataset, replacing any existing in-memory data.

        Returns:
            int: The number of records loaded.
        """
        self._records = read_records()
        return len(self._records)

    def save_to_file(self):
        """
        Persists the current in-memory records to a new UUID-named CSV file.

        Returns:
            str: The filename of the saved CSV.
        """
        return write_records(self._records)

    def get_all_records(self):
        """
        Returns the full in-memory records list.

        Returns:
            list: All PreyRecord objects currently in memory.
        """
        return self._records

    def get_record(self, index):
        """
        Returns a single record by zero-based index.

        Args:
            index (int): Zero-based position in the list.

        Returns:
            PreyRecord: The record at that index, or None if out of range.
        """
        if 0 <= index < len(self._records):
            return self._records[index]
        return None

    def add_record(self, record):
        """
        Appends a new PreyRecord to the in-memory list.

        Args:
            record (PreyRecord): The new record to add.
        """
        self._records.append(record)

    def update_record(self, index, record):
        """
        Replaces the record at the given index with a new PreyRecord.

        Args:
            index (int): Zero-based position of the record to replace.
            record (PreyRecord): The replacement record.

        Returns:
            bool: True if the update was successful, False if index is out of range.
        """
        if 0 <= index < len(self._records):
            self._records[index] = record
            return True
        return False

    def delete_record(self, index):
        """
        Removes the record at the given index from the in-memory list.

        Args:
            index (int): Zero-based position of the record to remove.

        Returns:
            bool: True if deleted successfully, False if index is out of range.
        """
        if 0 <= index < len(self._records):
            del self._records[index]
            return True
        return False

    def count(self):
        """
        Returns the number of records currently held in memory.

        Returns:
            int: Total record count.
        """
        return len(self._records)

    '''Done for Practical Project 04'''
    def count_by_column(self, attr):
        """
        Groups the in-memory records by the given PreyRecord attribute name
        and counts how many records fall into each distinct value. Used by
        the Practical Project 4 chart feature to turn raw records into the
        {label: count} shape a bar or pie chart needs.

        Args:
            attr (str): The PreyRecord attribute name to group by, e.g. "species".

        Returns:
            collections.Counter: Maps each distinct value of attr to its
                count, ordered by first appearance in the in-memory list.
        """
        return Counter(getattr(record, attr) for record in self._records)
