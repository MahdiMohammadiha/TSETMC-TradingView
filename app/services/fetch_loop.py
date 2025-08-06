import asyncio
from app.services.tsetmc_client import fetch_trade_data
from app.services.parser import parse_trade_xml
from app.services.storage import store_raw_trades
from app.services.aggregator import update_candles_from_trade


async def fetch_loop(flow_id: int):
    while True:
        try:
            xml_str = await fetch_trade_data(flow=flow_id)
            trades = parse_trade_xml(xml_str, flow=flow_id)
            if trades:
                await store_raw_trades(trades)

                for trade in trades:
                    await update_candles_from_trade(trade=trade, intervals=["1m", "5m"])

        except Exception as e:
            print(f"[flow {flow_id}] Error:", e)

        await asyncio.sleep(2)


async def start_all_flows():
    for flow_id in range(1, 5):
        asyncio.create_task(fetch_loop(flow_id))
