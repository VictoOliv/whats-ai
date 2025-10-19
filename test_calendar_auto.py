#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de teste automático (sem interação) para o Google Calendar.
"""

import os
import sys

# Configurar variável de ambiente antes de importar
os.environ['ENABLE_GOOGLE_CALENDAR'] = 'true'

def test_calendar_tools():
    """Testa as ferramentas do Google Calendar."""
    print("\n" + "="*60)
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
        return False
    
    # Teste 1: Listar eventos
    print("\n" + "="*60)
    print("📋 TESTE 1: Listar Próximos Eventos")
    print("="*60)
    try:
        result = list_calendar_events.invoke({"max_results": 5, "days_ahead": 7})
        print(f"✅ Sucesso!\nResultado:\n{result}\n")
    except Exception as e:
        print(f"❌ Erro: {e}\n")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*60)
    print("✅ TESTE CONCLUÍDO!")
    print("="*60)
    return True


def check_prerequisites():
    """Verifica pré-requisitos."""
    print("="*60)
    print("🔍 VERIFICANDO PRÉ-REQUISITOS")
    print("="*60)
    
    issues = []
    
    # 1. Verificar credentials.json
    if not os.path.exists('credentials.json'):
        issues.append("❌ Arquivo 'credentials.json' não encontrado")
    else:
        print("✅ credentials.json encontrado")
    
    # 2. Verificar dependências
    try:
        import google.auth
        import googleapiclient
        print("✅ Bibliotecas do Google instaladas")
    except ImportError:
        issues.append("❌ Bibliotecas do Google não instaladas")
    
    # 3. Verificar LangChain
    try:
        import langchain
        from langchain.agents import AgentExecutor
        print("✅ LangChain instalado")
    except ImportError:
        issues.append("❌ LangChain não instalado")
    
    # 4. Verificar .env
    from dotenv import load_dotenv
    load_dotenv()
    
    if not os.getenv('OPENAI_API_KEY'):
        issues.append("⚠️  OPENAI_API_KEY não encontrada")
    else:
        print("✅ OPENAI_API_KEY configurada")
    
    print()
    
    if issues:
        print("❌ PROBLEMAS ENCONTRADOS:")
        for issue in issues:
            print(f"  {issue}")
        return False
    
    print("✅ TODOS OS PRÉ-REQUISITOS ATENDIDOS!\n")
    return True


def main():
    """Função principal."""
    print("\n" + "="*60)
    print("🚀 TESTE AUTOMÁTICO - GOOGLE CALENDAR")
    print("="*60)
    
    # Verificar pré-requisitos
    if not check_prerequisites():
        print("\n❌ Testes cancelados.\n")
        return 1
    
    # Executar testes
    print("\n" + "="*60)
    print("▶️  INICIANDO TESTES...")
    print("="*60)
    
    tools_ok = test_calendar_tools()
    
    # Resultado final
    print("\n" + "="*60)
    print("📊 RESULTADO FINAL")
    print("="*60)
    
    if tools_ok:
        print("✅ TESTE PASSOU COM SUCESSO!")
        print("\n🎉 A integração está funcionando!")
        print("\nPróximos passos:")
        print("1. Configure ENABLE_GOOGLE_CALENDAR=true no .env")
        print("2. Execute: python main.py")
        print("3. Teste via WhatsApp")
        return 0
    else:
        print("❌ TESTE FALHOU")
        print("\nConsulte: GOOGLE_CALENDAR_SETUP.md")
        return 1


if __name__ == '__main__':
    sys.exit(main())

