# =============================================================================
# QUESTÃO 4 — Cliente de Hora TCP
# Conecta ao servidor, recebe a hora atual e exibe no terminal.
# Participantes: Gabriel Castro, Murilo Escobedo, Pávila Miranda, Humberto Freire
# =============================================================================

import os
import socket

# Endereço do servidor de hora (localhost ou valor de SERVER_HOST)
HOST = os.getenv('SERVER_HOST', 'localhost')
PORT = 7000

# Socket TCP — conexão orientada a fluxo
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecta ao servidor; o servidor envia a hora assim que aceita a conexão
client.connect((HOST, PORT))

# Recebe até 1024 bytes (a hora cabe em poucos caracteres, ex: "14:30:45")
hora = client.recv(1024).decode('utf-8')
print(f"Hora atual: {hora}")

# Fecha a conexão após obter a resposta (protocolo request-response simples)
client.close()
