import os
import pandas as pd
import numpy as np
from plyer import notification
from utils import get_live_data
import datetime as dt


icon = os.path.join(os.getcwd(),"logo.ico")  # Replace with the path to your icon

def bullish_pattern_sl(data):   
    if data.iloc[-2]['Close'] < data.iloc[-2]['Open'] and data.iloc[-1]['Close'] > data.iloc[-1]['Open']:
        return data.iloc[-1]['Low']
    return False
        
def bearish_pattern_sl(data):
    if data.iloc[-2]['Close'] > data.iloc[-2]['Open'] and data.iloc[-1]['Close'] < data.iloc[-1]['Open']:
        return data.iloc[-1]['High']
    return False

def trading_hours(curr_time):
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
    message = f'📡 Waiting for {symbol} signal...'

    for i in range(len(data)):
        # Check if current time is within market hours
        date = data.index[i]
        
        if trading_hours(date.time()):
            if i >= 21:
                # Get current and previous %K and %D values
                curr_k = data['%K'][i]
                prev_k = data['%K'][i-1]
                curr_d = data['%D'][i]
                prev_d = data['%D'][i-1]
                bull_sl = bullish_pattern_sl(data)
                bear_sl = bearish_pattern_sl(data)
                
                # Check for long entry condition
                if prev_k < prev_d and curr_k > curr_d and bull_sl:
                    
                    signals.append(1)  # Buy signal
                    positions.append(1)  # Enter long position
                    entry_levels.append(data['Close'][i])
                    sl_levels.append(bull_sl)
                    exit_levels.append(data['BB_upper'][i])  
                    message = f"📈 Buy {symbol} entry {data['Close'][i]} exit {data['BB_upper'][i]} sl {bull_sl} date {date}"
                    notification.notify(
                        title = f'{symbol} Signal 🤖',
                        message = message,
                        app_icon = icon)
                    print(message)
                    # TODO: Check for any short position running and exit 
                    
                # Check for sell condition
                elif prev_k > prev_d and curr_k < curr_d and bear_sl:
                    signals.append(-1)  # Sell signal
                    sl_levels.append(bear_sl)
                    positions.append(0)  # Enter short position
                    entry_levels.append(data['Close'][i])  
                    exit_levels.append(data['BB_lower'][i])
                    message = f"📉 Sell {symbol} entry {data['Close'][i]} exit {data['BB_lower'][i]} sl {bear_sl} date {date}"
                    notification.notify(
                        title=f'{symbol} Signal 🤖',
                        message=message,
                        app_icon=icon)
                    print(message)
                    
                    # TODO: Check for any long position running and exit
                # No conditions found
                else:
                    positions.append(-1)
                    signals.append(0)
                    entry_levels.append(0)
                    sl_levels.append(0)  
                    exit_levels.append(0)
                    message = f'📡 Waiting for {symbol} signal...'
                    print(message)
                    
            else:
                signals.append(0)
                positions.append(-1)
                entry_levels.append(0)
                exit_levels.append(0)
                sl_levels.append(0)
                message = f'📡 Waiting for {symbol} signal...'
                print(message)
                
        else:
            signals.append(0)
            positions.append(-1)
            entry_levels.append(0)
            exit_levels.append(0)
            sl_levels.append(0)
            message = f'📡 Waiting for {symbol} signal...'
            print(message)
    # Create a dataframe to store the signals, positions, entry levels, and exit levels
    data['signals'] = signals
    data['positions'] = positions
    data['entry_levels'] = entry_levels
    data['exit_levels'] = exit_levels
    data['sl'] = sl_levels
    print(message)

    return data, message


def start_bot(event, stock='^NSEI', interval='1m', call_back=None):
    while True:
        if event.is_set():
            break
        data = get_live_data(stock, interval)
        data = calculate_indicators(data)
        strategy_results, message = strategy(data, symbol=stock)
        if call_back is not None:
            call_back(message)