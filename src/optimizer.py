import finquant.portfolio as fq
from typing import List, Tuple, Any
import pandas as pd
from pypfopt import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices
import datetime

def compute_efficient_weights(names: List[str]):
    """
    Compute efficient weights of a portfolio
    """
    # Read in price data
    df = pd.read_csv("data/stocks_hist.csv", index_col=0)
    df = df[names]
    # Calculate expected returns and sample covariance
    mu = expected_returns.mean_historical_return(df)
    S = risk_models.sample_cov(df)

    # Optimize for maximal Sharpe ratio
    ef = EfficientFrontier(mu, S)
    raw_weights = ef.max_sharpe()
    cleaned_weights = ef.clean_weights()
    
    ret, vol, sharpe = ef.portfolio_performance(verbose=True)

    return {"weights": cleaned_weights, "sharpe": sharpe, "ret": ret, "vol": vol}

def compute_discrete_allocation(names: List[str], weights: List[float],
                                total_portfolio_value: int = 100_000):

    df = pd.read_csv("data/stocks_hist.csv", index_col=0, parse_dates=True)
    df = df[names]
    latest_prices = get_latest_prices(df)
    print(weights)
    # Convert weights to a dictionary
    
    weights = weights.set_index(0).T.to_dict('records')[0]

    da = DiscreteAllocation(weights, latest_prices,
                            total_portfolio_value=total_portfolio_value)
    allocation, leftover = da.greedy_portfolio()
    print(allocation)
    return allocation, leftover

if __name__ == "__main__":
    names = [ "AXP", "LUV", "DIS", "PG"]
    weights_eff = compute_efficient_weights(names)["weights"]
    weights_eff = pd.DataFrame.from_dict(weights_eff, orient='index', columns=['value']).reset_index().rename(columns={'index': 0, 'value': 1})

    compute_discrete_allocation(names, weights=weights_eff, total_portfolio_value=10_000)