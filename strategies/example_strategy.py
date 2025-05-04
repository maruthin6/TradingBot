from .base_strategy import BaseStrategy
import numpy as np

class ExampleStrategy(BaseStrategy):
    def __init__(self, logger):
        super().__init__("ExampleStrategy", logger)
        self.last_candle_window = None

    async def on_new_data(self, data_batch):
        if not self.enabled or len(data_batch) < self.window_size:
            self.log("Data not sufficient!")
            return
        
        current_candle_window = data_batch[-1]['candle_start_time']
        if self.last_candle_window == current_candle_window:
            return
        self.last_candle_window = current_candle_window

        historical_data = data_batch[:-1]

        # Get the last 50 closes excluding current row
        closes = [entry['close'] for entry in historical_data[-50:]]

        ma_30 = np.mean(closes[-30:])
        ma_50 = np.mean(closes)

        if ma_30 < ma_50:
            self.log("Buy signal: MA30 < MA50")
            # Place buy order logic here
        elif ma_30 > ma_50:
            self.log("Sell signal: MA30 > MA50")
            # Place sell order logic here
        else:
            self.log("No action")

        
