import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt

# compound series beginning at initial value, with annual growth rate and monthly contributions
def compound_investment_with_monthly_contributions(initial, rate, years, monthly_contribution):
    # Create a list to store the investment amount at each time interval
    investment = [initial]
    # Create a list to store the investment amount without compounding
    investment_no_compounding = [initial]
    # Create a list to store the dates
    dates = [pd.to_datetime('today')]
    # Loop through the number of years
    for i in range(1, years+1):
        # Compute the number of months in the current year
        months = 12
        # Loop through the number of months in the current year
        for j in range(1, months+1):
            # Compound the investment using the formula: investment[i] = investment[i-1] * (1 + rate/12) + monthly_contribution
            investment.append(round(investment[-1] * (1 + rate/12) + monthly_contribution, 2))
            # Add the monthly contribution to the investment without compounding
            investment_no_compounding.append(investment_no_compounding[-1] + monthly_contribution)
            # Add the date for the current month to the dates list
            dates.append(dates[-1] + pd.DateOffset(months=1))
    # Create a DataFrame from the investment list and add column headers
    df = pd.DataFrame({'Investment':investment, 'Investment without compounding':investment_no_compounding},index=dates)
    df.index = df.index.strftime('%Y-%m-%d')
    return df

if __name__ == "__main__":
    # create a series of annual balances
    balances = compound_series(100000, 0.1, 20)
    # print the series
    plt.plot(balances)
    plt.show()