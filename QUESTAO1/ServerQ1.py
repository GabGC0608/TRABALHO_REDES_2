import socket
import threading
# Nome dos participantes: [Gabriel Castro, Murilo Escobedo, Pávila Miranda, Humberto Freire]

def handle_client(client_socket, addr):
    """Manipula cada cliente em thread separada."""
    try:
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data or data.strip() == '':  # Validação mensagem vazia
                break
            print(f"Mensagem de {addr}: {data}")
            response = "Mensagem recebida"
            client_socket.send(response.encode('utf-8'))
    except Exception as e:
        print(f"Erro com {addr}: {e}")
    finally:
        client_socket.close()
        print(f"Cliente {addr} desconectado")

# Configuração servidor
HOST = '0.0.0.0'
PORT = 5000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(5)
print(f"Servidor TCP escutando em {HOST}:{PORT}")

while True:
    client_socket, addr = server.accept()
    print(f"Conexão de {addr}")
    client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    client_thread.start()