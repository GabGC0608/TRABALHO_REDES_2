# =============================================================================
# QUESTÃO 2 — Cliente UDP
# Envia mensagens ao servidor de eco e exibe a resposta devolvida.
# Participantes: Gabriel Castro, Murilo Escobedo, Pávila Miranda, Humberto Freire
# =============================================================================

import os
import socket

# Endereço do servidor UDP (localhost quando rodando local ou via Docker)
HOST = os.getenv('SERVER_HOST', 'localhost')
PORT = 6000
MAX_SIZE = 65536  # Limite de tamanho do datagrama

# Socket UDP — não há connect() obrigatório; endereço é informado em cada sendto
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    while True:
        msg = input("Digite mensagem ('sair' para encerrar): ")
        
        if msg.lower() == 'sair':
            break
        
        # Verifica se a mensagem codificada não excede o limite UDP
        if len(msg.encode('utf-8')) > MAX_SIZE:
            print("Mensagem excede limite UDP!")
            continue
        
        # Envia datagrama para (HOST, PORT) sem estabelecer conexão
        udp_socket.sendto(msg.encode('utf-8'), (HOST, PORT))
        
        try:
            # Aguarda resposta do servidor (eco do mesmo conteúdo)
            data, _ = udp_socket.recvfrom(MAX_SIZE)
            print(f"Eco: {data.decode('utf-8')}")
        except socket.timeout:
            # UDP pode perder pacotes; timeout indica que não houve resposta a tempo
            print("Timeout - pacote perdido")
            # Define timeout de 5 segundos para próximas tentativas de recvfrom
            udp_socket.settimeout(5.0)
finally:
    udp_socket.close()
