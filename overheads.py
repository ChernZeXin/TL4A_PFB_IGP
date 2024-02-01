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

def identify_highest_overhead_and_generate_output(overheads):
    percentage_overheads = []
    for row in overheads:
        percentage_overheads.append(row[1])

    output = f'[HIGHEST OVERHEAD] {overheads[percentage_overheads.index(max(percentage_overheads))][0]}: {overheads[percentage_overheads.index(max(percentage_overheads))][1]}%\n'
    return output

def overhead_function():
    # Read and process the CSV file
    records = read_and_process_file()
    # 
    output = identify_highest_overhead_and_generate_output(records)
    # Write the output to the Summary_report.txt file
    with open('Summary_report.txt', 'w') as f:
        f.write(output)
