import websockets
import json 
import asyncio
import logging

DISCORD_GATEWAY_URL = "wss://gateway.discord.gg/?v=10&encoding=json"
BOT_TOKEN = None

def connect(TOKEN,logging_level):
    global BOT_TOKEN
    BOT_TOKEN = TOKEN
    logging.basicConfig(level=logging.INFO)
    asyncio.run(listen())


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