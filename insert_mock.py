import asyncio
import random
from datetime import datetime
from app.db.mongo import connect_to_mongo, get_db


MOCK_COUNT = 20
SYMBOL_ID = "46700660505281786"  # Gold symbol ID


async def insert_mock_candles():
    await connect_to_mongo()
    db = get_db()

    base_time = datetime(2023, 11, 30, 12, 0)
    base_timestamp = int(base_time.timestamp() * 1000)

    candles = []
    open_price = 190000

    for i in range(MOCK_COUNT):
        time = base_timestamp + i * 60 * 60 * 1000
        change = random.randint(-1000, 1000)
        close_price = open_price + change
        high_price = max(open_price, close_price) + random.randint(100, 1000)
        low_price = min(open_price, close_price) - random.randint(100, 1000)
        volume = random.randint(100000, 5000000)

        candles.append(
            {
                "symbol": SYMBOL_ID,
                "time": time,
                "open": open_price,
                "close": close_price,
                "high": high_price,
                "low": low_price,
                "volume": volume,
            }
        )

        open_price = close_price

    await db["candles"].insert_many(candles)
    print(f"✅ {MOCK_COUNT} mock candles inserted.")


if __name__ == "__main__":
    asyncio.run(insert_mock_candles())
