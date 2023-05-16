# NSE BOT
![Alt Text](https://github.com/MuokaPWambua/NSE-BOT/blob/main/image.pngimage.png)
#### How It Works
This trading bot utilizes the stoch cross and candlestick pattern strategy to spot trading opportunities in
NSE markets. Once it finds an opportunity it pops up a desktop notification and write its signals into an excel file. 
With the ability to run check on multiple stocks and on different time intervals.

#### How to Run 
It can be run both as a desktop app and a script. 

To run it as a script you will need:
  - `python -m venv virtual`
  - `source virtual\bin\active` or `.\virtual\Scripts\activate`
  - `pip install -r install requirements.txt`
  - `python run.py`
  
To run it as a desktop application you will need to build it as an installable file by repeating 
the first three steps above then run `python setup.py bdist-msi` this will create an installable
windows file inside the bdist directory for linux system run `python setup.py build`
