import time
import random
from datetime import datetime, timedelta
import json

class MNQSimulator:
    def __init__(self, symbol="MNQ", initial_price=18500.0):
        self.symbol = symbol
        self.price = initial_price
        self.last_tick_time = datetime.now()

    def generate_tick(self):
        """Generates a single price tick."""
        change = random.uniform(-2.0, 2.0)
        self.price += change
        tick = {
            "symbol": self.symbol,
            "price": round(self.price, 2),
            "timestamp": datetime.now().isoformat(),
            "volume": random.randint(1, 10)
        }
        return tick

    def generate_candle(self, interval_minutes=1):
        """Generates a simulated OHLCV candle for the given interval."""
        start_price = self.price
        high = start_price
        low = start_price

        # Simulate some ticks within the candle
        num_ticks = random.randint(10, 30)
        for _ in range(num_ticks):
            tick = self.generate_tick()
            high = max(high, tick["price"])
            low = min(low, tick["price"])

        close = self.price
        volume = random.randint(100, 500)

        candle = {
            "symbol": self.symbol,
            "open": round(start_price, 2),
            "high": round(high, 2),
            "low": round(low, 2),
            "close": round(close, 2),
            "volume": volume,
            "timestamp": datetime.now().replace(second=0, microsecond=0).isoformat(),
            "interval": f"{interval_minutes}m"
        }
        return candle

if __name__ == "__main__":
    sim = MNQSimulator()
    print(sim.generate_candle())
