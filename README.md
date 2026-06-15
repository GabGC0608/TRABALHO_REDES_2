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

## Rodar em 2 computadores (rede local)

Use um PC como **servidor** e o outro como **cliente**. Ambos devem estar na mesma rede (Wi‑Fi ou cabo) e o firewall do servidor deve permitir as portas usadas.

### Passo 1 — Descobrir o IP do PC servidor

No **PC servidor** (Windows PowerShell):

```powershell
ipconfig
```

Anote o **IPv4** da interface ativa (ex.: `192.168.1.10`). Nos exemplos abaixo, substitua por esse IP.

### Passo 2 — Liberar portas no firewall (PC servidor)

No Windows, permita entrada nas portas do exercício que você vai testar (ex.: 5000, 5500, 6000, 7000, 8080, 8765). Você pode criar regras no “Firewall do Windows” ou, em ambiente de laboratório, desativar temporariamente o firewall.

### Passo 3 — Rodar o servidor no PC servidor

**Sem Docker** — no PC servidor, inicie o servidor da questão (ex. Questão 1):

```bash
cd QUESTAO1
python ServerQ1.py
```

**Com Docker** — na raiz do projeto no PC servidor:

```bash
docker compose up --build
```

### Passo 4 — Rodar o cliente no PC cliente

No **segundo PC**, clone ou copie o projeto e aponte o cliente ao IP do servidor com `SERVER_HOST`:

**Windows PowerShell:**

```powershell
cd QUESTAO1
$env:SERVER_HOST = "192.168.1.10"
python ClientQ1.py
```

**Linux/macOS:**

```bash
cd QUESTAO1
export SERVER_HOST=192.168.1.10
python ClientQ1.py
```

O mesmo vale para os outros clientes (`ClientUDP.py`, `ClientChat.py`, `ClientHora.py`).

### Resumo por questão (2 PCs)

| Questão | PC servidor (roda) | PC cliente (roda) | Porta(s) no firewall |
|---------|--------------------|-------------------|----------------------|
| Q1 TCP | `ServerQ1.py` ou Docker | `ClientQ1.py` + `SERVER_HOST=IP` | 5000 |
| Q2 UDP | `ServerUDP.py` ou Docker | `ClientUDP.py` + `SERVER_HOST=IP` | 6000 (UDP) |
| Q3 Chat | `ServerChat.py` ou Docker | 2× `ClientChat.py` (pode ser 1 em cada PC) | 5500 |
| Q4 Hora | `ServerHora.py` ou Docker | `ClientHora.py` + `SERVER_HOST=IP` | 7000 |
| Q10 Web | `ServerWebSocket.py` ou Docker | Navegador em ambos os PCs | 8080 e 8765 |

### Questão 10 — Chat web em 2 PCs (detalhado)

1. **PC servidor** — instale dependências e suba o servidor:

```bash
cd QUESTAO10
pip install -r requirements.txt
python ServerWebSocket.py
```

O terminal mostrará algo como:

```
Pagina web (este PC):     http://localhost:8080/
Pagina web (outros PCs):  http://192.168.1.10:8080/
WebSocket (este PC):      ws://localhost:8765
WebSocket (outros PCs):   ws://192.168.1.10:8765
```

2. **PC servidor** — abra no navegador: `http://localhost:8080/`

3. **PC cliente** — abra no navegador: `http://192.168.1.10:8080/` (use o IP real do servidor)

4. A página usa automaticamente `window.location.hostname` para o WebSocket. Se você abre `http://192.168.1.10:8080/`, ela conecta em `ws://192.168.1.10:8765` — não precisa configurar nada no front.

5. Digite mensagens em um PC; elas aparecem no outro em tempo real.

**Importante:** não abra o arquivo `CientWebSocketPage.html` direto do disco (`file://`). Sempre use a URL HTTP do servidor (`http://IP:8080/`), senão o WebSocket não encontra o servidor.

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
| WebSocket Q10 não conecta        | Porta 8765 bloqueada ou página aberta via `file://` | Use `http://IP_SERVIDOR:8080/` e libere 8765 no firewall |
