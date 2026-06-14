# =============================================================================
# QUESTÃO 3 — Cliente de Chat TCP
# Conecta ao servidor de chat; envia mensagens e recebe as dos outros em thread.
# Participantes: Gabriel Castro, Murilo Escobedo, Pávila Miranda, Humberto Freire
# =============================================================================

import os
import socket
import threading

HOST = os.getenv('SERVER_HOST', 'localhost')
PORT = 5500

def receive_messages(client):
    """
    Thread dedicada à recepção de mensagens do servidor.
    Permite digitar e receber ao mesmo tempo (entrada não bloqueia saída).
    
    Parâmetros:
        client: socket TCP conectado ao servidor
    """
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')
            if not msg:
                break
            # \n no início para não misturar com o prompt "Você: "
            print(f"\nMensagem: {msg}")
        except:
            break

# Cria e conecta socket TCP ao servidor de chat
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Inicia thread em background para escutar mensagens vindas do servidor
recv_thread = threading.Thread(target=receive_messages, args=(client,), daemon=True)
recv_thread.start()

try:
    while True:
        msg = input("\nVocê: ")
        
        if msg.lower() == 'sair':
            # Informa o servidor antes de encerrar
            client.send(msg.encode('utf-8'))
            break
        
        # Envia mensagem para o servidor (que fará broadcast aos outros)
        client.send(msg.encode('utf-8'))
finally:
    client.close()
