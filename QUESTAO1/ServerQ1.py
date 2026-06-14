# =============================================================================
# QUESTÃO 1 — Servidor TCP
# Recebe mensagens de clientes via socket TCP e responde com confirmação.
# Cada cliente é atendido em uma thread separada (concorrência).
# Participantes: Gabriel Castro, Murilo Escobedo, Pávila Miranda, Humberto Freire
# =============================================================================

import socket      # Módulo padrão para comunicação em rede (sockets TCP/UDP)
import threading   # Permite atender vários clientes simultaneamente em threads

def handle_client(client_socket, addr):
    """
    Trata a comunicação com um único cliente conectado.
    
    Parâmetros:
        client_socket: socket já conectado ao cliente
        addr: tupla (IP, porta) de origem da conexão
    """
    try:
        # Loop infinito enquanto o cliente permanecer conectado e enviar dados
        while True:
            # Recebe até 1024 bytes e decodifica de bytes para string UTF-8
            data = client_socket.recv(1024).decode('utf-8')
            
            # Se não houver dados ou a mensagem for só espaços, encerra a conexão
            if not data or data.strip() == '':
                break
            
            # Exibe no terminal do servidor quem enviou e o conteúdo
            print(f"Mensagem de {addr}: {data}")
            
            # Monta resposta padrão de confirmação e envia ao cliente
            response = "Mensagem recebida"
            client_socket.send(response.encode('utf-8'))
            
    except Exception as e:
        # Captura erros de rede (cliente desconectou abruptamente, etc.)
        print(f"Erro com {addr}: {e}")
    finally:
        # Garante fechamento do socket e informa desconexão no log
        client_socket.close()
        print(f"Cliente {addr} desconectado")

# --- Configuração e inicialização do servidor ---

# 0.0.0.0 = escuta em todas as interfaces de rede (necessário no Docker)
HOST = '0.0.0.0'
# Porta TCP exposta no docker-compose (5000:5000)
PORT = 5000

# Cria socket IPv4 (AF_INET) orientado a conexão (SOCK_STREAM = TCP)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# SO_REUSEADDR permite reutilizar a porta imediatamente após reiniciar o servidor
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Associa o socket ao endereço IP e porta
server.bind((HOST, PORT))

# Coloca o socket em modo escuta; fila de até 5 conexões pendentes
server.listen(5)
print(f"Servidor TCP escutando em {HOST}:{PORT}")

# Loop principal: aceita novas conexões indefinidamente
while True:
    # accept() bloqueia até um cliente conectar; retorna socket do cliente e endereço
    client_socket, addr = server.accept()
    print(f"Conexão de {addr}")
    
    # Cria thread para não bloquear o accept() enquanto atende o cliente anterior
    client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    client_thread.start()
