from fastapi import APIRouter, Query
from typing import Optional
from app.db.mongo import get_db

router = APIRouter()

@router.get("/technical/tv/chart/history")
async def get_chart_history(
    symbol: str = Query(...),
    from_timestamp: int = Query(..., alias="from"),
    to_timestamp: int = Query(..., alias="to"),
    resolution: str = Query(...),
    countback: Optional[int] = Query(None)
):
    db = get_db()

    candles_cursor = db["candles"].find({
        "symbol": symbol,
        "interval": resolution.lower(),
        "time": {
            "$gte": from_timestamp,
            "$lte": to_timestamp
        }
    }).sort("time", 1)

    bars = []
    async for c in candles_cursor:
        bars.append({
            "time": c["time"],
            "open": c["open"],
            "close": c["close"],
            "high": c["high"],
            "low": c["low"],
            "volume": c["volume"]
        })

    return {
        "status": "success",
        "data": {
            "status": "ok",
            "bars": bars
        }
    }
