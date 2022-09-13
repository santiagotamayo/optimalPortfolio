import helpers
import yfinance as yf
import taxConvertion as tax

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
app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/portfolio', methods = ["GET", "POST"] )
def portfolio():
    if request.method == 'GET':
        return render_template('portfolio.html')
    
    tick = request.get_json(force=True)
    ticket = yf.Ticker(tick.get("ticket"))
    ticket_info = ticket.info
    
    return {
            'status': 200,
            'existencia': "si",
            'price': ticket_info['currentPrice'], 
            'expected_price': ticket_info['targetMedianPrice'], 
            }
    
@app.route('/taxconvertion', methods = ["GET", "POST"])
def taxconvertion():
    if request.method == 'GET':
        return render_template('taxconvertion.html')
    
    try:
        data = request.get_json(force=True)
        response = tax.estimacion_intereses( tipo = int(data['tipo']), 
                                             interes = float(data['interes']), 
                                             periodo = float(data['periodo']) )
        return response
    except Exception as e:
        return {
            'status': 400,
            'message': str(e)
        } 

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
            'optimal_weigths': {
                                'tickets': data,
                                'weigths': [round(i, 4) for i in list(sharpe_weights.values())], 
                                'pfmance': [round(i, 4) for i in list(ef_sharpe.portfolio_performance())]
                                }, 
            
            'minvol_weigths':  {
                                'tickets': data,
                                'weigths':[round(i, 4) for i in list(minvol_weights.values())], 
                                'pfmance': [round(i, 4) for i in list(ef_minvol.portfolio_performance())]
                                }, 
            }

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8000, debug = True)
