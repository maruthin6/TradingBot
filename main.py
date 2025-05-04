import asyncio
from websocket_client import WebSocketClient
from strategies.example_strategy import ExampleStrategy
from utils.logger import Logger
from utils.data_flusher import DataFlusher
from config import LOG_FLUSH_INTERVAL, DATA_FLUSH_INTERVAL, VALID_FIELDNAMES, WEBSOCKET_URL


class Main:
    async def init(self):
        self.logger = Logger(LOG_FLUSH_INTERVAL)
        self.data_flusher = DataFlusher(VALID_FIELDNAMES, DATA_FLUSH_INTERVAL)
        self.strategies = [
            ExampleStrategy(self.logger)
        ]
        self.websocket_client = WebSocketClient(
            uri=WEBSOCKET_URL,
            logger=self.logger,
            data_flusher=self.data_flusher,
            strategies=self.strategies
        )

    async def start(self):
        await self.init()  # ensure Logger is initialized in the current event loop

        # Start the logger tasks
        asyncio.create_task(self.logger.log_worker())
        asyncio.create_task(self.logger.log_flusher())

        # Start the data flushing task
        asyncio.create_task(self.data_flusher.dump_data_periodically(self.websocket_client.recent_data))

        # Start the websocket connection
        await self.websocket_client.connect()


if __name__ == "__main__":
    main_app = Main()
    asyncio.run(main_app.start())

