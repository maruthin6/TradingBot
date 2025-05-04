import time
import csv
import os
import asyncio

class DataFlusher:
    def __init__(self,  valid_fieldnames, flush_interval, output_dir="market_data"):
        self.valid_fieldnames = valid_fieldnames
        self.output_dir = output_dir
        self.flush_interval = flush_interval
        os.makedirs(self.output_dir, exist_ok=True)  # Create the directory if it doesn't exist

    async def dump_data_periodically(self, recent_data):
        while True:
            await asyncio.sleep(self.flush_interval)

            if recent_data:
                timestamp = int(time.time())
                filename = os.path.join(self.output_dir, f"candle_1m_{timestamp}.csv")
                
                # Use VALID_FIELDNAMES as the fieldnames for the CSV
                with open(filename, "w", newline="") as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=self.valid_fieldnames)
                    writer.writeheader()
                    writer.writerows(recent_data)

                print(f"[Dumped {len(recent_data)} records to {filename}]")
                recent_data.clear()
