import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
# compound series beginning at initial value, with annual growth rate and monthly contributions
def compounding_
    # return balance

    return balances

if __name__ == "__main__":
    # create a series of annual balances
    balances = compound_series(100000, 0.1, 20)
    # print the series
    plt.plot(balances)
    plt.show()