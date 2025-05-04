import asyncio
import time
import os

class Logger:
    def __init__(self, flush_interval, output_dir="logs"):
        self.log_queue = asyncio.Queue()
        self.log_buffer = []
        self.output_dir = output_dir
        self.LOG_FLUSH_INTERVAL = flush_interval
        os.makedirs(self.output_dir, exist_ok=True)  # Create the directory if it doesn't exist


    async def log(self, name, message):
        await self.log_queue.put((name, message))

    async def log_worker(self):
        while True:
            name, message = await self.log_queue.get()
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            log_line = f"[{timestamp}][{name}] {message}"
            print(log_line)
            self.log_buffer.append(log_line)
            self.log_queue.task_done()

    async def log_flusher(self):
        while True:
            await asyncio.sleep(self.LOG_FLUSH_INTERVAL)
            timestamp = int(time.time())
            filename = f"{self.output_dir}/{timestamp}.txt"
            if self.log_buffer:
                with open(filename, "w") as log_file:
                    log_file.write("\n".join(self.log_buffer) + "\n")
                print(f"[Dumped {len(self.log_buffer)} logs to {filename}]")
                self.log_buffer.clear()
