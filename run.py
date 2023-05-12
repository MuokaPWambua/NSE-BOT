from bot_interface import TradingBotGUI
import tkinter as tk
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

root = tk.Tk()
app = TradingBotGUI(root)
root.mainloop()
