from utils import *
import pandas as pd
from streamlit_tags import st_tags
import streamlit as st
import random

if __name__ == "__main__":
    st.title("Portfolio Optimizer")
    suggestions = get_tickers_name()
    names = st_tags(
        label='# Enter tickers:',
        text='Press enter to add more',
        # random sample from suggestions
        value=random.choices(suggestions, k=5),
        suggestions=suggestions,
        maxtags=15,
        key='1')

    start_date = st.date_input("Start date", value=pd.to_datetime("2019-01-01"))
    end_date = st.date_input("End date", value=pd.to_datetime("2020-01-01"))
    pf_allocation = pd.DataFrame({'Name': names,
                                  'Allocation': [1 / len(names)] * len(names)})
    pf = create_pf(names, start_date, end_date, pf_allocation)
    st.write(pf)
    plot_cum_returns(pf)
    compute_efficient_weights(names, start=start_date, end=end_date)
    total_portfolio_value = st.sidebar.number_input("Total portfolio value",
                                            value=10_000)











