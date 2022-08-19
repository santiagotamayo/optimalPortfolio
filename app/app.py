from crypt import methods
import helpers
import pandas as pd
from flask import Flask, render_template, request

from pypfopt import risk_models 
from pypfopt.expected_returns import mean_historical_return
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

STOCKS = ['AAPL', 'WMT', 'TSLA', 'GE', 'AMZN', 'DB']
START = '2021-01-01'
END = '2022-01-01'

PORTFOLIO_VALUE = 1000000 #USD

NAME = '/api/v1'
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.route(f'{NAME}/path', methods = ["POST"])
def func_name():
    data = request.get_json().split(";") #  Ejemplo ["AAPL", "MSFT"]
    df = helpers.download_prices_as_frame( stocks = data, 
                                           start_date = START, 
                                           end_date = END)
    
    mu = mean_historical_return(df)
    sigma = risk_models.sample_cov(df)

    ef_sharpe = EfficientFrontier(mu, sigma)
    sharpe_weights = ef_sharpe.max_sharpe()
    
    ef_minvol = EfficientFrontier(mu, sigma)
    minvol_weights = ef_minvol.min_volatility()
    
    return {
            'optimal_weigths': {'sharpe_weigths':sharpe_weights, 
                                'sharpe_pfmc': list(ef_sharpe.portfolio_performance())
                                }, 
            
            'minvol_weigths':  {'minvol_weigths':minvol_weights, 
                                'minvol_pfmc': list(ef_minvol.portfolio_performance())
                                }, 
            }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
