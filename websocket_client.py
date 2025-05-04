import asyncio
import websockets
import json
from config import MAX_COMPLETE_DATA_SIZE, VALID_FIELDNAMES
from utils.logger import Logger
from utils.data_flusher import DataFlusher

class WebSocketClient:
    def __init__(self, uri, logger, data_flusher, strategies):
        self.uri = uri
        self.logger = logger
        self.data_flusher = data_flusher
        self.strategies = strategies
        self.complete_data = {}
        self.recent_data = []

    async def connect(self):
        subscription_message = {
            "type": "subscribe",
            "payload": {
                "channels": [
                    {
                        "name": "candlestick_1m", 
                        "symbols": ["BTCUSD"]
                    }
                ]
            }
        }

        async with websockets.connect(self.uri) as websocket:
            self.log(f"Subscribed to market data via URI: {self.uri}")
            await websocket.send(json.dumps(subscription_message))
            
            while True:
                message = await websocket.recv()
                data = json.loads(message)
                self.log(f"Received data: {data}")
                self.handle_ticker_data(data)

    def handle_ticker_data(self, data):
        if not all(k in data for k in VALID_FIELDNAMES):
            return 

        filtered_data = {key: value for key, value in data.items() if key in VALID_FIELDNAMES}
        candle_time = filtered_data["candle_start_time"]

        self.complete_data[candle_time] = filtered_data
        self.recent_data.append(filtered_data)

        # Keep only the most recent data if the size exceeds the max limit
        if len(self.complete_data) > MAX_COMPLETE_DATA_SIZE:
            self.complete_data.pop(0)

        # Run strategies asynchronously after processing the data
        asyncio.create_task(self.run_strategies())

    async def run_strategies(self):
        data_list = list(self.complete_data.values())
        tasks = [strategy.on_new_data(data_list) for strategy in self.strategies if strategy.enabled]
        
        if tasks:
            asyncio.gather(*tasks)
        else:
            self.log("No strategies to run.") 

    def log(self, message):
        asyncio.create_task(self.logger.log(self.__class__.__name__ , message))  