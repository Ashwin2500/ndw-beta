import websockets
import json
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

DISCORD_GATEWAY_URL = "wss://gateway.discord.gg/?v=10&encoding=json"
BOT_TOKEN = "MTI3MTQ5MDg3MTIyNDk2MzIyMw.GOZa1_.k9lz-VM_xlumBTyMdDN9ivAkGxH7yr4mdQeZX0"

async def heartbeat(ws, interval, sequence):
    while True:
        payload = {
            "op" : 1,
            "d" : sequence
        }
        await ws.send(json.dumps(payload))
        logging.info("Heartbeat sent")
        await asyncio.sleep(interval)

async def identify(ws):
    payload ={
        "op" : 2,
        "d" : {
            "token": BOT_TOKEN,
            "intents": 513,
            "properties": {
                "$os": "linux",
                "$browser": "my_library",
                "$device": "my_library"
            }
        }
    }
    await ws.send(json.dumps(payload))
    logging.info("Identify payload sent")

async def listen():
    async with websockets.connect(DISCORD_GATEWAY_URL) as ws:
        event = json.loads(await ws.recv())
        logging.info(f"Recived event: {event}")
        
        heartbeat_interval = event['d']['heartbeat_interval']/1000
        asyncio.create_task(heartbeat(ws,heartbeat_interval,None))

        await identify(ws)

        while True:
            try:
                event = json.loads(await ws.recv())
                logging.info(f"Recived event: {event}")
            except websockets.exceptions.ConnectionClosed:
                logging.warning("Connection closed, reconnecting")
                break

asyncio.run(listen())