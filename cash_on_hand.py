import cash_on_hand
import overheads
import ProfitandLoss

def main():
    overheads.overhead_function()
    cash_on_hand.coh_function()
    ProfitandLoss.profit_loss_function()

main()

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
FILEPATH = Path.cwd() / "csv_reports" / "Cash-On-Hand.csv"

def coh_function():
    net_diff = get_COH_difference(FILEPATH)
    output = get_output(net_diff)
    with open('Summary_report.txt', 'a', encoding='utf-8') as f:
        f.write(output)
