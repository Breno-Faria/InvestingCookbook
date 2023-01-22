import streamlit as st
import finquant.portfolio as fq
from typing import List, Tuple, Any
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from pypfopt import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices
import yfinance as yf
import datetime

def download_data(names: List[str] = None,
                  start: datetime = datetime.datetime(2019, 1, 1),
                  end: datetime = datetime.datetime(2023, 1, 1)) \
        -> pd.DataFrame:

    data = yf.download(names, start=start, end=end)
    data = data["Adj Close"]
    # drop nan values
    data = data.dropna()
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

def compute_discrete_allocation(names: List[str],
                                start: datetime = datetime.datetime(2019, 1, 1),
                                end: datetime = datetime.datetime(2023, 1, 1),
                                total_portfolio_value: int = 10_000):

    df = download_data(names=names, start=start, end=end)
    df = df[names]
    latest_prices = get_latest_prices(df)
    weights = pd.read_csv("data/weights.csv", header=None)
    st.write(weights)
    # Convert weights to a dictionary
    weights = weights.set_index(0).T.to_dict('records')[0]
    st.write(weights)

    da = DiscreteAllocation(weights, latest_prices,
                            total_portfolio_value=total_portfolio_value)
    allocation, leftover = da.greedy_portfolio()

    st.write("Discrete allocation:", allocation)
    st.write("Funds remaining: ${:.2f}".format(leftover))

    return None

def compute_cum_returns() -> pd.DataFrame:
    """
    Compute cumulative returns of a portfolio
    """

    df = pd.read_csv("data/sp500_data.csv", index_col=0)
    # Compute cumulative returns for each ticker
    cum_returns = (1 + df.pct_change()).cumprod()
    cum_returns.to_csv("data/cum_returns.csv")

    return cum_returns

def compute_portfolio_value(cum_returns: pd.DataFrame,
                            allocation: pd.DataFrame,
                            total_portfolio_value: float) -> pd.DataFrame:
    """
    Compute the value of a portfolio
    """

    pf_value = cum_returns * allocation * total_portfolio_value
    pf_value.to_csv("data/pf_value.csv")

    return pf_value






