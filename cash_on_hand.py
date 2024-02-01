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
