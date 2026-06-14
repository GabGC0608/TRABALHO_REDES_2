# =============================================================================
# QUESTÃO 2 — Servidor UDP (eco)
# Recebe datagramas UDP e devolve o mesmo conteúdo ao remetente (servidor de eco).
# UDP não garante entrega nem ordem — cada pacote é independente.
# Participantes: Gabriel Castro, Murilo Escobedo, Pávila Miranda, Humberto Freire
# =============================================================================

import socket

# Escuta em todas as interfaces (0.0.0.0) — padrão para containers Docker
HOST = '0.0.0.0'
# Porta UDP mapeada no docker-compose como 6000:6000/udp
PORT = 6000

# Tamanho máximo de datagrama UDP em bytes (65536 é o limite teórico comum)
MAX_SIZE = 65536

# SOCK_DGRAM = socket datagrama (UDP), sem conexão prévia
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Vincula o socket à porta UDP especificada
udp_socket.bind((HOST, PORT))
print(f"Servidor UDP eco em {HOST}:{PORT}")

try:
    # Loop infinito aguardando pacotes UDP
    while True:
        # recvfrom bloqueia até chegar um datagrama; retorna dados e endereço do remetente
        data, addr = udp_socket.recvfrom(MAX_SIZE)
        
        # Converte bytes recebidos em string para exibição e validação
        msg = data.decode('utf-8')
        print(f"Recebido de {addr}: {msg}")
        
        # Validação de tamanho (após decode; em produção validaria len(data))
        if len(msg) > MAX_SIZE:
            udp_socket.sendto("Mensagem muito grande!".encode('utf-8'), addr)
        else:
            # Eco: reenvia os mesmos bytes (data) de volta ao endereço de origem
            udp_socket.sendto(data, addr)
            
except KeyboardInterrupt:
    # Ctrl+C no terminal encerra o servidor graciosamente
    pass
finally:
    # Libera o recurso de rede
    udp_socket.close()
