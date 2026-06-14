# Trabalho de Redes 2

Projeto com exercícios de programação de redes em Python: TCP, UDP, chat multi-cliente, servidor de hora e WebSocket com interface web.

**Participantes:** Gabriel Castro, Murilo Escobedo, Pávila Miranda, Humberto Freire

---

## Pré-requisitos

- [Python 3.11+](https://www.python.org/downloads/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (opcional, para subir todos os serviços de uma vez)
- Dois terminais abertos (um para o servidor e outro para o cliente) ao testar manualmente

---

## Estrutura do projeto

| Pasta       | Protocolo   | Porta(s)     | Descrição                          |
|-------------|-------------|--------------|------------------------------------|
| `QUESTAO1/` | TCP         | 5000         | Servidor/cliente com confirmação     |
| `QUESTAO2/` | UDP         | 6000         | Servidor de eco UDP                |
| `QUESTAO3/` | TCP         | 5500         | Chat entre dois clientes           |
| `QUESTAO4/` | TCP         | 7000         | Servidor que retorna hora atual    |
| `QUESTAO10/`| WebSocket   | 8765 + 8080  | Chat em tempo real com página web  |

---

## Opção 1 — Rodar com Docker (recomendado)

Na raiz do projeto:

```bash
docker compose up --build
```

Para rodar em segundo plano:

```bash
docker compose up --build -d
```

Para parar:

```bash
docker compose down
```

### Testar com Docker em execução

Abra **terminais separados** e execute os clientes apontando para `localhost`:

**Questão 1 — TCP**

```bash
cd QUESTAO1
python ClientQ1.py
```

**Questão 2 — UDP**

```bash
cd QUESTAO2
python ClientUDP.py
```

**Questão 3 — Chat (precisa de 2 terminais)**

Terminal 1:

```bash
cd QUESTAO3
python ClientChat.py
```

Terminal 2:

```bash
cd QUESTAO3
python ClientChat.py
```

**Questão 4 — Hora**

```bash
cd QUESTAO4
python ClientHora.py
```

**Questão 10 — Web (navegador)**

Abra no navegador:

**http://localhost:8080/**

A página conecta automaticamente ao WebSocket em `ws://localhost:8765`. Abra várias abas ou janelas para simular vários usuários no chat.

---

## Opção 2 — Rodar localmente sem Docker

Em cada questão, use **dois terminais**: um para o servidor e outro para o cliente.

### Questão 1 — TCP (porta 5000)

**Terminal 1 — Servidor:**

```bash
cd QUESTAO1
python ServerQ1.py
```

**Terminal 2 — Cliente:**

```bash
cd QUESTAO1
python ClientQ1.py
```

Digite mensagens no cliente. O servidor responde `Mensagem recebida`. Digite `sair` para encerrar.

---

### Questão 2 — UDP eco (porta 6000)

**Terminal 1 — Servidor:**

```bash
cd QUESTAO2
python ServerUDP.py
```

**Terminal 2 — Cliente:**

```bash
cd QUESTAO2
python ClientUDP.py
```

O servidor devolve a mesma mensagem (eco). Digite `sair` no cliente para encerrar.

---

### Questão 3 — Chat TCP (porta 5500)

**Terminal 1 — Servidor:**

```bash
cd QUESTAO3
python ServerChat.py
```

**Terminal 2 e 3 — Dois clientes:**

```bash
cd QUESTAO3
python ClientChat.py
```

Conecte os dois clientes. As mensagens de um aparecem no outro. Digite `sair` para desconectar.

---

### Questão 4 — Servidor de hora (porta 7000)

**Terminal 1 — Servidor:**

```bash
cd QUESTAO4
python ServerHora.py
```

**Terminal 2 — Cliente:**

```bash
cd QUESTAO4
python ClientHora.py
```

O cliente exibe a hora atual (fuso `America/Sao_Paulo`). O servidor grava logs em `hora_server.log`.

---

### Questão 10 — WebSocket + página web

Instale a dependência (apenas na primeira vez):

```bash
cd QUESTAO10
pip install -r requirements.txt
```

**Terminal 1 — Servidor (HTTP + WebSocket):**

```bash
cd QUESTAO10
python ServerWebSocket.py
```

Saída esperada:

```
Pagina web em http://localhost:8080/
Servidor WebSocket em ws://localhost:8765
```

**Navegador:**

Acesse **http://localhost:8080/**

- Campo de texto + botão **Enviar** para mandar mensagens
- Mensagens de outros usuários aparecem na área `#messages`
- Abra a mesma URL em outra aba para testar o chat entre dois usuários

---

## Resumo das URLs e portas locais

| Serviço              | Endereço local              |
|----------------------|-----------------------------|
| Questão 1 (TCP)      | `localhost:5000`            |
| Questão 2 (UDP)      | `localhost:6000`            |
| Questão 3 (Chat)     | `localhost:5500`            |
| Questão 4 (Hora)     | `localhost:7000`            |
| Questão 10 (Web)     | **http://localhost:8080/**  |
| Questão 10 (WS)      | `ws://localhost:8765`       |

---

## Variáveis de ambiente (clientes)

Os clientes usam `SERVER_HOST` para apontar ao servidor quando ele não está em `localhost`:

```bash
# Windows PowerShell
$env:SERVER_HOST = "localhost"
python ClientQ1.py

# Linux/macOS
export SERVER_HOST=localhost
python ClientQ1.py
```

No Docker, os serviços já expõem as portas no host; os clientes locais continuam usando `localhost`.

---

## Dicas para testes

1. **Sempre inicie o servidor antes do cliente** — o cliente tenta conectar imediatamente.
2. **Questão 3** exige dois clientes conectados; o chat só repassa mensagens com pelo menos 2 participantes.
3. **Questão 10** — se a página não conectar, confira se `ServerWebSocket.py` está rodando e se as portas 8080 e 8765 estão livres.
4. **Firewall** — permita conexões locais nas portas listadas acima.
5. Use `Ctrl+C` no terminal do servidor para encerrá-lo.

---

## Solução de problemas

| Problema                         | Possível causa                    | Solução                                      |
|----------------------------------|-----------------------------------|----------------------------------------------|
| `Connection refused`             | Servidor não iniciado             | Rode o servidor no terminal 1 primeiro       |
| Porta já em uso                  | Outro processo na mesma porta     | Feche o processo ou pare o Docker (`down`)   |
| Chat Q3 não envia mensagens      | Apenas 1 cliente conectado        | Abra um segundo terminal com `ClientChat.py` |
| Página web Q10 em branco         | Servidor HTTP não subiu           | Verifique `python ServerWebSocket.py`        |
| WebSocket Q10 não conecta        | Porta 8765 bloqueada              | Libere a porta ou reinicie o servidor        |
