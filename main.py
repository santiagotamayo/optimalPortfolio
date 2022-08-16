from tabnanny import verbose
from extract import download_prices_as_frame
from settings import (START, END, STOCKS, PORTFOLIO_VALUE)

from pypfopt import risk_models 
from pypfopt.expected_returns import mean_historical_return
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

df = download_prices_as_frame( stocks = STOCKS, 
                               start_date = START, 
                               end_date = END, 
                               )

latest_prices = get_latest_prices(df)

mu = mean_historical_return(df)
sigma = risk_models.sample_cov(df)

ef_sharpe = EfficientFrontier(mu, sigma)
sharpe_weights = ef_sharpe.max_sharpe()

ef_minvol = EfficientFrontier(mu, sigma)
minvol_weights = ef_minvol.min_volatility()
#
da = DiscreteAllocation(sharpe_weights, 
                        latest_prices, 
                        total_portfolio_value = PORTFOLIO_VALUE)

allocation, leftover = da.lp_portfolio()
print(f'Allocation {allocation} {leftover}')

print(ef_sharpe.portfolio_performance(verbose=True))
breakpoint()

