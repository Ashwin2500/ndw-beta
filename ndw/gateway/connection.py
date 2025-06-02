import websockets
import json
import asyncio
import logging
from .handler import set_user_handelers, handle

DISCORD_GATEWAY_URL = "wss://gateway.discord.gg/?v=10&encoding=json"

RECONNECT_URL = None
session_id = None
seq = None
recon = False
BOT_TOKEN = None

async def heartbeat(ws, interval):
    global seq
    while True:
        payload = {
            "op": 1,
            "d": seq
        }
        await ws.send(json.dumps(payload))
        logging.debug("Heartbeat sent")
        await asyncio.sleep(interval)

async def identify(ws):
    payload = {
        "op": 2,
        "d": {
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
    logging.debug("Identify payload sent")

async def resume(ws):
    payload = {
        "op": 6,
        "d": {
            "token": BOT_TOKEN,
            "session_id": session_id,
            "seq": seq
        }
    }
    await ws.send(json.dumps(payload))
    logging.debug("Resume payload sent")

async def listen(url, use_resume=False):
    global RECONNECT_URL, session_id, seq, recon, bot_obj
    async with websockets.connect(url) as ws:
        event = json.loads(await ws.recv())
        logging.debug(f"Received HELLO event: {event}")

        heartbeat_interval = event['d']['heartbeat_interval'] / 1000
        asyncio.create_task(heartbeat(ws, heartbeat_interval))

        if use_resume and session_id:
            await resume(ws)
        else:
            await identify(ws)

        while True:
            try:
                event = json.loads(await ws.recv())
                logging.debug(f"Received event: {event}")
                seq = event.get("s", seq)

                if event.get("t") == "READY":
                    RECONNECT_URL = event['d']['resume_gateway_url']
                    session_id = event['d']['session_id']
                    logging.info(f"Session ID: {session_id}")

                if event.get("op") == 7:
                    recon = True
                    logging.warning("Reconnecting")
                    break

                await handle(event, bot_obj)

            except websockets.exceptions.ConnectionClosed as e:
                logging.info(f"Connection closed: {e.code} - {e.reason}")
                codes = [4004, 4010, 4011, 4012, 4013, 4014]
                if e.code in codes:
                    logging.error(f"Connection closed: {e.reason}")
                    break
                else:
                    recon = True
                break

def connect(token, logging_level, user_handlers, bot):
    global BOT_TOKEN, recon, bot_obj
    bot_obj = bot
    BOT_TOKEN = token
    level_map = {
        10: logging.DEBUG,
        20: logging.INFO,
        30: logging.WARNING,
        40: logging.ERROR,
        50: logging.CRITICAL
        }
    logging.basicConfig(level=level_map.get(logging_level))

    set_user_handelers(user_handlers)

    asyncio.run(listen(DISCORD_GATEWAY_URL))

    while recon:
        logging.warning("Reconnecting...")
        recon = False
        asyncio.run(listen(RECONNECT_URL, use_resume=True))