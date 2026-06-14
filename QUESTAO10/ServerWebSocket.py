import asyncio
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

import websockets
# Nome dos participantes: [Gabriel Castro, Murilo Escobedo, Pávila Miranda, Humberto Freire]


HOST = os.getenv('HOST', '0.0.0.0')
WS_PORT = int(os.getenv('PORT', '8765'))
HTTP_PORT = int(os.getenv('HTTP_PORT', '8080'))

clients = set()
APP_DIR = Path(__file__).resolve().parent


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(APP_DIR), **kwargs)

    def do_GET(self):
        if self.path in ('/', '/index.html'):
            self.path = '/CientWebSocketPage.html'
        return super().do_GET()


def start_http_server():
    server = ThreadingHTTPServer((HOST, HTTP_PORT), Handler)
    print(f"Pagina web em http://localhost:{HTTP_PORT}/")
    server.serve_forever()


async def websocket_handler(websocket):
    clients.add(websocket)
    try:
        async for message in websocket:
            for client in clients.copy():
                if client != websocket:
                    await client.send(message)
    finally:
        clients.remove(websocket)


async def main():
    http_thread = Thread(target=start_http_server, daemon=True)
    http_thread.start()

    async with websockets.serve(websocket_handler, HOST, WS_PORT):
        print(f"Servidor WebSocket em ws://localhost:{WS_PORT}")
        await asyncio.Future()


if __name__ == '__main__':
    asyncio.run(main())
