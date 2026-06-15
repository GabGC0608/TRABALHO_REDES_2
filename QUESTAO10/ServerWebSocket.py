# =============================================================================
# QUESTÃO 10 — Servidor WebSocket + HTTP (Flask) para o front-end
# Sobe dois serviços:
#   - HTTP na porta 8080: Flask serve a página HTML do chat
#   - WebSocket na porta 8765: repassa mensagens entre clientes conectados
# Participantes: Gabriel Castro, Murilo Escobedo, Pávila Miranda, Humberto Freire
# =============================================================================

import asyncio
import os
import socket
from pathlib import Path
from threading import Thread

import websockets
from flask import Flask, send_from_directory

# Endereço de escuta (0.0.0.0 = aceita conexões de outros PCs na rede)
HOST = os.getenv('HOST', '0.0.0.0')
WS_PORT = int(os.getenv('PORT', '8765'))
HTTP_PORT = int(os.getenv('HTTP_PORT', '8080'))

clients = set()
APP_DIR = Path(__file__).resolve().parent


def get_local_ip():
    """Descobre o IP da máquina na rede local (útil para acessar de outro PC)."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(('8.8.8.8', 80))
            return s.getsockname()[0]
    except OSError:
        return '127.0.0.1'


def create_flask_app():
    """Cria app Flask que entrega a página web do chat."""
    app = Flask(__name__)

    @app.route('/')
    @app.route('/index.html')
    def index():
        return send_from_directory(APP_DIR, 'CientWebSocketPage.html')

    return app


def start_http_server():
    """Inicia Flask em thread separada para servir o front-end HTML/JS."""
    app = create_flask_app()
    local_ip = get_local_ip()
    print(f"Pagina web (este PC):     http://localhost:{HTTP_PORT}/")
    print(f"Pagina web (outros PCs):  http://{local_ip}:{HTTP_PORT}/")
    app.run(host=HOST, port=HTTP_PORT, threaded=True, use_reloader=False)


async def websocket_handler(websocket):
    """Repassa cada mensagem recebida para todos os outros clientes WebSocket."""
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

    local_ip = get_local_ip()
    async with websockets.serve(websocket_handler, HOST, WS_PORT):
        print(f"WebSocket (este PC):      ws://localhost:{WS_PORT}")
        print(f"WebSocket (outros PCs):   ws://{local_ip}:{WS_PORT}")
        await asyncio.Future()


if __name__ == '__main__':
    asyncio.run(main())
