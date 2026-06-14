import socket
import threading
from datetime import datetime
import logging
# Nome dos participantes: [Seu Nome, Parceiro 1, Parceiro 2]

logging.basicConfig(filename='hora_server.log', level=logging.INFO, 
                    format='%(asctime)s - %(message)s')

def handle_client(client_socket, addr):
    """Thread por cliente."""
    try:
        client_socket.send(datetime.now().strftime("%H:%M:%S").encode('utf-8'))
        log_msg = f"Solicitação de {addr} atendida"
        print(log_msg)
        logging.info(log_msg)
    except Exception as e:
        print(f"Erro {addr}: {e}")
        logging.error(f"Erro {addr}: {e}")
    finally:
        client_socket.close()

HOST = 'localhost'
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
    thread.start()import socket
import threading
from datetime import datetime
import logging
# Nome dos participantes: [Seu Nome, Parceiro 1, Parceiro 2]

logging.basicConfig(filename='hora_server.log', level=logging.INFO, 
                    format='%(asctime)s - %(message)s')

def handle_client(client_socket, addr):
    """Thread por cliente."""
    try:
        client_socket.send(datetime.now().strftime("%H:%M:%S").encode('utf-8'))
        log_msg = f"Solicitação de {addr} atendida"
        print(log_msg)
        logging.info(log_msg)
    except Exception as e:
        print(f"Erro {addr}: {e}")
        logging.error(f"Erro {addr}: {e}")
    finally:
        client_socket.close()

HOST = 'localhost'
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