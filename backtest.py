from bot import *
from utils import *
import backtrader as bt


class NSEStrategy(bt.Strategy):
    params = (
        ('symbol', ''),
    )
    
    def __init__(self):
        data = pd.DataFrame({
            'High': [x for x in self.datas[0].high],
            'Close': [x for x in self.datas[0].close],
            'Open': [x for x in self.datas[0].open],
            'Low': [x for x in self.datas[0].low]
            }, index=[x for x in self.datas[0]])
        self.data = calculate_indicators(data).fillna(0)
        self.order = None

    def next(self):
        # Get the current data and apply the strategy function
        data = strategy(self.data)
        
        if data is not None:

            # Check if there is a position to take
            if data.iloc[-1]['position'] == 'Buy':
                self.order = self.buy(price=data.iloc[-1]['entry'], exectype=bt.Order.Market)
                self.sell(price=data.iloc[-1]['exit'], exectype=bt.Order.Limit, parent=self.order, transmit=False)
                self.sell(price=data.iloc[-1]['sl'], exectype=bt.Order.Stop, parent=self.order, transmit=True)

            elif data.iloc[-1]['position'] == 'Sell':
                self.order = self.sell(price=data.iloc[-1]['entry'], exectype=bt.Order.Market)
                self.buy(price=data['exit'].iloc[-1][0], exectype=bt.Order.Limit, parent=self.order, transmit=False)
                self.buy(price=data['sl'].iloc[-1][0], exectype=bt.Order.Stop, parent=self.order, transmit=True)
            excel_file_path = os.path.join(bot_dir, 'backtest.xlsx')
            data.to_excel(excel_file_path, header=True, index=False, engine='openpyxl')
            
    def stop(self):
        print('Finished')

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(100000.0)
    data = bt.feeds.PandasData(dataname=get_historical_data('^NSEI'))
    cerebro.adddata(data)
    cerebro.addstrategy(NSEStrategy, symbol='^NSEI')

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.plot()