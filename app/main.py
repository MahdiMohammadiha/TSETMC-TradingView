from fastapi import FastAPI
from app.routers import chart
from app.db.mongo import connect_to_mongo
from app.services.data_fetcher import start_all_flows


app = FastAPI(title="TSETMC Stream to TradingView")
app.include_router(chart.router)


@app.on_event("startup")
async def startup():
    await connect_to_mongo()
    await start_all_flows()
