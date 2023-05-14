import pandas as pd
import numpy as np
from plyer import notification
from utils import get_live_data, resource_path, write_dataframe_to_excel
import datetime as dt


icon = resource_path("logo.ico")  # Replace with the path to your icon

def bullish_pattern_sl(data):   
    if data.iloc[-2]['Close'] < data.iloc[-2]['Open'] and data.iloc[-1]['Close'] > data.iloc[-1]['Open']:
        return data.iloc[-1]['Low']
    return False
        
def bearish_pattern_sl(data):
    if data.iloc[-2]['Close'] > data.iloc[-2]['Open'] and data.iloc[-1]['Close'] < data.iloc[-1]['Open']:
        return data.iloc[-1]['High']
    return False

def trading_hours():
    curr_time = dt.datetime.now().time()
    if curr_time >= dt.time(9,15) and curr_time <= dt.time(15,30):
        return True
    return False

def calculate_indicators(data, k_period=6, d_period=3, ma_period=10, stdev_factor=2):
    # Calculate %K and %D values for stochastic oscillator
    highest_high = data['High'].rolling(k_period).max()
    lowest_low = data['Low'].rolling(k_period).min()
    k = 100 * (data['Close'] - lowest_low) / (highest_high - lowest_low)
    d = k.rolling(d_period).mean()

    # Calculate Bollinger Bands
    bb_middle = data['Close'].rolling(ma_period).mean()
    bb_std = data['Close'].rolling(ma_period).std()
    bb_upper = bb_middle + stdev_factor * bb_std
    bb_lower = bb_middle - stdev_factor * bb_std

    # Add calculated indicators to the data
    data['%K'] = k
    data['%D'] = d
    data['BB_upper'] = bb_upper
    data['BB_middle'] = bb_middle
    data['BB_lower'] = bb_lower

    return data

def strategy(data, symbol=''):
    # Initialize empty lists to track signals and positions
    signals = []
    positions = []
    entry_levels = []
    exit_levels = []
    sl_levels = []

    for i in range(len(data)):
        date = dt.datetime.now()   

        # Get current and previous %K and %D values
        curr_k = data.iloc[i]['%K']
        prev_k = data.iloc[i-1]['%K']
        curr_d = data.iloc[i]['%D']
        prev_d = data.iloc[i-1]['%D']
        bull_sl = bullish_pattern_sl(data)
        bear_sl = bearish_pattern_sl(data)
    
        # Check for long entry condition
        if prev_k < prev_d and curr_k > curr_d and bull_sl:
            
            signals.append(1)
            positions.append('Buy')  # Enter long position
            entry_levels.append(data.iloc[i]['Close'])
            sl_levels.append(bull_sl)
            exit_levels.append(data.iloc[i]['BB_upper'])  
            message = f"📈 Buy {symbol} entry {data.iloc[i]['Close']} exit {data.iloc[i]['BB_upper']} sl {bull_sl} date {date}"
            notification.notify(title = f'{symbol} Signal 🤖', message = message, app_icon = icon)
            # TODO: Check for any short position running and exit 
            
        # Check for sell condition
        elif prev_k > prev_d and curr_k < curr_d and bear_sl:
            signals.append(-1)
            sl_levels.append(bear_sl)
            positions.append('Sell')  # Enter short position
            entry_levels.append(data.iloc[i]['Close'])  
            exit_levels.append(data.iloc[i]['BB_lower'])
            message = f"📉 Sell {symbol} entry {data.iloc[i]['Close']} exit {data.iloc[i]['BB_lower']} sl {bear_sl} date {date}"
            notification.notify(title=f'{symbol} Signal 🤖', message=message, app_icon=icon)                
            # TODO: Check for any long position running and exit
            
        # No conditions found
        else:
            positions.append(None)
            signals.append(0)
            entry_levels.append(0)
            sl_levels.append(0)  
            exit_levels.append(0)

    if sum(signals) == 0:
        return None
    
    data['position'] = positions
    data['entry'] = entry_levels
    data['exit'] = exit_levels
    data['sl'] = sl_levels

    return data


def start_bot(event, stock='^NSEI', interval='1m'):

    while True:
        if event.is_set():
            break
        if trading_hours():        
            data = get_live_data(stock, interval)
            data = calculate_indicators(data)
            strategy_results = strategy(data, symbol=stock)
            
            if strategy_results is None:
                pass
            else:
                write_dataframe_to_excel(strategy_results, f'{stock}', f'{interval}.xlsx' )