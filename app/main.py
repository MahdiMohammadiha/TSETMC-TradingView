from fastapi import FastAPI
from app.routes import chart
from app.db.mongo import connect_to_mongo
from app.services.fetch_loop import start_all_flows


app = FastAPI(title="TSETMC Stream to TradingView")


@app.on_event("startup")
async def startup():
    await connect_to_mongo()
    await start_all_flows()


app.include_router(chart.router, prefix="/technical/tv/chart")
