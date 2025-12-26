#!/usr/bin/env python3
import os
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

# Diretório dos prompts dentro do container
# Variáveis de ambiente
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY não encontrada. Configure no arquivo .env")
OPENAI_MODEL_NAME = os.getenv('OPENAI_MODEL_NAME', 'gpt-5')  # Modelo mais avançado (GPT-5)
OPENAI_MODEL_TEMPERATURE = os.getenv('OPENAI_MODEL_TEMPERATURE', '0.7')  # Aumentado para GPT-5 (mais natural)
VECTOR_STORE_PATH = os.getenv('VECTOR_STORE_PATH')
RAG_FILES_DIR = os.getenv('RAG_FILES_DIR')
# Configuração da Evolution API - detecta automaticamente se está rodando dentro ou fora do Docker
EVOLUTION_API_URL_DOCKER = os.getenv('EVOLUTION_API_URL', 'http://evolution-api:8080')
EVOLUTION_API_URL_LOCAL = EVOLUTION_API_URL_DOCKER.replace('http://evolution-api:', 'http://localhost:')

# Se estiver rodando fora do Docker, usa localhost
EVOLUTION_API_URL = EVOLUTION_API_URL_LOCAL if not os.path.exists('/.dockerenv') else EVOLUTION_API_URL_DOCKER
EVOLUTION_INSTANCE_NAME = os.getenv('EVOLUTION_INSTANCE_NAME')
if not EVOLUTION_INSTANCE_NAME:
    raise ValueError("EVOLUTION_INSTANCE_NAME não encontrada. Configure no arquivo .env")

EVOLUTION_AUTHENTICATION_API_KEY = os.getenv('AUTHENTICATION_API_KEY')
if not EVOLUTION_AUTHENTICATION_API_KEY:
    raise ValueError("AUTHENTICATION_API_KEY não encontrada. Configure no arquivo .env")

# Configuração do Redis - detecta automaticamente se está rodando dentro ou fora do Docker
REDIS_URL_DOCKER = os.getenv('CACHE_REDIS_URI', 'redis://redis:6379/6')
REDIS_URL_LOCAL = REDIS_URL_DOCKER.replace('redis://redis:', 'redis://localhost:')

# Se estiver rodando fora do Docker, usa localhost
REDIS_URL = REDIS_URL_LOCAL if not os.path.exists('/.dockerenv') else REDIS_URL_DOCKER
BUFFER_KEY_SUFIX = os.getenv('BUFFER_KEY_SUFIX', ':buffer')
DEBOUNCE_SECONDS = os.getenv('DEBOUNCE_SECONDS', '10')
BUFFER_TTL = os.getenv('BUFFER_TTL', '300')

# Configuração do Google Calendar
# TEMPORARIAMENTE DESABILITADO devido ao erro de streaming da OpenAI
ENABLE_GOOGLE_CALENDAR = True  # ✅ Verificação feita - aguardando propagação (até 15min)
