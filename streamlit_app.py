from utils import *
import pandas as pd
from streamlit_tags import st_tags
import streamlit as st

if __name__ == "__main__":
    st.title("Portfolio Optimizer")
    names = st_tags(
        label='# Enter tickers:',
        text='Press enter to add more',
        # random sample from suggestions
        value=["MSFT", "RCL", "DIS", "PG", "AAPL"],
        suggestions=["MSFT", "RCL", "DIS", "PG",
                     "AAPL", "MMM", "AXP", "BA", "LUV"],
        maxtags=15,
        key='1')

    start_date = st.sidebar.date_input("Start date", value=pd.to_datetime("2019-01-01"))
    end_date = st.sidebar.date_input("End date", value=pd.to_datetime("2020-01-01"))
    pf_allocation = pd.DataFrame({'Name': names,
                                  'Allocation': [1 / len(names)] * len(names)})
    # pf = create_pf(names, start_date, end_date, pf_allocation)
    # plot_cum_returns(pf)
    compute_efficient_weights(names, start=start_date, end=end_date)
    total_portfolio_value = st.sidebar.number_input("Total portfolio value",
                                            value=10_000)
    allocation, leftover = compute_discrete_allocation(names,
                                start=start_date,
                                end=end_date,
                                total_portfolio_value=total_portfolio_value)
    cum_returns = compute_cum_returns()
    plot_w_allocation(allocation, leftover, total_portfolio_value)
    plot_pf_vs_index()
    plot_pf_cum_returns_vs_sp500()












