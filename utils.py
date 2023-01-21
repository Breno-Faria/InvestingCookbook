import streamlit as st
import finquant.portfolio as fq
from typing import List, Tuple, Any
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from pypfopt import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
import yfinance as yf
import datetime

def download_data(names: List[str] = None,
                  start: datetime = datetime.datetime(2019, 1, 1),
                  end: datetime = datetime.datetime(2023, 1, 1)) \
        -> pd.DataFrame:

    data = yf.download(names, start=start, end=end)
    data = data["Adj Close"]
    data.to_csv('data/sp500_data.csv')

    return data
def get_tickers_name() -> List[str]:
    """
    Get a list of tickers names from data_info.csv
    """

    tickers = pd.read_csv("data/sp500_info.csv")
    tickers = tickers["Symbol"].tolist()

    return tickers
def create_pf(names: List[str],
              start_date: str,
              end_date: str,
              pf_allocation: pd.DataFrame) -> fq.Portfolio:
    """
    Create a portfolio from a list of tickers

    """

    pf = fq.build_portfolio(names=names,
                            start_date=start_date,
                            end_date=end_date,
                            data_api='yfinance',
                            pf_allocation=pf_allocation)

    return pf

def plot_cum_returns(pf: fq.Portfolio) -> None:
    """
    Plot cumulative returns of a portfolio
    """

    pf.comp_cumulative_returns().plot(
        title="Cumulative returns of the portfolio").axhline(y=0,
                                                             color="black",
                                                             lw=3)
    plt.savefig("figures/cumulative_returns.png")
    # open the image
    image = Image.open("figures/cumulative_returns.png")
    # show the image
    st.image(image, caption="Cumulative returns of the portfolio")

    return None

def compute_efficient_weights(names: List[str],
                              start: datetime = datetime.datetime(2019, 1, 1),
                              end: datetime = datetime.datetime(2023, 1, 1)) \
        -> None:
    """
    Compute efficient weights of a portfolio
    """
    # Read in price data
    df = download_data(names=names, start=start, end=end)
    df = df[names]
    # Calculate expected returns and sample covariance
    mu = expected_returns.mean_historical_return(df)
    S = risk_models.sample_cov(df)

    # Optimize for maximal Sharpe ratio
    ef = EfficientFrontier(mu, S)
    raw_weights = ef.max_sharpe()
    cleaned_weights = ef.clean_weights()
    ef.save_weights_to_file("data/weights.csv")  # saves to file
    st.write(cleaned_weights)
    ret, vol, sharpe = ef.portfolio_performance(verbose=True)
    st.write("Expected Annual Return: ", round(ret, 4))
    st.write("Annual Volatility: ", round(vol, 4))
    st.write("Sharpe Ratio: ", round(sharpe, 4))

    return None



