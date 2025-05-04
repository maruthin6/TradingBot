import asyncio

class BaseStrategy:
    def __init__(self, name, logger):
        self.name = name
        self.enabled = True
        self.logger = logger

    async def on_new_data(self, data_batch):
        """Called when new data is available."""
        raise NotImplementedError

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def log(self, message):
        asyncio.create_task(self.logger.log(self.name, message))
