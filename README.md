# 🤖 WhatsApp AI Bot

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![LangChain](https://img.shields.io/badge/LangChain-0.3.27-green.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--5-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

**Bot inteligente para WhatsApp com IA, RAG e integração com Google Calendar**

[Características](#-características) •
[Requisitos](#-requisitos) •
[Instalação](#-instalação) •
[Configuração](#-configuração) •
[Uso](#-uso) •
[Estrutura](#-estrutura-do-projeto)

</div>

---

## 📋 Sobre o Projeto

Bot de WhatsApp alimentado por IA que combina **GPT-5**, **RAG (Retrieval Augmented Generation)** e **Google Calendar** para fornecer respostas inteligentes e gerenciar compromissos automaticamente através do WhatsApp.

### 🎯 Características

- 🧠 **IA Avançada**: Utiliza GPT-5 da OpenAI para conversas naturais e contextuais
- 📚 **RAG Inteligente**: Base de conhecimento vetorial com ChromaDB para respostas precisas
- 📅 **Google Calendar**: Gerenciamento completo de eventos e compromissos
- 💬 **WhatsApp Business**: Integração via Evolution API
- 🎭 **Agente Autônomo**: Decide automaticamente qual ferramenta usar (RAG ou Calendar)
- 🧵 **Memória Contextual**: Mantém histórico de conversas com cada usuário
- 🚀 **Docker Ready**: Ambiente completo containerizado
- ⚡ **Buffer Inteligente**: Sistema de debounce para agrupar mensagens

---

## 🛠 Requisitos

### Software Necessário

- **Python 3.12+**
- **Docker & Docker Compose**
- **Git**
- **Conta Google** (para integração Calendar)
- **Chave API OpenAI**

### Dependências Principais

```
langchain==0.3.27
langchain-openai==0.3.33
langchain-chroma==0.2.5
chromadb==1.0.20
openai==1.107.1
google-api-python-client==2.147.0
fastapi==0.116.1
```

---

## 📦 Instalação

### 1. Clone o Repositório

```bash
git clone https://github.com/VictoOliv/whats-ai.git
cd whats-ai
```

### 2. Crie o Ambiente Virtual

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o Docker

```bash
docker-compose up -d
```

Isso iniciará:
- 🐘 **PostgreSQL** (porta 5432)
- 🔴 **Redis** (porta 6379)
- 📱 **Evolution API** (porta 8080)

---

## ⚙️ Configuração

### 1. Configure o Arquivo `.env`

Copie o arquivo de exemplo e edite com suas credenciais:

```bash
cp ".env copy" .env
```

**Variáveis Essenciais:**

```env
#Arquivo de prompts na raiz do projeto
PROMPTS_DIR=bot/prompts/

#Gpt
OPENAI_API_KEY=...  #Sua chave de api
OPENAI_MODEL_NAME=... #Modelo gpt
OPENAI_MODEL_TEMPERATURE=... #Temperatura do modelo

#Evolution API
EVOLUTION_API_URL=http://evolution-api:8080
EVOLUTION_INSTANCE_NAME=...
AUTHENTICATION_API_KEY=...
MANAGER_AUTHENTICATION_DISABLED=true
MANAGER_API_KEY=...
CONFIG_SESSION_PHONE_VERSION=2.3000.1030226392

#Postgres
DATABASE_ENABLED=true
DATABASE_PROVIDER=postgresql
DATABASE_CONNECTION_URI=...
DATABASE_CONNECTION_CLIENT_NAME=...
DATABASE_SAVE_DATA_INSTANCE=true
DATABASE_SAVE_DATA_NEW_MESSAGE=true
DATABASE_SAVE_MESSAGE_UPDATE=true
DATABASE_SAVE_DATA_CONTACTS=true
DATABASE_SAVE_DATA_CHATS=true
DATABASE_SAVE_DATA_LABELS=true
DATABASE_SAVE_DATA_HISTORIC=true

#Redis
CACHE_REDIS_ENABLED=false
CACHE_REDIS_URI=...
CACHE_REDIS_PREFIX_KEY=...
CACHE_REDIS_SAVE_INSTANCES=false
CACHE_LOCAL_ENABLED=false

#RAG
VECTOR_STORE_PATH=...
RAG_FILES_DIR=...

#Debounce de mensagens
BUFFER_KEY_SUFIX=...
DEBOUNCE_SECONDS=10
BUFFER_TTL=300

#Google calendário
ENABLE_GOOGLE_CALENDAR=true
```

### 2. Configure o Google Calendar (Opcional)

Para habilitar a integração com Google Calendar:

#### 2.1. Crie um Projeto no Google Cloud Console

1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um novo projeto
3. Ative a **Google Calendar API**

#### 2.2. Crie Credenciais OAuth 2.0

1. Vá em **APIs & Services** → **Credentials**
2. Clique em **Create Credentials** → **OAuth 2.0 Client ID**
3. Escolha **Desktop App**
4. Baixe o arquivo `credentials.json`

#### 2.3. Coloque as Credenciais

```bash
# Coloque o arquivo credentials.json na raiz do projeto
cp ~/Downloads/credentials.json .
```

#### 2.4. Configure Usuários de Teste

1. Em **OAuth consent screen**, adicione seu email como usuário de teste
2. Isso evitará erros de "App não verificado"

### 3. Prepare a Base de Conhecimento

Coloque seus documentos PDF na pasta apropriada:

```
rag_files/
└── processed/
    ├── categoria1/
    │   └── documento1.pdf
    ├── categoria2/
    │   └── documento2.pdf
    └── ...
```

---

## 🚀 Uso

### Inicie o Bot

```bash
python main.py
```

Na primeira execução com Google Calendar habilitado:
1. Uma janela do navegador abrirá
2. Faça login com sua conta Google
3. Autorize o acesso ao Calendar
4. O arquivo `token.pickle` será criado automaticamente

### Conecte o WhatsApp

1. Acesse a Evolution API: `http://localhost:8080`
2. Crie uma instância com o nome configurado em `.env`
3. Escaneie o QR Code com seu WhatsApp
4. Pronto! O bot está online 🎉

### Exemplos de Uso

#### 💬 Conversas Gerais
```
Usuário: Olá!
Bot: Olá! Como posso ajudá-lo hoje?
```

#### 📚 Consultas RAG (Base de Conhecimento)
```
Usuário: Quais são as atividades extracurriculares?
Bot: [Resposta baseada nos documentos PDF processados]
```

#### 📅 Gerenciamento de Agenda
```
Usuário: Quais são meus compromissos de hoje?
Bot: Você tem 2 eventos hoje:
- 10:00 - Reunião com cliente
- 15:30 - Apresentação projeto

Usuário: Crie um evento "Dentista" amanhã às 14h
Bot: ✅ Evento criado com sucesso!

Usuário: Buscar eventos sobre reunião
Bot: Encontrei 3 eventos com "reunião"...
```

---

## 📁 Estrutura do Projeto

```
whats_ai/
├── bot/
│   └── prompts/              # Prompts do sistema e contextualização
│       ├── system.txt
│       └── contextualize.txt
├── rag_files/
│   └── processed/            # Documentos PDF para RAG
├── vectorstore/              # Base vetorial ChromaDB
├── calendar_tools.py         # Ferramentas Google Calendar
├── chains.py                 # Chains e Agent LangChain
├── config.py                 # Configurações do projeto
├── env_loader.py             # Carregamento de variáveis .env
├── evolution_api.py          # Integração Evolution API
├── main.py                   # Ponto de entrada principal
├── memory.py                 # Gerenciamento de memória/histórico
├── message_buffer.py         # Buffer de mensagens com debounce
├── prompts.py                # Carregamento de prompts
├── vectorstore.py            # Configuração ChromaDB
├── docker-compose.yml        # Orquestração Docker
├── Dockerfile                # Build do container
├── requirements.txt          # Dependências Python
└── .env                      # Variáveis de ambiente (criar)
```

---

## 🔧 Testes

### Teste Manual Básico

```bash
python test_manual.py
```

### Teste de Diagnóstico

```bash
python test_diagnostico.py
```

---

## 🐛 Solução de Problemas

### ❌ "credentials.json não encontrado"
**Solução:** Coloque o arquivo `credentials.json` na raiz do projeto.

### ❌ "App não verificado" no Google
**Solução:** 
- Adicione seu email como usuário de teste no Google Cloud Console
- Clique em "Avançar" → "Ir para [Nome do App]"

### ❌ Evolution API não conecta
**Solução:**
```bash
docker-compose down
docker-compose up -d
docker-compose logs -f evolution-api
```

### ❌ "Erro 403/401" no Google Calendar
**Solução:**
```bash
# Delete o token e refaça autenticação
rm token.pickle
python main.py
```

### ❌ Bot não responde
**Solução:**
- Verifique se o Docker está rodando: `docker-compose ps`
- Verifique os logs: `docker-compose logs -f`
- Confirme que o WhatsApp está conectado na Evolution API

---

## 🏗️ Arquitetura

```
┌─────────────────┐
│   WhatsApp      │
│   (Usuário)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Evolution API  │
│  (WebSocket)    │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│        Message Buffer               │
│   (Debounce + Agrupamento)          │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│      LangChain Agent                │
│   (Decisão Inteligente)             │
└─────┬───────────────────────┬───────┘
      │                       │
      ▼                       ▼
┌─────────────┐      ┌──────────────────┐
│   RAG       │      │ Google Calendar  │
│ (ChromaDB)  │      │   (Tools API)    │
└─────────────┘      └──────────────────┘
      │                       │
      └───────────┬───────────┘
                  │
                  ▼
            ┌─────────┐
            │   GPT   │
            │ Response│
            └─────────┘
```

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer um Fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abrir um Pull Request

---

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

## 👨‍💻 Autor

**Victor Oliveira**

- GitHub: [@VictoOliv](https://github.com/VictoOliv)
- Projeto: [whats-ai](https://github.com/VictoOliv/whats-ai)

---

## 🙏 Agradecimentos

- [LangChain](https://langchain.com/) - Framework de IA
- [OpenAI](https://openai.com/) - Modelos GPT
- [Evolution API](https://evolution-api.com/) - WhatsApp Business API
- [ChromaDB](https://www.trychroma.com/) - Vector Database

---

<div align="center">

**Feito com ❤️ e ☕**

⭐ Se este projeto foi útil, considere dar uma estrela!

</div>

