#!/usr/bin/env python3

import datetime
import asyncio
import pathlib
import ssl
import websockets

async def stipend_secure_websocket(websocket, path):
    while True:
        f = open("/path/to/stipendStatus.txt", 'r')
        ws_data = f.readline()
        f.close()
        await websocket.send(ws_data)
        await asyncio.sleep(3)

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
localhost_pem = pathlib.Path(__file__).with_name("ssl_key_here.key")
ssl_context.load_cert_chain("/path/to/ssl_cert_chain_here.pem","/path/to/ssl_key_here.key")

start_server = websockets.serve(stipend_secure_websocket, "0.0.0.0", 1234, ssl=ssl_context)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
