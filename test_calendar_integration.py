#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de teste para a integração do Google Calendar.
Execute este script para testar as ferramentas do Calendar sem usar o WhatsApp.
"""

import os
import sys
from datetime import datetime, timedelta

# Configurar variável de ambiente antes de importar
os.environ['ENABLE_GOOGLE_CALENDAR'] = 'true'

def test_calendar_tools():
    """Testa as ferramentas do Google Calendar individualmente."""
    print("="*60)
    print("🧪 TESTE DAS FERRAMENTAS DO GOOGLE CALENDAR")
    print("="*60)
    
    try:
        from calendar_tools import (
            list_calendar_events,
            create_calendar_event,
            search_calendar_events,
        )
        print("✅ Módulo calendar_tools importado com sucesso!\n")
    except Exception as e:
        print(f"❌ Erro ao importar calendar_tools: {e}")
        print("\nCertifique-se de que:")
        print("1. As dependências estão instaladas (pip install -r requirements.txt)")
        print("2. O arquivo credentials.json está na raiz do projeto")
        return False
    
    # Teste 1: Listar eventos
    print("\n" + "="*60)
    print("📋 TESTE 1: Listar Próximos Eventos")
    print("="*60)
    try:
        result = list_calendar_events.invoke({"max_results": 5, "days_ahead": 7})
        print(f"Resultado:\n{result}\n")
    except Exception as e:
        print(f"❌ Erro: {e}\n")
    
    # Teste 2: Criar evento de teste
    print("\n" + "="*60)
    print("➕ TESTE 2: Criar Evento de Teste")
    print("="*60)
    try:
        # Calcula data/hora para amanhã às 14h
        tomorrow = datetime.now() + timedelta(days=1)
        start_time = tomorrow.replace(hour=14, minute=0, second=0, microsecond=0)
        end_time = start_time + timedelta(hours=1)
        
        # Formato ISO com timezone
        start_iso = start_time.strftime("%Y-%m-%dT%H:%M:%S-03:00")
        end_iso = end_time.strftime("%Y-%m-%dT%H:%M:%S-03:00")
        
        print(f"Criando evento para: {start_time.strftime('%d/%m/%Y às %H:%M')}")
        
        result = create_calendar_event.invoke({
            "summary": "🧪 Teste de Integração - Bot WhatsApp",
            "start_datetime": start_iso,
            "end_datetime": end_iso,
            "description": "Este é um evento de teste criado automaticamente pelo bot.",
            "location": "Teste Virtual"
        })
        print(f"Resultado:\n{result}\n")
    except Exception as e:
        print(f"❌ Erro: {e}\n")
    
    # Teste 3: Buscar eventos
    print("\n" + "="*60)
    print("🔍 TESTE 3: Buscar Eventos")
    print("="*60)
    try:
        result = search_calendar_events.invoke({
            "query": "Teste",
            "max_results": 5
        })
        print(f"Resultado:\n{result}\n")
    except Exception as e:
        print(f"❌ Erro: {e}\n")
    
    return True


def test_chain_integration():
    """Testa a integração completa com o chain."""
    print("\n" + "="*60)
    print("🔗 TESTE DA INTEGRAÇÃO COMPLETA COM CHAIN")
    print("="*60)
    
    try:
        from chains import get_conversational_rag_chain
        from env_loader import load_env_with_file_contents
        
        print("✅ Módulos importados com sucesso!\n")
        
        # Carrega configuração
        env = load_env_with_file_contents()
        contextualize_prompt_text = env.get("AI_CONTEXTUALIZE_PROMPT_FILE")
        system_prompt_text = env.get("AI_SYSTEM_PROMPT_FILE")
        
        # Cria o chain
        print("Criando chain conversacional com ferramentas do Calendar...")
        chain = get_conversational_rag_chain(
            contextualize_prompt_text,
            system_prompt_text
        )
        print("✅ Chain criado com sucesso!\n")
        
        # Testa com uma pergunta sobre calendário
        print("="*60)
        print("💬 TESTE: Pergunta sobre Calendário")
        print("="*60)
        test_query = "Quais são os meus próximos compromissos?"
        print(f"Pergunta: {test_query}\n")
        
        result = chain.invoke(
            input={'input': test_query},
            config={'configurable': {'session_id': 'test_session_001'}}
        )
        
        # Tenta buscar resposta
        answer = result.get('answer') or result.get('output', 'Sem resposta')
        print(f"Resposta:\n{answer}\n")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False


def check_prerequisites():
    """Verifica se todos os pré-requisitos estão atendidos."""
    print("="*60)
    print("🔍 VERIFICANDO PRÉ-REQUISITOS")
    print("="*60)
    
    issues = []
    
    # 1. Verificar credentials.json
    if not os.path.exists('credentials.json'):
        issues.append("❌ Arquivo 'credentials.json' não encontrado na raiz do projeto")
    else:
        print("✅ credentials.json encontrado")
    
    # 2. Verificar dependências
    try:
        import google.auth
        import googleapiclient
        print("✅ Bibliotecas do Google instaladas")
    except ImportError:
        issues.append("❌ Bibliotecas do Google não instaladas. Execute: pip install -r requirements.txt")
    
    # 3. Verificar LangChain
    try:
        import langchain
        from langchain.agents import AgentExecutor
        print("✅ LangChain instalado")
    except ImportError:
        issues.append("❌ LangChain não instalado corretamente")
    
    # 4. Verificar .env
    from dotenv import load_dotenv
    load_dotenv()
    
    if not os.getenv('OPENAI_API_KEY'):
        issues.append("⚠️  OPENAI_API_KEY não encontrada no .env")
    else:
        print("✅ OPENAI_API_KEY configurada")
    
    print()
    
    if issues:
        print("❌ PROBLEMAS ENCONTRADOS:")
        for issue in issues:
            print(f"  {issue}")
        print("\nCorreja esses problemas antes de continuar.")
        return False
    
    print("✅ TODOS OS PRÉ-REQUISITOS ATENDIDOS!\n")
    return True


def main():
    """Função principal."""
    print("\n" + "="*60)
    print("🚀 TESTE DE INTEGRAÇÃO GOOGLE CALENDAR")
    print("="*60)
    print("\nEste script irá testar:")
    print("1. Pré-requisitos do sistema")
    print("2. Ferramentas individuais do Calendar")
    print("3. Integração completa com o chain\n")
    
    # Verificar pré-requisitos
    if not check_prerequisites():
        print("\n❌ Testes cancelados devido a problemas nos pré-requisitos.\n")
        return 1
    
    # Aguardar confirmação
    print("="*60)
    input("Pressione ENTER para iniciar os testes...")
    
    # Executar testes das tools
    tools_ok = test_calendar_tools()
    
    if not tools_ok:
        print("\n❌ Testes das ferramentas falharam. Não é possível continuar.\n")
        return 1
    
    # Aguardar antes do próximo teste
    print("\n" + "="*60)
    input("Pressione ENTER para testar a integração completa com o chain...")
    
    # Executar teste do chain
    chain_ok = test_chain_integration()
    
    # Resultado final
    print("\n" + "="*60)
    print("📊 RESULTADO FINAL")
    print("="*60)
    
    if tools_ok and chain_ok:
        print("✅ TODOS OS TESTES PASSARAM COM SUCESSO!")
        print("\n🎉 A integração do Google Calendar está funcionando corretamente!")
        print("\nPróximos passos:")
        print("1. Configure ENABLE_GOOGLE_CALENDAR=true no .env")
        print("2. Execute o bot: python main.py")
        print("3. Teste via WhatsApp")
        return 0
    else:
        print("❌ ALGUNS TESTES FALHARAM")
        print("\nConsulte os erros acima e:")
        print("1. Verifique a documentação em GOOGLE_CALENDAR_SETUP.md")
        print("2. Confirme que a autenticação foi feita (token.pickle existe)")
        print("3. Verifique os logs de erro")
        return 1


if __name__ == '__main__':
    sys.exit(main())

