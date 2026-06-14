import os
import socket
import threading
# Nome dos participantes: [Gabriel Castro, Murilo Escobedo, Pávila Miranda, Humberto Freire]

HOST = os.getenv('SERVER_HOST', 'localhost')
PORT = 5500

def receive_messages(client):
    """Thread para receber msgs."""
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')
            if not msg:
                break
            print(f"\nMensagem: {msg}")
        except:
            break

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

recv_thread = threading.Thread(target=receive_messages, args=(client,), daemon=True)
recv_thread.start()

try:
    while True:
        msg = input("\nVocê: ")
        if msg.lower() == 'sair':
            client.send(msg.encode('utf-8'))
            break
        client.send(msg.encode('utf-8'))
finally:
    client.close()