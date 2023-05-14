import tkinter as tk
from tkinter import ttk
import pandas as pd
import yfinance as yf
from bot import start_bot
import threading
import uuid

class TradingBotGUI:
    def __init__(self, master):
        self.master = master
        master.title("NSE BOT")
        master.geometry()
        master.pack_propagate(0)
        self.threads = {}
        self.stop_event = threading.Event()
        # Create label for stock dropdown menu
        self.stock_label = tk.Label(master, text="Select a stock:")
        self.stock_label.grid(row=1, column=0, padx=10, pady=10)

        # Create stock dropdown menu
        self.stock_var = tk.StringVar()
        self.stock_dropdown = tk.OptionMenu(master, self.stock_var, *self.get_stock_names())
        self.stock_dropdown.grid(row=2, column=0, padx=10, pady=10)

        # Create label for interval dropdown menu
        self.interval_label = tk.Label(master, text="Select an interval:")
        self.interval_label.grid(row=1, column=1, padx=10, pady=10)

        # Create interval dropdown menu
        self.interval_var = tk.StringVar()
        self.interval_dropdown = tk.OptionMenu(master, self.interval_var, *self.get_intervals())
        self.interval_dropdown.grid(row=2, column=1, padx=10, pady=10)

        # Create "Run" button
        self.run_button = tk.Button(master, text="Run", command=self.run_bot)
        self.run_button.grid(row=3, column=0, padx=10, pady=10)
        
        # Create "Stop All" button
        self.stop_button = tk.Button(master, text="Stop All", command=self.stop_all)
        self.stop_button.grid(row=3, column=1, padx=10, pady=10)
    
        self.treeview = ttk.Treeview(master, columns=('symbol', 'interval', 'status'))
        self.treeview.heading('symbol', text='Symbol')
        self.treeview.heading('interval', text='Interval')
        self.treeview.heading('status', text='Status')
        self.treeview.heading('#0', text='Thread ID')
    
        self.treeview.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        # Create status label
        self.status_label = tk.Label(master, text="Status: Not running")
        self.status_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        # Center all the elements
        for i in range(6):
            master.grid_rowconfigure(i, weight=1)
        for i in range(2):
            master.grid_columnconfigure(i, weight=1)
            
    def get_stock_names(self):
        # Get list of Indian stock symbols from Yahoo Finance
        tickers = pd.read_html('https://ournifty.com/stock-list-in-nse-fo-futures-and-options.html#:~:text=NSE%20F%26O%20Stock%20List%3A%20%20%20%20SL,%20%201000%20%2052%20more%20rows%20')[0]
        tickers = tickers.SYMBOL.to_list()
        indian_stocks = [ticker + '.NS' for ticker in tickers]
    
        return indian_stocks

    def get_intervals(self):
        return ['1m', '5m', '15m', '30m', '1h', '4h', '1d', '1w', '1mnth']

    def run_bot(self):
        # Get the selected stock symbol and interval from the dropdown menus
        symbol = self.stock_var.get()
        interval = self.interval_var.get()
        thread_id = str(uuid.uuid4())

        self.threads[thread_id] = threading.Thread(
            target=start_bot,
            args=(self.stop_event,),
            kwargs=({"stock": symbol, 'interval':interval,}))
        self.threads[thread_id].start()
        self.status_label.config(text=f"Status:Running bot for {symbol} with {interval} interval")
        self.treeview.insert('', 'end', text=thread_id, values=(symbol, interval, 'Running'))
        
    def stop_bot(self, thread_id):
        if thread_id in self.threads:
            self.threads[thread_id].join()
            self.status_label.config(text=f"Status: Bot with ID {thread_id} stopped.")
            self.treeview.set(thread_id, 'status', 'Stopped')
            self.master.after(2000, lambda: self.treeview.delete(thread_id))
        else:
            self.status_label.config(text=f"Status: Bot with ID {thread_id} not found.")

    def stop_all(self):
        self.stop_event.set()
        for thread_id in self.threads:
            self.threads[thread_id].join()
        self.status_label.config(text="Status: All threads stopped.")
        

