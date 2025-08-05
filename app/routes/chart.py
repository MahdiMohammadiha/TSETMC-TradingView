from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from app.db.mongo import get_db

router = APIRouter()

@router.get("/history")
async def get_history(
    symbol: str = Query(...),
    _from: int = Query(..., alias="from"),
    to: int = Query(...),
    resolution: str = Query("1D"),
    countback: int = Query(500)
):
    if resolution != "1D":
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": "Only 1D resolution is supported in this version."}
        )

    from_ts = _from * 1000
    to_ts = to * 1000

    db = get_db()
    cursor = db["candles"].find({
        "symbol": symbol,
        "time": {"$gte": from_ts, "$lte": to_ts}
    }).sort("time", 1).limit(countback)

    bars = []
    async for doc in cursor:
        bars.append({
            "time": doc["time"],
            "open": doc["open"],
            "close": doc["close"],
            "high": doc["high"],
            "low": doc["low"],
            "volume": doc["volume"]
        })

    return {
        "status": "success",
        "data": {
            "status": "ok",
            "bars": bars
        }
    }
