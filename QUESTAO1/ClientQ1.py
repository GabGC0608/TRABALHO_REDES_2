# =============================================================================
# QUESTÃO 1 — Cliente TCP
# Conecta ao servidor, envia mensagens digitadas pelo usuário e exibe respostas.
# Participantes: Gabriel Castro, Murilo Escobedo, Pávila Miranda, Humberto Freire
# =============================================================================

import os       # Permite ler variável de ambiente SERVER_HOST (útil no Docker)
import socket   # Comunicação TCP com o servidor

# Host do servidor: localhost por padrão; pode ser alterado via variável de ambiente
HOST = os.getenv('SERVER_HOST', 'localhost')
# Porta deve coincidir com a do ServerQ1.py e do docker-compose
PORT = 5000

# Cria socket TCP (IPv4, orientado a conexão)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Estabelece conexão com o servidor; falha se o servidor não estiver rodando
client.connect((HOST, PORT))

try:
    # Loop de interação: usuário digita mensagens até decidir sair
    while True:
        msg = input("Digite mensagem (ou Enter para sair): ")
        
        # Ignora mensagens vazias e pede nova entrada
        if not msg.strip():
            print("Mensagem vazia inválida!")
            continue
        
        # Envia a mensagem codificada em UTF-8 (bytes) pelo socket
        client.send(msg.encode('utf-8'))
        
        # Aguarda e exibe a resposta do servidor (até 1024 bytes)
        response = client.recv(1024).decode('utf-8')
        print(f"Servidor: {response}")
        
        # Comando 'sair' encerra o loop de envio
        if msg.lower() == 'sair':
            break
finally:
    # Fecha o socket mesmo se ocorrer interrupção (Ctrl+C) ou erro
    client.close()
