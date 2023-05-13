from bot import *
from utils import *

data = get_historical_data('^NSEI')
data = calculate_indicators(data)

strategy_results = strategy(data)

positions = strategy_results.positions
entry_levels = strategy_results.entry_levels
exit_levels = strategy_results.exit_levels
sl_levels = strategy_results.sl

returns = pd.Series(0.0, index=positions.index)  # Initialize returns to 0
entry_levels_valid = entry_levels != 0  # Check if entry levels are valid
returns[entry_levels_valid] = positions.shift(1)[entry_levels_valid] * (exit_levels - entry_levels)[entry_levels_valid] / entry_levels[entry_levels_valid]

strategy_results['cumulative_returns'] = (returns + 1).cumprod()


print(strategy_results.tail(3))
# Save the strategy results to a CSV file
strategy_results.to_excel('backtest_results.xlsx', header=True, index=False)

    
plot_results(strategy_results)