#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Teste Manual Simplificado
Para diagnóstico rápido
"""

import os
from dotenv import load_dotenv

load_dotenv()

print("="*60)
print("🔍 TESTE RÁPIDO DO BOT")
print("="*60)

# 1. Verificar .env
print("\n1. Verificando arquivo .env...")
env_vars = [
    'OPENAI_API_KEY',
    'EVOLUTION_API_URL',
    'EVOLUTION_INSTANCE_NAME',
    'AI_SYSTEM_PROMPT_FILE',
    'AI_CONTEXTUALIZE_PROMPT_FILE'
]
for var in env_vars:
    value = os.getenv(var)
    status = "✅" if value else "❌"
    display = value[:20] + "..." if value and len(value) > 20 else (value if value else "FALTANDO")
    print(f"   {status} {var}: {display}")

# 2. Testar OpenAI
print("\n2. Testando OpenAI API...")
try:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.chat.completions.create(
        model=os.getenv('OPENAI_MODEL_NAME', 'gpt-4o-mini'),
        messages=[{"role": "user", "content": "teste"}],
        max_tokens=5
    )
    print(f"   ✅ OpenAI funcionando! Resposta: {response.choices[0].message.content}")
except Exception as e:
    print(f"   ❌ Erro OpenAI: {str(e)[:100]}")

# 3. Testar Evolution API
print("\n3. Testando Evolution API...")
try:
    import requests
    url = f"{os.getenv('EVOLUTION_API_URL')}/instance/fetchInstances"
    headers = {"apikey": os.getenv('AUTHENTICATION_API_KEY', 'PyWhats')}
    response = requests.get(url, headers=headers, timeout=5)
    if response.status_code == 200:
        print(f"   ✅ Evolution API respondendo! Instâncias: {len(response.json())}")
    else:
        print(f"   ⚠️ Status code: {response.status_code}")
except Exception as e:
    print(f"   ❌ Erro Evolution API: {str(e)[:100]}")

# 4. Testar Vectorstore
print("\n4. Testando Vectorstore...")
try:
    from vectorstore import get_vectorstore
    vs = get_vectorstore()
    results = vs.similarity_search("teste", k=1)
    print(f"   ✅ Vectorstore carregado! Documentos encontrados: {len(results)}")
except Exception as e:
    print(f"   ❌ Erro Vectorstore: {str(e)[:100]}")

# 5. Verificar Servidor
print("\n5. Verificando Servidor FastAPI...")
try:
    import requests
    response = requests.get("http://localhost:8000/docs", timeout=2)
    print("   ✅ Servidor rodando em http://localhost:8000")
except:
    print("   ⚠️ Servidor NÃO está rodando!")
    print("   💡 Execute: uvicorn main:app --host 0.0.0.0 --port 8000 --reload")

print("\n" + "="*60)
print("TESTE COMPLETO!")
print("="*60)
print("\nℹ️ Para diagnóstico detalhado, execute: python test_diagnostico.py")
print("📖 Leia a documentação em: arquivosMD/DIAGNOSTICO_BOT_NAO_RESPONDE.md\n")

