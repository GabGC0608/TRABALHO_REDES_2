import socket
# Nome dos participantes: [Seu Nome, Parceiro 1, Parceiro 2]

HOST = '0.0.0.0'
PORT = 6000
MAX_SIZE = 65536  # Limite UDP

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind((HOST, PORT))
print(f"Servidor UDP eco em {HOST}:{PORT}")

try:
    while True:
        data, addr = udp_socket.recvfrom(MAX_SIZE)
        msg = data.decode('utf-8')
        print(f"Recebido de {addr}: {msg}")
        if len(msg) > MAX_SIZE:
            udp_socket.sendto("Mensagem muito grande!".encode('utf-8'), addr)
        else:
            udp_socket.sendto(data, addr)  # Eco
except KeyboardInterrupt:
    pass
finally:
    udp_socket.close()