
import os
import sys
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd

home_dir = os.path.expanduser("~")
bot_dir = os.path.join(home_dir, "NSE BOT")

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)

def write_dataframe_to_excel(dataframe, directory, excel_file):
    stock_dir = os.path.join(bot_dir, directory)

    if not os.path.exists(stock_dir):
        os.makedirs(stock_dir)    

    excel_file_path = os.path.join(stock_dir, excel_file)
    
    if os.path.exists(excel_file_path):
        # Append the new dataframe to the existing Excel file
        with pd.ExcelWriter(excel_file_path, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
            last_sheet = writer.book.worksheets[-1] # get the last sheet object
            startrow = last_sheet.max_row + 1 # get the next row to start writing at
            dataframe.to_excel(writer, header=False, startrow=startrow, index=False, engine='openpyxl')
        
    else:
        dataframe.to_excel(excel_file_path, header=True, index=False, engine='openpyxl')


# Define function to get historical OHLC data from Yahoo Finance
def get_historical_data(symbol, start = '2022-05-01', end='2023-05-01', interval='1d'):
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