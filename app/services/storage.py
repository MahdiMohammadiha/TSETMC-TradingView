from datetime import datetime
from app.db.mongo import get_db


def get_today_collection_name(base: str) -> str:
    today = datetime.now().strftime("%Y%m%d")
    return f"{base}_{today}"


async def store_raw_trades(trades: list[dict]):
    if not trades:
        return

    collection_name = get_today_collection_name("raw_trades")
    db = get_db()
    await db[collection_name].insert_many(trades)
