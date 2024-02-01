 from pathlib import Path
import csv

def read_and_process_file():
    # Read the CSV file and process the records
    file_path = Path.cwd() / "csv_reports" / "Overheads.csv"
    with file_path.open(mode="r", encoding="UTF-8", newline="") as file:
        reader = csv.reader(file)
        next(reader)  # skip header
        records = []
        for row in reader:
            records.append([row[0], float(row[1])])
            
    return records
