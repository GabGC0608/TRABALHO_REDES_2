import os
import socket
# Nome dos participantes: [Gabriel Castro, Murilo Escobedo, Pávila Miranda, Humberto Freire]

HOST = os.getenv('SERVER_HOST', 'localhost')
PORT = 6000
MAX_SIZE = 65536

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    while True:
        msg = input("Digite mensagem ('sair' para encerrar): ")
        if msg.lower() == 'sair':
            break
        if len(msg.encode('utf-8')) > MAX_SIZE:
            print("Mensagem excede limite UDP!")
            continue
        udp_socket.sendto(msg.encode('utf-8'), (HOST, PORT))
        try:
            data, _ = udp_socket.recvfrom(MAX_SIZE)
            print(f"Eco: {data.decode('utf-8')}")
        except socket.timeout:
            print("Timeout - pacote perdido")
            udp_socket.settimeout(5.0)
finally:
    udp_socket.close()