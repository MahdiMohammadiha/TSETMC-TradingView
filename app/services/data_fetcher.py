import asyncio
from app.services.tsetmc_client import fetch_trade_data
from app.services.parser import parse_trade_xml
from app.services.storage import store_raw_trades
from app.services.aggregator import update_candles_from_trade
from app.services.scheduler import is_within_trading_hours, seconds_until_next_start


ERROR_RETRY_DELAY = 5  # Delay after encountering an error (in seconds)


async def fetch_loop(flow_id: int):
    """Main fetch loop for a specific data flow."""
    while True:
        try:
            if is_within_trading_hours():
                xml_str = await fetch_trade_data(flow=flow_id)
                trades = parse_trade_xml(xml_str, flow=flow_id)

                if trades:
                    await store_raw_trades(trades)
                    for trade in trades:
                        await update_candles_from_trade(
                            trade=trade, intervals=["1m", "5m"]
                        )

            else:
                sleep_sec = seconds_until_next_start()
                print(
                    f"[flow {flow_id}] Outside trading hours, sleeping for {sleep_sec} seconds"
                )
                await asyncio.sleep(sleep_sec)

        except Exception as e:
            print(f"[flow {flow_id}] Error: {e}")
            await asyncio.sleep(ERROR_RETRY_DELAY)


async def start_all_flows():
    """Start fetch loops for all data flows."""
    flows = [1, 2, 3, 4]
    for flow_id in flows:
        asyncio.create_task(fetch_loop(flow_id))
