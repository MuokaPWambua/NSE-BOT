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
        
        if isinstance(data, pd.core.frame.DataFrame):
            # Check if there is a position to take
            if data['Positions'][0] == 'Buy':
                self.order = self.buy(price=data['Entry'][0], exectype=bt.Order.Market)
            
            if data['Positions'][0] == 'Sell':
                self.order = self.sell(price=data['Entry'][0], exectype=bt.Order.Market)
    
                            
            if not os.path.exists(bot_dir):
                os.makedirs(bot_dir)
                
            excel_file_path = os.path.join(bot_dir, 'backtest.xlsx')
            data.to_excel(excel_file_path, header=True, index=False, engine='openpyxl')
            
    def stop(self):
        print('Finished')

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    # Set the initial cash value
    cerebro.broker.setcash(100000.0)
    
    # Configure commissions
    cerebro.broker.setcommission(commission=10.0, margin=False)

    # Specify slippage
    cerebro.broker.set_slippage(slip_open=0.50, slip_close=0.50)

    # Configure margin requirements
    cerebro.broker.set_margin(perc=10.0)

    data = bt.feeds.PandasData(dataname=get_historical_data('^NSEI')) #^NSEI
    cerebro.adddata(data)
    cerebro.addstrategy(NSEStrategy, symbol='^NSEI')

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.plot()