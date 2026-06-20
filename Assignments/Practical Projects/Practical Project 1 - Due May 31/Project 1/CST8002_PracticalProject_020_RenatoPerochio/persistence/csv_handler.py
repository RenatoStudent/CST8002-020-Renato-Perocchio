# ============================================================
# Course:      CST8002 - Programming Language Research Project
# Professor:   Stanley Pieda
# Due Date:    June 21, 2026
# Author:      Renato Perocchio
# References:
#   [1] Python Software Foundation. (2024). csv — CSV File Reading and Writing.
#       docs.python.org. [online] Available at: https://docs.python.org/3/library/csv.html
#       [Accessed on June 19, 2026]

#   [2] Python Software Foundation. (2024). uuid — UUID objects according to RFC 4122.
#       docs.python.org. [online] Available at: https://docs.python.org/3/library/uuid.html
#       [Accessed on June 19, 2026]

#   [3] Python Software Foundation. (2024). Errors and Exceptions.
#       docs.python.org. [online] Available at: https://docs.python.org/3/tutorial/errors.html
#       [Accessed on June 19, 2026]

#   [4] R. Oliveira. (Jul 31, 2024). GUID vs UUID vs ULID: Understanding Unique Identifiers.
#       medium.com. [online] Available at: https://medium.com/@ronaldo.oliver7/guid-vs-uuid-vs-ulid-understanding-unique-identifiers-565c88cdca13
#       [Accessed on June 19, 2026]
# ============================================================

"""
Persistence layer: handles all file I/O for the prey collection dataset.
Reads records from the CSV on startup and writes records to a new UUID-named CSV.
"""

import csv
import uuid
from model.prey_record import PreyRecord

DATASET_PATH = "data/Prey collection & analysis - raw data.csv"
MAX_RECORDS = 100

HEADERS = [
    "Year/Année", "Species/Espèce", "Common name/Nom commun",
    "Study site/Site d'étude", "Associated community/Collectivité associée",
    "Lat", "Long", "delta13C", "delta13Cc", "delta15N", "delta15Nc",
    "TP", "C:N", "Astaxanthin/Astaxanthine (mg/kg)",
    "Canthaxanthin/Canthaxanthine (mg/kg)", "Retinol/Rétinol (mg/kg)"
]


def read_records():
    """
    Opens the prey collection CSV and parses up to MAX_RECORDS rows into
    PreyRecord objects.

    Returns:
        list: A list of PreyRecord objects. Returns an empty list if the
              file is missing or any error occurs.
    """
    records = []
    try:
        with open(DATASET_PATH, "r", encoding="latin-1") as file:
            reader = csv.reader(file)
            next(reader)
            for i, row in enumerate(reader):
                if i >= MAX_RECORDS:
                    break
                record = PreyRecord(
                    year=row[0],
                    species=row[1],
                    common_name=row[2],
                    study_site=row[3],
                    associated_community=row[4],
                    lat=row[5],
                    long=row[6],
                    delta13C=row[7],
                    delta13Cc=row[8],
                    delta15N=row[9],
                    delta15Nc=row[10],
                    tp=row[11],
                    cn=row[12],
                    astaxanthin=row[13],
                    canthaxanthin=row[14],
                    retinol=row[15]
                )
                records.append(record)
    except FileNotFoundError:
        print(f"ERROR: Dataset file '{DATASET_PATH}' not found.")
        print("Please place the CSV file in the /data folder and try again.")
    except Exception as e:
        print(f"ERROR loading dataset: {e}")
    return records


def write_records(records):
    """
    Writes the given list of PreyRecord objects to a new CSV file.
    The filename is a UUID (universally unique identifier) to ensure
    each save produces a distinct file with no name collisions.

    Args:
        records (list): A list of PreyRecord objects to save.

    Returns:
        str: The path of the newly created CSV file.
    """
    filename = f"data/{uuid.uuid4()}.csv"
    try:
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(HEADERS)
            for r in records:
                writer.writerow([
                    r.year, r.species, r.common_name, r.study_site,
                    r.associated_community, r.lat, r.long,
                    r.delta13C, r.delta13Cc, r.delta15N, r.delta15Nc,
                    r.tp, r.cn, r.astaxanthin, r.canthaxanthin, r.retinol
                ])
        print(f"Saved {len(records)} record(s) to '{filename}'.")
    except Exception as e:
        print(f"ERROR saving file: {e}")
    return filename
