from fastapi import FastAPI
from app.routes import chart
from app.db.mongo import connect_to_mongo

app = FastAPI(title="TSETMC Stream to TradingView")


@app.on_event("startup")
async def startup():
    await connect_to_mongo()


app.include_router(chart.router, prefix="/technical/tv/chart")
