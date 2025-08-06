import asyncio
import datetime
from app.services.tsetmc_client import fetch_trade_data
from app.services.parser import parse_trade_xml
from app.db.mongo import connect_to_mongo, get_db
from app.services.aggregator import update_candles_from_trade


async def debug_fetch_oce():
    await connect_to_mongo()
    db = get_db()

    flow_id = 3
    xml_str = await fetch_trade_data(flow=flow_id)

    if not xml_str:
        print("❌ No XML returned from fetch_trade_data")
        return

    trade_data_list = parse_trade_xml(xml_str, flow=flow_id)
    print(f"📦 Parsed {len(trade_data_list)} trades from flow {flow_id}")

    if not trade_data_list:
        print("⚠️ No trade data found after parsing")
        return

    today_str = datetime.datetime.now().strftime("%Y%m%d")
    collection_name = f"raw_trades_{today_str}"

    # ذخیره معاملات
    await db[collection_name].insert_many(trade_data_list)
    print(f"✅ Inserted {len(trade_data_list)} records into {collection_name}")

    # ساخت کندل برای هر معامله
    print("🔍 Sample trade:", trade_data_list[0])

    count = 0
    for trade in trade_data_list:
        await update_candles_from_trade(db, trade, intervals=["1m", "5m"])
        count += 1
        if count % 100 == 0:
            print(f"⏳ Processed {count} trades...")

    print("🏁 Candle generation complete")


if __name__ == "__main__":
    asyncio.run(debug_fetch_oce())
