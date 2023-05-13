
import os
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
from openpyxl import load_workbook, Workbook
import uuid

def write_dataframe_to_excel(dataframe, directory, excel_file):
    excel_file_path = os.path.join(directory, excel_file)
    
    if os.path.exists(excel_file_path):
        # Append the new dataframe to the existing Excel file
        writer = pd.ExcelWriter(excel_file_path, mode='a', engine='openpyxl', if_sheet_exists='overlay')
        last_sheet = writer.book.worksheets[-1] # get the last sheet object
        startrow = last_sheet.max_row + 1 # get the next row to start writing at
        dataframe.to_excel(writer, header=False, startrow=startrow, index=False, engine='openpyxl')
        writer.close()
    else:
        # Create a new Excel workbook
        if not os.path.exists(directory):
            os.makedirs(directory)        
        dataframe.to_excel(excel_file_path, header=True, index=False, engine='openpyxl')


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