# =============================================================================
# QUESTÃO 4 — Servidor de Hora TCP
# Ao conectar, envia a hora atual formatada (fuso America/Sao_Paulo) e encerra.
# Registra cada atendimento em arquivo de log (hora_server.log).
# Participantes: Gabriel Castro, Murilo Escobedo, Pávila Miranda, Humberto Freire
# =============================================================================

import os
import socket
import threading
from datetime import datetime
from zoneinfo import ZoneInfo  # Fuso horário (Python 3.9+)
import logging

# Fuso lido de TZ (Docker define TZ=America/Sao_Paulo no docker-compose)
TZ = ZoneInfo(os.getenv('TZ', 'America/Sao_Paulo'))

# Configura log em arquivo na pasta de execução do servidor
logging.basicConfig(
    filename='hora_server.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

def hora_atual():
    """Retorna hora local no fuso configurado, formato HH:MM:SS."""
    return datetime.now(TZ).strftime("%H:%M:%S")

def handle_client(client_socket, addr):
    """
    Atende um cliente: envia a hora uma vez e fecha a conexão.
    Cada solicitação roda em thread própria para suportar vários clientes.
    """
    try:
        # Envia string da hora codificada em UTF-8
        client_socket.send(hora_atual().encode('utf-8'))
        
        log_msg = f"Solicitação de {addr} atendida"
        print(log_msg)
        logging.info(log_msg)
        
    except Exception as e:
        print(f"Erro {addr}: {e}")
        logging.error(f"Erro {addr}: {e}")
    finally:
        client_socket.close()

# --- Servidor TCP na porta 7000 ---

HOST = '0.0.0.0'
PORT = 7000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(5)
print(f"Servidor hora em {HOST}:{PORT}")

while True:
    client, addr = server.accept()
    print(f"Cliente {addr} conectado")
    thread = threading.Thread(target=handle_client, args=(client, addr), daemon=True)
    thread.start()
