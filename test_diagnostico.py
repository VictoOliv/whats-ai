#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de Diagnóstico do Bot WhatsApp
Testa todos os componentes do sistema
"""

import os
import sys
from dotenv import load_dotenv

print("="*70)
print("🔍 DIAGNÓSTICO COMPLETO DO BOT WHATSAPP")
print("="*70)

# Carregar .env
print("\n📁 Carregando arquivo .env...")
load_dotenv()

# ==============================================================================
# TESTE 1: Verificar Variáveis de Ambiente
# ==============================================================================
print("\n" + "="*70)
print("1️⃣ VERIFICANDO VARIÁVEIS DE AMBIENTE")
print("="*70)

required_vars = {
    'OPENAI_API_KEY': 'Chave da API OpenAI',
    'OPENAI_MODEL_NAME': 'Modelo da OpenAI',
    'EVOLUTION_API_URL': 'URL da Evolution API',
    'EVOLUTION_INSTANCE_NAME': 'Nome da instância',
    'AI_CONTEXTUALIZE_PROMPT_FILE': 'Arquivo de prompt de contextualização',
    'AI_SYSTEM_PROMPT_FILE': 'Arquivo de prompt do sistema',
    'VECTOR_STORE_PATH': 'Caminho do vectorstore',
}

optional_vars = {
    'CACHE_REDIS_URI': 'URI do Redis',
    'DEVELOPMENT_MODE': 'Modo de desenvolvimento',
    'DEBOUNCE_SECONDS': 'Segundos de debounce',
}

missing_vars = []
for var, description in required_vars.items():
    value = os.getenv(var)
    if value:
        # Mascara API keys
        if 'KEY' in var or 'API' in var:
            display_value = value[:15] + "..." if len(value) > 15 else value
        else:
            display_value = value
        print(f"   ✅ {var}: {display_value}")
    else:
        print(f"   ❌ {var}: FALTANDO - {description}")
        missing_vars.append(var)

print("\n   Variáveis Opcionais:")
for var, description in optional_vars.items():
    value = os.getenv(var, 'Não configurado')
    print(f"   ℹ️ {var}: {value}")

if missing_vars:
    print(f"\n   ⚠️ ATENÇÃO: {len(missing_vars)} variável(is) obrigatória(s) faltando!")
    print(f"   Configure no arquivo .env: {', '.join(missing_vars)}")
else:
    print("\n   ✅ Todas as variáveis obrigatórias configuradas!")

# ==============================================================================
# TESTE 2: Verificar Arquivos de Prompt
# ==============================================================================
print("\n" + "="*70)
print("2️⃣ VERIFICANDO ARQUIVOS DE PROMPT")
print("="*70)

contextualize_file = os.getenv('AI_CONTEXTUALIZE_PROMPT_FILE', 'bot/prompts/contextualize.txt')
system_file = os.getenv('AI_SYSTEM_PROMPT_FILE', 'bot/prompts/system.txt')

files_to_check = [
    (contextualize_file, 'Prompt de Contextualização'),
    (system_file, 'Prompt do Sistema'),
]

for file_path, description in files_to_check:
    if os.path.exists(file_path):
        file_size = os.path.getsize(file_path)
        print(f"   ✅ {description}: {file_path} ({file_size} bytes)")
    else:
        print(f"   ❌ {description}: {file_path} - ARQUIVO NÃO ENCONTRADO")

# ==============================================================================
# TESTE 3: Testar OpenAI API
# ==============================================================================
print("\n" + "="*70)
print("3️⃣ TESTANDO OPENAI API")
print("="*70)

try:
    from openai import OpenAI
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("   ❌ OPENAI_API_KEY não configurada!")
    else:
        print("   📡 Tentando conectar à OpenAI...")
        client = OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model=os.getenv('OPENAI_MODEL_NAME', 'gpt-4o-mini'),
            messages=[{"role": "user", "content": "Responda apenas: OK"}],
            max_tokens=5
        )
        
        result = response.choices[0].message.content
        print(f"   ✅ OpenAI API funcionando!")
        print(f"   📝 Resposta de teste: {result}")
        print(f"   💰 Tokens usados: {response.usage.total_tokens}")
        
except ImportError:
    print("   ❌ Biblioteca 'openai' não instalada!")
    print("   💡 Execute: pip install openai")
except Exception as e:
    print(f"   ❌ Erro ao testar OpenAI: {e}")
    print("\n   Possíveis causas:")
    print("   - API Key inválida ou expirada")
    print("   - Sem créditos na conta OpenAI")
    print("   - Problema de conexão com internet")

# ==============================================================================
# TESTE 4: Testar Evolution API
# ==============================================================================
print("\n" + "="*70)
print("4️⃣ TESTANDO EVOLUTION API")
print("="*70)

try:
    import requests
    
    evolution_url = os.getenv('EVOLUTION_API_URL')
    api_key = os.getenv('AUTHENTICATION_API_KEY', os.getenv('EVOLUTION_INSTANCE_NAME', 'PyWhats'))
    
    if not evolution_url:
        print("   ❌ EVOLUTION_API_URL não configurada!")
    else:
        print(f"   📡 Conectando a: {evolution_url}")
        
        # Teste de conexão básica
        try:
            response = requests.get(f"{evolution_url}/instance/fetchInstances", 
                                   headers={"apikey": api_key}, 
                                   timeout=5)
            
            if response.status_code == 200:
                print(f"   ✅ Evolution API respondendo!")
                
                instances = response.json()
                if instances:
                    print(f"   📱 Instâncias encontradas: {len(instances)}")
                    for instance in instances:
                        instance_name = instance.get('instance', {}).get('instanceName', 'N/A')
                        status = instance.get('instance', {}).get('status', 'N/A')
                        print(f"      - {instance_name}: {status}")
                else:
                    print(f"   ⚠️ Nenhuma instância encontrada")
            else:
                print(f"   ⚠️ Evolution API respondeu com status: {response.status_code}")
                print(f"   💡 Verifique se a API está configurada corretamente")
                
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Não foi possível conectar à Evolution API")
            print(f"   💡 Verifique se a Evolution API está rodando em: {evolution_url}")
            print(f"   💡 Execute: docker-compose up -d")
            
except ImportError:
    print("   ❌ Biblioteca 'requests' não instalada!")
    print("   💡 Execute: pip install requests")
except Exception as e:
    print(f"   ❌ Erro ao testar Evolution API: {e}")

# ==============================================================================
# TESTE 5: Verificar Vectorstore
# ==============================================================================
print("\n" + "="*70)
print("5️⃣ VERIFICANDO VECTORSTORE")
print("="*70)

try:
    vectorstore_path = os.getenv('VECTOR_STORE_PATH', 'vectorstore_data')
    
    if os.path.exists(vectorstore_path):
        print(f"   ✅ Diretório vectorstore existe: {vectorstore_path}")
        
        # Contar arquivos
        files = []
        for root, dirs, filenames in os.walk(vectorstore_path):
            files.extend(filenames)
        
        print(f"   📁 Total de arquivos: {len(files)}")
        
        # Tentar carregar vectorstore
        try:
            from vectorstore import get_vectorstore
            print("   📡 Carregando vectorstore...")
            vs = get_vectorstore()
            print("   ✅ Vectorstore carregado com sucesso!")
            
            # Teste de busca
            results = vs.similarity_search("teste", k=1)
            print(f"   🔍 Teste de busca: {len(results)} resultado(s)")
            
        except Exception as e:
            print(f"   ⚠️ Erro ao carregar vectorstore: {e}")
    else:
        print(f"   ❌ Diretório vectorstore não encontrado: {vectorstore_path}")
        print(f"   💡 Execute o script de processamento RAG")
        
except Exception as e:
    print(f"   ❌ Erro ao verificar vectorstore: {e}")

# ==============================================================================
# TESTE 6: Verificar RAG Files
# ==============================================================================
print("\n" + "="*70)
print("6️⃣ VERIFICANDO ARQUIVOS RAG")
print("="*70)

try:
    rag_dir = os.getenv('RAG_FILES_DIR', 'rag_files/processed')
    
    if os.path.exists(rag_dir):
        print(f"   ✅ Diretório RAG existe: {rag_dir}")
        
        # Contar PDFs
        pdf_count = 0
        for root, dirs, files in os.walk(rag_dir):
            for file in files:
                if file.endswith('.pdf'):
                    pdf_count += 1
        
        print(f"   📄 Total de PDFs: {pdf_count}")
        
        if pdf_count == 0:
            print(f"   ⚠️ Nenhum PDF encontrado em {rag_dir}")
            print(f"   💡 Adicione arquivos PDF para o RAG processar")
    else:
        print(f"   ❌ Diretório RAG não encontrado: {rag_dir}")
        
except Exception as e:
    print(f"   ❌ Erro ao verificar arquivos RAG: {e}")

# ==============================================================================
# TESTE 7: Verificar Redis (Opcional)
# ==============================================================================
print("\n" + "="*70)
print("7️⃣ VERIFICANDO REDIS (OPCIONAL)")
print("="*70)

dev_mode = os.getenv('DEVELOPMENT_MODE', 'false').lower() == 'true'

if dev_mode:
    print("   ℹ️ DEVELOPMENT_MODE=true - Usando buffer local")
    print("   ✅ Redis não é necessário")
else:
    redis_uri = os.getenv('CACHE_REDIS_URI')
    if redis_uri:
        print(f"   📡 Testando conexão Redis: {redis_uri}")
        try:
            import redis
            r = redis.from_url(redis_uri)
            r.ping()
            print("   ✅ Redis conectado!")
        except Exception as e:
            print(f"   ⚠️ Redis não disponível: {e}")
            print(f"   💡 O bot usará buffer local automaticamente")
    else:
        print("   ℹ️ Redis não configurado - usando buffer local")

# ==============================================================================
# TESTE 8: Verificar Servidor FastAPI
# ==============================================================================
print("\n" + "="*70)
print("8️⃣ VERIFICANDO SERVIDOR FASTAPI")
print("="*70)

try:
    import requests
    
    print("   📡 Tentando conectar ao servidor local...")
    
    try:
        response = requests.get("http://localhost:8000/docs", timeout=2)
        if response.status_code == 200:
            print("   ✅ Servidor FastAPI está rodando!")
            print("   🌐 Documentação disponível em: http://localhost:8000/docs")
        else:
            print(f"   ⚠️ Servidor respondeu com status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("   ⚠️ Servidor FastAPI não está rodando")
        print("\n   💡 Para iniciar o servidor:")
        print("      1. Ative o ambiente virtual: venv\\Scripts\\activate")
        print("      2. Execute: uvicorn main:app --host 0.0.0.0 --port 8000 --reload")
        
except Exception as e:
    print(f"   ❌ Erro ao verificar servidor: {e}")

# ==============================================================================
# RESUMO FINAL
# ==============================================================================
print("\n" + "="*70)
print("📊 RESUMO DO DIAGNÓSTICO")
print("="*70)

print("\n✅ PASSOS CONCLUÍDOS:")
print("   1. Variáveis de ambiente verificadas")
print("   2. Arquivos de prompt verificados")
print("   3. OpenAI API testada")
print("   4. Evolution API testada")
print("   5. Vectorstore verificado")
print("   6. Arquivos RAG verificados")
print("   7. Redis verificado")
print("   8. Servidor FastAPI verificado")

print("\n📋 PRÓXIMOS PASSOS:")
print("\n   Para o bot funcionar, você precisa:")
print("   1. ✅ Servidor FastAPI rodando (porta 8000)")
print("   2. ✅ Evolution API rodando (porta 8080)")
print("   3. ✅ Instância WhatsApp conectada")
print("   4. ✅ Webhook configurado na Evolution API")
print("   5. ✅ Arquivo .env com todas as variáveis")

print("\n🔧 COMANDOS ÚTEIS:")
print("\n   # Iniciar servidor:")
print("   uvicorn main:app --host 0.0.0.0 --port 8000 --reload")
print("\n   # Iniciar Evolution API (Docker):")
print("   docker-compose up -d")
print("\n   # Ver logs em tempo real:")
print("   # (observe o terminal onde o servidor está rodando)")

print("\n📖 DOCUMENTAÇÃO:")
print("   - Leia: arquivosMD/DIAGNOSTICO_BOT_NAO_RESPONDE.md")
print("   - Para testes manuais: test_manual.py")

print("\n" + "="*70)
print("DIAGNÓSTICO COMPLETO! ✨")
print("="*70 + "\n")

