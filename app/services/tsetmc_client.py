import httpx
from app.core.config import settings
from lxml import etree


def build_soap_envelope():
    return f"""<?xml version="1.0" encoding="utf-8"?>
    <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                     xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                     xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
      <soap12:Body>
        <TradeLastDay xmlns="http://tsetmc.com/">
          <UserName>{settings.tsetmc_username}</UserName>
          <Password>{settings.tsetmc_password}</Password>
          <Flow>1</Flow>
        </TradeLastDay>
      </soap12:Body>
    </soap12:Envelope>"""


async def fetch_trade_data():
    headers = {"Content-Type": "application/soap+xml; charset=utf-8"}
    body = build_soap_envelope()

    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.post(
            "http://service.tsetmc.com/WebService/TsePublicV2.asmx",
            data=body,
            headers=headers,
        )

    if response.status_code != 200:
        raise RuntimeError(f"TSETMC API error: {response.status_code}")

    xml_root = etree.fromstring(response.content)
    ns = {
        "soap": "http://www.w3.org/2003/05/soap-envelope",
        "tsetmc": "http://tsetmc.com/"
    }

    result_element = xml_root.find(".//soap:Body/tsetmc:TradeLastDayResponse/tsetmc:TradeLastDayResult", namespaces=ns)

    if result_element is None:
        print("⚠️ TradeLastDayResult not found")
        return None

    inner_xml_bytes = etree.tostring(result_element, encoding="utf-8", method="xml")
    inner_xml_str = inner_xml_bytes.decode("utf-8")

    return inner_xml_str
