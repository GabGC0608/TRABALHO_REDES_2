import asyncio
import os
import websockets
# Nome dos participantes: [Seu Nome, Parceiro 1, Parceiro 2]

HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', '8765'))
clients = set()

async def handler(websocket):
    clients.add(websocket)
    try:
        async for message in websocket:
            for client in clients.copy():
                if client != websocket:
                    await client.send(message)
    finally:
        clients.remove(websocket)

async def main():
    async with websockets.serve(handler, HOST, PORT):
        print(f"Servidor WebSocket em ws://{HOST}:{PORT}")
        await asyncio.Future()

asyncio.run(main())