# =============================================================================
# QUESTÃO 10 — Servidor WebSocket + HTTP estático
# Sobe dois serviços:
#   - HTTP na porta 8080: serve a página HTML do chat
#   - WebSocket na porta 8765: repassa mensagens entre clientes conectados
# Participantes: Gabriel Castro, Murilo Escobedo, Pávila Miranda, Humberto Freire
# =============================================================================

import asyncio
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

import websockets  # Biblioteca assíncrona para protocolo WebSocket

# Endereço de escuta (0.0.0.0 para aceitar conexões externas ao container)
HOST = os.getenv('HOST', '0.0.0.0')
# Porta do WebSocket — usada pela página em CientWebSocketPage.html
WS_PORT = int(os.getenv('PORT', '8765'))
# Porta do servidor HTTP que entrega os arquivos estáticos
HTTP_PORT = int(os.getenv('HTTP_PORT', '8080'))

# Conjunto de conexões WebSocket ativas (thread-safe com copy() no broadcast)
clients = set()

# Diretório onde estão ServerWebSocket.py e CientWebSocketPage.html
APP_DIR = Path(__file__).resolve().parent


class Handler(SimpleHTTPRequestHandler):
    """
    Handler HTTP customizado: serve arquivos da pasta APP_DIR.
    Redireciona / e /index.html para a página do chat WebSocket.
    """
    def __init__(self, *args, **kwargs):
        # directory= define a pasta raiz dos arquivos servidos
        super().__init__(*args, directory=str(APP_DIR), **kwargs)

    def do_GET(self):
        # Raiz do site abre diretamente a página do cliente WebSocket
        if self.path in ('/', '/index.html'):
            self.path = '/CientWebSocketPage.html'
        return super().do_GET()


def start_http_server():
    """
    Inicia servidor HTTP em thread separada (bloqueante).
    ThreadingHTTPServer atende várias requisições GET em paralelo.
    """
    server = ThreadingHTTPServer((HOST, HTTP_PORT), Handler)
    print(f"Pagina web em http://localhost:{HTTP_PORT}/")
    server.serve_forever()


async def websocket_handler(websocket):
    """
    Callback chamado para cada nova conexão WebSocket.
    Repassa cada mensagem recebida para todos os outros clientes (chat room).
    """
    clients.add(websocket)
    try:
        # async for itera sobre mensagens até o cliente desconectar
        async for message in websocket:
            # clients.copy() evita erro se o set mudar durante a iteração
            for client in clients.copy():
                if client != websocket:
                    await client.send(message)
    finally:
        clients.remove(websocket)


async def main():
    """
    Ponto de entrada assíncrono: HTTP em thread + WebSocket no event loop.
    """
    # HTTP roda em thread daemon para não bloquear o asyncio
    http_thread = Thread(target=start_http_server, daemon=True)
    http_thread.start()

    # websockets.serve registra o handler na porta WS_PORT
    async with websockets.serve(websocket_handler, HOST, WS_PORT):
        print(f"Servidor WebSocket em ws://localhost:{WS_PORT}")
        # Future que nunca completa — mantém o servidor rodando indefinidamente
        await asyncio.Future()


if __name__ == '__main__':
    asyncio.run(main())
