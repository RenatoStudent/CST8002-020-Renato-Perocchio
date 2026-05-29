import csv 
from models.prey_record import PreyRecord

DATASET_PATH = "data/prey collection & Analysis - raw data.csv"
MAX_RECORDS = 1

def load_records():
    records = []
    try:
        with open(DATASET_PATH, "r", encoding="latin-1") as file:
            reader = csv.reader(file)
            next(reader)
            count = 0
            for row in reader:
                if count >= MAX_RECORDS:
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
                count += 1
    except FileNotFoundError:
        print(f"ERROR - Dataset file '{DATASET_PATH}' cannot be found.")
        print(f"Please place the CSV in the '/data' folder and try again.")
    except Exception as e:
        print(f"Something went wrong when loading dataset {e}")
    return records