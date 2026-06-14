import socket
import threading
# Nome dos participantes: [Seu Nome, Parceiro 1, Parceiro 2]

HOST = 'localhost'
PORT = 5500
clients = []  # Lista de clientes conectados

def broadcast(msg, sender):
    """Envia msg para todos exceto remetente."""
    for client in clients:
        if client != sender:
            try:
                client.send(msg.encode('utf-8'))
            except:
                clients.remove(client)

def handle_client(client_socket, addr):
    """Thread por cliente."""
    clients.append(client_socket)
    print(f"Cliente {addr} conectado. Total: {len(clients)}")
    
    while len(clients) < 2:
        pass  # Espera segundo cliente
    
    try:
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data or data == 'sair':
                break
            print(f"Chat {addr}: {data}")
            broadcast(data, client_socket)
    except:
        pass
    finally:
        clients.remove(client_socket)
        broadcast(f"{addr} saiu do chat", client_socket)
        client_socket.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(2)
print(f"Servidor chat em {HOST}:{PORT}")

while True:
    client, addr = server.accept()
    threading.Thread(target=handle_client, args=(client, addr), daemon=True).start()