from xml.etree import ElementTree
from datetime import datetime


def parse_trade_xml(xml_str: str, flow: int = 0) -> list[dict]:
    """
    Parse TradeLastDayResult XML from TSETMC into list of dicts.
    Each trade will have `flow` and `received_at` fields added.
    """
    try:
        root = ElementTree.fromstring(xml_str)
    except Exception as e:
        print("Error parsing XML:", e)
        return []

    trades = []

    # Find <diffgram> inside the root
    ns_diffgr = "{urn:schemas-microsoft-com:xml-diffgram-v1}"
    diffgram = root.find(f".//{ns_diffgr}diffgram")
    if diffgram is None:
        print("No diffgram found in XML.")
        return []

    trade_root = diffgram.find("TradeLastDay")
    if trade_root is None:
        print("No TradeLastDay found in diffgram.")
        return []

    for item in trade_root.findall("TradeLastDay"):
        data = {}
        for child in item:
            tag = child.tag.strip()
            text = child.text.strip() if child.text else ""
            data[tag] = try_cast(text)

        data["flow"] = flow
        data["received_at"] = int(datetime.now().timestamp() * 1000)
        trades.append(data)

    return trades


def try_cast(value: str):
    """Try to cast values to int or float when possible."""
    if value.isdigit():
        return int(value)
    try:
        return float(value)
    except ValueError:
        return value
