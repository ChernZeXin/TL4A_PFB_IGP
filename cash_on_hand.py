from pathlib import Path
import csv

# Function to read "Cash-On-Hand.csv" and parse contents into a list
def read_and_process_file():
    file_path = Path.cwd() / "csv_reports" / "Cash_on_Hand.csv"
    with file_path.open(mode="r", encoding="UTF-8", newline="") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        # Extract the day and Cash on hand for each record
        cash_on_hand = [[row[0], int(row[1])] for row in reader]  # Day and cash on hand
    return cash_on_hand

def get_COH_difference(file_path):
    '''
    Accepts file as input.
    Return dict in the form of {day: cash on hand diff}
    '''
    cashonhand = []  # Store [day, cash on hand] for day 11-90
    with open(file_path, encoding='utf-8') as f:
        rows = f.readlines()[1:]  # Get rows of data excluding header
        for row in rows:
            row.rstrip("\n")
            row = row.split(',')  # Split each row into a list

            day = int(row[0])
            COH = int(row[-1])

            if not 11 <= day <= 90:
                continue  # skip if day not in range
            cashonhand.append([day, COH])
    
    res = {}
    res[11] = 0  # Add day 11 first. Difference will be 0
    
    # Add remaining differences
    for i in range(1, len(cashonhand)):
        day = cashonhand[i][0]
        diff = cashonhand[i][1] - cashonhand[i - 1][1]
        res[day] = diff

    return res

def get_output(COH_diff):
    '''
    Accepts a dict as argument.
    Returns output according to trend.
    '''
    trend = get_trend(COH_diff)
    if trend == "increase":
        return get_increasing_output(COH_diff)
    elif trend == "decreasse":
        return get_decreasing_output(COH_diff)
    else:
        return get_fluctuating_output(COH_diff)


def get_trend(COH_diff):
    '''
    Accepts a dic as argument.
    Returns trend as string output.
    '''
    increasing = False
    decreasing = False
    for diff in COH_diff.values():
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
def get_increasing_output(COH_diff):
    '''
    Accepts a dict as argument.
    Return output for increasing trend.
    '''
    highest_day = 0
    highest_increase = 0

    for day, amt in COH_diff.items():
        if amt > highest_increase:
            highest_increase = amt
            highest_day = day

    output = f'[CASH SURPLUS] CASH ON EACH DAY IS HIGHER THAN PREVIOUS DAY\n[HIGHEST CASH SURPLUS] DAY: {highest_day}, AMOUNT: SGD{highest_increase}\n'
    return output

def get_decreasing_output(COH_diff):
    '''
    Accepts a dict as argument.
    Return output for decreasing trend.
    '''
    lowest_day = 0
    lowest_increase = 0

    for day, amt in COH_diff.items():
        if amt < lowest_increase:
            lowest_increase = amt
            lowest_day = day

    output = f'[CASH DEFICIT] CASH ON EACH DAY IS LOWER THAN PREVIOUS DAY\n[HIGHEST CASH DEFICIT] DAY: {lowest_day}, AMOUNT: SGD{-lowest_increase}\n'
    return output


def get_fluctuating_output(COH_diff):
    '''
    Accepts a dict as argument.
    Return output for fluctuating trend.
    '''
    deficits = []  # Store days with deficits

    output = ""
    for day, amt in COH_diff.items():
        if amt < 0:
            deficits.append(day)  # Append days with deficit to list
            output += f"[CASH DEFICIT] DAY: {day}, AMOUNT:  SGD{amt * -1}\n"

    # Get top 3 highest deficits
    top = [0, 0]
    second = [0, 0]
    third = [0, 0]

    for day in deficits:
        curr_deficit = COH_diff[day]  # Get deficit for current day
        if curr_deficit < top[1]:  # If largest deficit
            third = second
            second = top
            top = [day, curr_deficit]
        elif curr_deficit < second[1]:  # If second largest
            third = second
            second = [day, curr_deficit]
        elif curr_deficit < third[1]:  # If third largest
            third = [day, curr_deficit]

    top3_highest = [top, second, third]

    for index, deficit in enumerate(top3_highest):
        day = deficit[0]
        amount = abs(deficit[1])  # Convert the deficit amount to a positive value

        if index == 0:
            output += f"[HIGHEST CASH DEFICIT] DAY: {day}, AMOUNT: SGD{amount}\n"
        elif index == 1:
            output += f"[2ND HIGHEST CASH DEFICIT] DAY: {day}, AMOUNT: SGD{amount}\n"
        else:
            output += f"[3RD HIGHEST CASH DEFICIT] DAY: {day}, AMOUNT: SGD{amount}\n"

    return output

h: # Main program
FILEPATH = Path.cwd() / "csv_reports" / "Cash_on_Hand.csv"

def coh_function():
    net_diff = get_COH_difference(FILEPATH)
    output = get_output(net_diff)
    with open('Summary_report.txt', 'a', encoding='utf-8') as f:
        f.write(output)
