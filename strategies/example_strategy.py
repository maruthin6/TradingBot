from .base_strategy import BaseStrategy

class ExampleStrategy(BaseStrategy):
    def __init__(self, logger, short_window=3, long_window=5):
        super().__init__("ExampleStrategy", logger)
        self.short_window = short_window
        self.long_window = long_window
        self.last_candle_window = None

    async def on_new_data(self, data_batch):
        if not self.enabled or len(data_batch) < self.long_window:
            self.log("Data not sufficient!")
            return
        
        current_candle_window = data_batch[-1]['candle_start_time']
        if self.last_candle_window == None or self.last_candle_window == current_candle_window:
            return
        self.last_candle_window = current_candle_window

        closes = [d["close"] for d in data_batch[-self.long_window:]]
        short_avg = sum(closes[-self.short_window:]) / self.short_window
        long_avg = sum(closes) / self.long_window

        if short_avg > long_avg:
            self.log("BUY SIGNAL")
        elif short_avg < long_avg:
            self.log("SELL SIGNAL")
        else:
            self.log("NO SIGNAL")
