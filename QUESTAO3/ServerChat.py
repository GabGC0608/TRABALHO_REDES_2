# =============================================================================
# QUESTÃO 3 — Servidor de Chat TCP
# Repassa mensagens entre clientes conectados (broadcast exceto o remetente).
# Requer pelo menos 2 clientes para o chat funcionar plenamente.
# Participantes: Gabriel Castro, Murilo Escobedo, Pávila Miranda, Humberto Freire
# =============================================================================

import socket
import threading

HOST = '0.0.0.0'
PORT = 5500

# Lista compartilhada entre threads com os sockets de todos os clientes ativos
clients = []

def broadcast(msg, sender):
    """
    Envia uma mensagem para todos os clientes conectados, exceto quem enviou.
    
    Parâmetros:
        msg: texto a ser transmitido
        sender: socket do cliente remetente (será excluído do envio)
    """
    for client in clients:
        if client != sender:
            try:
                client.send(msg.encode('utf-8'))
            except:
                # Remove clientes cuja conexão falhou (desconectados)
                clients.remove(client)

def handle_client(client_socket, addr):
    """
    Gerencia um cliente: recebe mensagens e faz broadcast para os demais.
    Executada em thread separada por conexão.
    """
    # Registra o novo cliente na lista global
    clients.append(client_socket)
    print(f"Cliente {addr} conectado. Total: {len(clients)}")
    
    # Aguarda ativamente até existir um segundo participante no chat
    while len(clients) < 2:
        pass
    
    try:
        while True:
            # Recebe mensagem do cliente (bloqueante)
            data = client_socket.recv(1024).decode('utf-8')
            
            # Encerra se não houver dados ou se o cliente enviar 'sair'
            if not data or data == 'sair':
                break
            
            print(f"Chat {addr}: {data}")
            # Repassa a mensagem para os outros participantes
            broadcast(data, client_socket)
    except:
        # Erro de conexão (cliente fechou abruptamente)
        pass
    finally:
        # Remove da lista, avisa os outros e fecha o socket
        clients.remove(client_socket)
        broadcast(f"{addr} saiu do chat", client_socket)
        client_socket.close()

# --- Inicialização do servidor de chat ---

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(2)  # Fila pequena — chat pensado para 2 clientes
print(f"Servidor chat em {HOST}:{PORT}")

while True:
    client, addr = server.accept()
    # daemon=True: thread encerra quando o programa principal terminar
    threading.Thread(target=handle_client, args=(client, addr), daemon=True).start()
