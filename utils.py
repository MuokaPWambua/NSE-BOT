
import matplotlib.pyplot as plt
import yfinance as yf

# Define function to get historical OHLC data from Yahoo Finance
def get_historical_data(symbol, start = '2010-05-01', end='2023-05-01', interval='1d'):
    data = yf.download(symbol, start=start, end=end, interval=interval)
    return data

def get_live_data(symbol, interval="1m", period="1d"):
    ticker = yf.Ticker(symbol)
    data = ticker.history(interval=interval, period=period)
    return data


def plot_results(df):
    fig, ax = plt.subplots(figsize=(12,8))
    ax.plot(df)
    ax.set_xlabel('Date')
    ax.set_ylabel('Cumulative Returns')
    ax.set_title('Cumulative Returns of Strategy')
    plt.show()
