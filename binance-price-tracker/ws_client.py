import asyncio
import websockets
import json
from db import get_connection
from datetime import datetime

symbols = ["btcusdt", "ethusdt"]

async def binance_ws():
    url = f"wss://stream.binance.com:9443/stream?streams=" + "/".join([f"{s}@trade" for s in symbols])
    async with websockets.connect(url) as ws:
        while True:
            msg = await ws.recv()
            data = json.loads(msg)["data"]
            symbol = data["s"]
            price = float(data["p"])
            ts = datetime.utcfromtimestamp(data["T"] / 1000)

            conn = get_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO prices (symbol, price, timestamp) VALUES (%s, %s, %s)",
                        (symbol, price, ts))
            conn.commit()
            conn.close()

            print(f"{symbol} @ {ts} → {price}")

asyncio.run(binance_ws())
