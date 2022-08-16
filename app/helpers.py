import yfinance as yf
import pandas as pd

def download_prices_as_frame(stocks: list[str], start_date: str, end_date: str):
    """ Existira una mejor forma? """
    stock_data = {}

    for stock in stocks:
        print(f'Download data {stock}')
        ticker = yf.Ticker(stock)
        stock_data[stock] = ticker.history(start=start_date, end=end_date)['Close']
    return pd.DataFrame(stock_data)