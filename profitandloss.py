from pathlib import Path
import csv
 # Read and process "Profit & Loss.csv" to calculate net profit differences
def read_and_process_file():
    # Define the path to the CSV file
    file_path = Path.cwd() / "csv_reports" / "Profit & Loss.csv"
    # Open the CSV file and read its contents
    with file_path.open(mode="r", encoding="UTF-8", newline="") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        # Extract the day and net profit for each record
        records = [[row[0]] + [int(row[4])] for row in reader]

    # Calculate the difference in net profit from the previous day
    for i in range(1, len(records)):
        profit_diff = records[i][1] - records[i-1][1]
        records[i].append(profit_diff)

    # The first record has no previous day for comparison
    records[0].append(0)

    return records

def get_net_profit_difference(file_path):
    '''
    Accepts file as input.
    Return dict in the form of {day: net profit diff}
    '''
    profits = []  # Store [day, net profit] for day 11-90
    with open(file_path, encoding='utf-8') as f:
        rows = f.readlines()[1:]  # Get rows of data excluding header
        for row in rows:
            row.rstrip("\n")
            row = row.split(',')  # Split each row into a list

            day = int(row[0])
            net_profit = int(row[-1])

            if not 11 <= day <= 90:
                continue  # skip if day not in range
            profits.append([day, net_profit])
    
    res = {}
    res[11] = 0  # Add day 11 first. Difference will be 0
    
    # Add remaining differences
    for i in range(1, len(profits)):
        day = profits[i][0]
        diff = profits[i][1] - profits[i - 1][1]
        res[day] = diff

    return res
def get_output(profit_diff):
    '''
    Accepts a dict as argument.
    Returns output according to trend.
    '''
    trend = get_trend(profit_diff)
    if trend == "increase":
        return get_increasing_output(profit_diff)
    elif trend == "decreasse":
        return get_decreasing_output(profit_diff)
    else:
        return get_fluctuating_output(profit_diff)


def get_trend(profit_diff):
    '''
    Accepts a dict as argument.
    Returns trend as string output.
    '''
    increasing = False
    decreasing = False
    for diff in profit_diff.values():
        # If both increasing and decrease has occured in middle of loop, break loop.
        if increasing and decreasing:
            break

        if diff > 0:
            increasing = True
        elif diff < 0:
            decreasing = True
    
    if increasing and decreasing:
        return "fluctuate"
    elif increasing:
        return "increase"
    else:
        return "decrease"
