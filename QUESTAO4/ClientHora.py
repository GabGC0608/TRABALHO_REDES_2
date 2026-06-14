import os
import socket
# Nome dos participantes: [Seu Nome, Parceiro 1, Parceiro 2]

HOST = os.getenv('SERVER_HOST', 'localhost')
PORT = 7000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
hora = client.recv(1024).decode('utf-8')
print(f"Hora atual: {hora}")
client.close()