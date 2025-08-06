from app.utils.time_utils import round_timestamp
from app.db.mongo import get_db


async def update_candles_from_trade(trade, intervals=["1m"]):
    price = trade["PDrCotVal"]
    volume = trade["QTotTran5J"]
    symbol = str(trade["InsCode"])
    timestamp = trade["received_at"]

    for interval in intervals:
        candle_time = round_timestamp(timestamp, interval)
        filter = {"symbol": symbol, "interval": interval, "time": candle_time}
        update = {
            "$min": {"low": price},
            "$max": {"high": price},
            "$set": {
                "close": price,
                "volume": volume,
                "last_updated": timestamp,
            },
            "$setOnInsert": {
                "open": price,
                "time": candle_time,
                "symbol": symbol,
                "interval": interval,
            },
        }

        db = get_db()
        await db["candles"].update_one(filter, update, upsert=True)
