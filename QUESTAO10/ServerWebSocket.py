import asyncio
import websockets
import json
# Nome dos participantes: [Seu Nome, Parceiro 1, Parceiro 2]

clients = set()

async def handler(websocket, path):
    clients.add(websocket)
    try:
        async for message in websocket:
            for client in clients.copy():
                if client != websocket:
                    await client.send(message)
    finally:
        clients.remove(websocket)

start_server = websockets.serve(handler, "localhost", 8765)
print("Servidor WebSocket em ws://localhost:8765")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()