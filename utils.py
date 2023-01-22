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
import plotly.graph_objects as go

def download_data(names: List[str] = None,
                  start: datetime = datetime.datetime(2019, 1, 1),
                  end: datetime = datetime.datetime(2023, 1, 1)) \
        -> pd.DataFrame:

    data = yf.download(names, start=start, end=end)
    sp500 = yf.download("^GSPC", start=start, end=end)
    data = data["Adj Close"]
    # drop nan values
    data = data.dropna()
    data.to_csv('data/sp500_data.csv')
    sp500.to_csv('data/sp500_index.csv')

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
    # remove the first row by ones
    cum_returns.iloc[0, :] = 1
    cum_returns.to_csv("data/cum_returns.csv")

    return cum_returns

def compute_portfolio_value(cum_returns: pd.DataFrame,
                            total_portfolio_value: float) -> pd.DataFrame:
    """
    Compute the value of a portfolio
    """
    allocation = pd.read_csv("data/weights.csv", index_col=0, header=None)
    # keep the first column
    allocation = allocation.iloc[:, 0]
    pf_value = cum_returns * allocation * total_portfolio_value
    total_pf_value = pf_value.sum(axis=1)
    # rename column
    total_pf_value = total_pf_value.rename("PF_value")
    total_pf_value.to_csv("data/total_pf_value.csv")

    return total_pf_value

def compute_sp500_value(total_portfolio_value: float) -> pd.DataFrame:
    """
    Compute the value of the S&P500 index
    """
    sp500 = pd.read_csv("data/sp500_index.csv", index_col=0)
    sp500 = sp500["Adj Close"]
    sp500_cum_returns = (1 + sp500.pct_change()).cumprod()
    # replace first line by ones
    sp500_cum_returns.iloc[0] = 1
    # rename column
    sp500_cum_returns = sp500_cum_returns.rename("SP500")
    sp500_value = sp500_cum_returns * total_portfolio_value
    sp500_value.to_csv("data/sp500_value.csv")

    return sp500_value

def plot_pf_vs_index() -> None:
    """
    Plot the value of the portfolio and the S&P500 index
    """
    total_pf_value = pd.read_csv("data/total_pf_value.csv", index_col=0)
    sp500_value = pd.read_csv("data/sp500_value.csv", index_col=0)
    # merge the two dataframes
    df = pd.merge(total_pf_value, sp500_value, left_index=True, right_index=True)
    # plot the two dataframes
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df["PF_value"],
                                mode='lines',
                                name='Portfolio'))
    fig.add_trace(go.Scatter(x=df.index, y=df["SP500"],
                                mode='lines',
                                name='S&P500'))
    fig.update_layout(title="Portfolio vs S&P500",
                        xaxis_title="Date",
                        yaxis_title="Value")

    st.plotly_chart(fig)
    return None







