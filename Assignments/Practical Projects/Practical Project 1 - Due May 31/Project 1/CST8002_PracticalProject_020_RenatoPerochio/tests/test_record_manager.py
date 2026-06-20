# ============================================================
# Course:      CST8002 - Programming Language Research Project
# Professor:   Stanley Pieda
# Due Date:    June 21, 2026
# Author:      Renato Perocchio
# References:
#   [1] Python Software Foundation. (2024). unittest — Unit testing framework.
#       docs.python.org. [online] Available at: https://docs.python.org/3/library/unittest.html
#       [Accessed on June 19, 2026]
# ============================================================

"""
Unit tests for the RecordManager business layer.
Uses Python's built-in unittest framework.

Run from the project root directory with:
    python -m unittest discover -s tests -v
"""

import unittest
from business.record_manager import RecordManager
from model.prey_record import PreyRecord


def make_sample_record(year="2020", species="Salmo salar"):
    """
    Helper function that creates a sample PreyRecord for use in tests.

    Args:
        year (str): Year value for the record.
        species (str): Species name for the record.

    Returns:
        PreyRecord: A populated sample record.
    """
    return PreyRecord(
        year=year,
        species=species,
        common_name="Atlantic Salmon",
        study_site="Test Site A",
        associated_community="Test Community",
        lat="45.123",
        long="-75.456",
        delta13C="-22.1",
        delta13Cc="-21.5",
        delta15N="12.3",
        delta15Nc="12.0",
        tp="3.2",
        cn="3.5",
        astaxanthin="1.0",
        canthaxanthin="0.5",
        retinol="0.2"
    )


class TestRecordManager(unittest.TestCase):
    """Unit tests for the RecordManager class in the business layer."""

    def setUp(self):
        """Creates a fresh RecordManager before each test."""
        self.manager = RecordManager()

    def test_add_record_increases_count(self):
        """Adding a record should increase the count from 0 to 1."""
        self.manager.add_record(make_sample_record())
        self.assertEqual(self.manager.count(), 1)

    def test_delete_record_decreases_count(self):
        """Deleting the only record should reduce the count back to 0."""
        self.manager.add_record(make_sample_record())
        result = self.manager.delete_record(0)
        self.assertTrue(result)
        self.assertEqual(self.manager.count(), 0)

    def test_update_record_changes_field_value(self):
        """Updating a record should replace the year field with the new value."""
        self.manager.add_record(make_sample_record(year="2020"))
        updated = make_sample_record(year="2025")
        self.manager.update_record(0, updated)
        self.assertEqual(self.manager.get_record(0).year, "2025")

    def test_get_record_returns_none_for_invalid_index(self):
        """Requesting an index that does not exist should return None."""
        result = self.manager.get_record(99)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
