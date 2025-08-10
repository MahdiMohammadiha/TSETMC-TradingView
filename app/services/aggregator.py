from app.utils.time_utils import round_timestamp
from app.db.mongo import get_db


async def update_candles_from_trade(trade, intervals=["1m"]):
    """
    Update or create candle data in MongoDB based on a trade.

    This function processes a single trade and updates the relevant 
    candlestick (OHLCV) data for each specified time interval. 
    If the candle does not exist, it will be created (upsert behavior).

    Args:
        trade (dict): Trade data containing at least:
            - "PDrCotVal" (int/float): Trade price
            - "QTotTran5J" (int): Trade volume
            - "InsCode" (str/int): Instrument/Symbol code
            - "received_at" (int): Timestamp of the trade in milliseconds
        intervals (list[str]): List of candle intervals to update (e.g., ["1m", "5m"]).
    """
    price = trade["PDrCotVal"]       # Trade price
    volume = trade["QTotTran5J"]     # Trade volume
    symbol = str(trade["InsCode"])   # Symbol code as string
    timestamp = trade["received_at"] # Timestamp in milliseconds

    for interval in intervals:
        # Round timestamp down to the nearest candle start time for this interval
        candle_time = round_timestamp(timestamp, interval)

        # Filter to find the existing candle for this symbol/interval/time
        filter = {
            "symbol": symbol,
            "interval": interval,
            "time": candle_time
        }

        # MongoDB update document
        update = {
            "$min": {"low": price},    # Update low if price is lower
            "$max": {"high": price},   # Update high if price is higher
            "$set": {
                "close": price,        # Always update the close price
                "volume": volume,      # Always update volume
                "last_updated": timestamp
            },
            "$setOnInsert": {          # Fields set only when inserting a new candle
                "open": price,         # First price becomes open
                "time": candle_time,
                "symbol": symbol,
                "interval": interval
            },
        }

        # Perform upsert in MongoDB (update or insert if not exists)
        db = get_db()
        await db["candles"].update_one(filter, update, upsert=True)
