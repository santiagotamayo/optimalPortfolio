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

if __name__ == '__main__':

    stocks = ['AAPL', 'WMT', 'TSLA', 'GE', 'AMZN', 'DB']

    dia_inicial = '2022-01-01'
    dia_final = '2022-06-01'
    
    frame = download_prices_as_frame(stocks=stocks, 
                                     start_date=dia_inicial, 
                                     end_date=dia_final)
    
    frame.to_csv('data.csv')
    
    
    