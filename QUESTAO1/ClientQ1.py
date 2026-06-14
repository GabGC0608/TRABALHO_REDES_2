import socket
# Nome dos participantes: [Seu Nome, Parceiro 1, Parceiro 2]

HOST = 'localhost'
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

try:
    while True:
        msg = input("Digite mensagem (ou Enter para sair): ")
        if not msg.strip():  # Validação vazia
            print("Mensagem vazia inválida!")
            continue
        client.send(msg.encode('utf-8'))
        response = client.recv(1024).decode('utf-8')
        print(f"Servidor: {response}")
        if msg.lower() == 'sair':
            break
finally:
    client.close()