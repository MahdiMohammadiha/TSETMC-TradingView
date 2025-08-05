from lxml import etree
from datetime import datetime
from typing import Optional

def parse_trade_xml(xml_str: str, symbol_id: str) -> Optional[dict]:
    """
    Parses the XML and returns the latest daily candle for the given symbol_id.
    """
    root = etree.fromstring(xml_str.encode("utf-8"))
    trades = root.findall(".//Trade")

    for trade in trades:
        ins_code = trade.findtext("InsCode")
        if ins_code != symbol_id:
            continue

        date_raw = trade.findtext("DEven")  # e.g. "20250805"
        time_ts = int(datetime.strptime(date_raw, "%Y%m%d").timestamp()) * 1000

        return {
            "symbol": ins_code,
            "time": time_ts,
            "open": int(trade.findtext("PDrCotVal")),
            "close": int(trade.findtext("PClosing")),
            "high": int(trade.findtext("PHigh")),
            "low": int(trade.findtext("PLow")),
            "volume": int(trade.findtext("ZTotVol")),
        }

    return None
