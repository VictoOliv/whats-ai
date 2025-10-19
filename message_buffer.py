import asyncio
import redis.asyncio as redis
import os

from collections import defaultdict

from config import REDIS_URL, BUFFER_KEY_SUFIX, DEBOUNCE_SECONDS, BUFFER_TTL
from evolution_api import send_whatsapp_message

# Modo de desenvolvimento - se não conseguir conectar ao Redis, usa modo local
DEVELOPMENT_MODE = os.getenv('DEVELOPMENT_MODE', 'false').lower() == 'true'
USE_REDIS = True

# Tenta conectar ao Redis, se falhar, usa modo local
try:
    if REDIS_URL and not DEVELOPMENT_MODE:
        redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)
        USE_REDIS = True
    else:
        USE_REDIS = False
        redis_client = None
except Exception as e:
    USE_REDIS = False
    redis_client = None

# Buffer local para desenvolvimento
local_buffer = defaultdict(list)
debounce_tasks = defaultdict(asyncio.Task)

async def buffer_message(chat_id: str, message: str, conversational_rag_chain):
    global USE_REDIS
    buffer_key = f'{chat_id}{BUFFER_KEY_SUFIX}'
    
    print(f"\n{'='*60}")
    print(f"[BUFFER] Nova mensagem recebida: '{message}'")
    print(f"[BUFFER] Chat ID: {chat_id}")
    print(f"[BUFFER] Modo Redis: {USE_REDIS}")

    if USE_REDIS and redis_client:
        try:
            # Primeiro verifica quantas mensagens já existem
            current_count = await redis_client.llen(buffer_key)
            print(f"[BUFFER] Mensagens existentes no Redis antes de adicionar: {current_count}")
            
            await redis_client.rpush(buffer_key, message)
            await redis_client.expire(buffer_key, BUFFER_TTL)
            
            new_count = await redis_client.llen(buffer_key)
            print(f"[BUFFER] ✅ Mensagem adicionada ao Redis. Total agora: {new_count}")
        except Exception as e:
            print(f"[BUFFER] ❌ Erro ao adicionar ao Redis: {e}. Mudando para buffer local.")
            USE_REDIS = False
            # Adiciona ao buffer local
            local_buffer[chat_id].append(message)
            print(f"[BUFFER] Total no buffer local: {len(local_buffer[chat_id])}")
    else:
        # Modo local
        print(f"[BUFFER] Mensagens no buffer local antes: {len(local_buffer[chat_id])}")
        local_buffer[chat_id].append(message)
        print(f"[BUFFER] ✅ Mensagem adicionada ao buffer local. Total agora: {len(local_buffer[chat_id])}")
        print(f"[BUFFER] Conteúdo do buffer local: {local_buffer[chat_id]}")

    if debounce_tasks.get(chat_id):
        print(f"[BUFFER] ⏱️ Cancelando task anterior e reiniciando debounce de {DEBOUNCE_SECONDS}s")
        debounce_tasks[chat_id].cancel()
    else:
        print(f"[BUFFER] 🆕 Primeira mensagem - criando nova task de debounce de {DEBOUNCE_SECONDS}s")

    debounce_tasks[chat_id] = asyncio.create_task(handle_debounce(chat_id, conversational_rag_chain))
    print(f"{'='*60}\n")


async def handle_debounce(chat_id: str, conversational_rag_chain):
    try:
        print(f"\n[DEBOUNCE] 💤 Aguardando {DEBOUNCE_SECONDS}s antes de processar...")
        await asyncio.sleep(float(DEBOUNCE_SECONDS))
        
        print(f"\n{'='*60}")
        print(f"[DEBOUNCE] ⏰ Tempo de espera terminou! Processando mensagens...")

        # Busca mensagens do buffer (Redis ou local)
        if USE_REDIS and redis_client:
            try:
                buffer_key = f'{chat_id}{BUFFER_KEY_SUFIX}'
                count_before = await redis_client.llen(buffer_key)
                print(f"[DEBOUNCE] Mensagens no Redis antes de recuperar: {count_before}")
                
                messages = await redis_client.lrange(buffer_key, 0, -1)
                await redis_client.delete(buffer_key)
                
                print(f"[DEBOUNCE] ✅ Recuperadas {len(messages)} mensagens do Redis")
                print(f"[DEBOUNCE] Mensagens recuperadas: {messages}")
            except Exception as e:
                print(f"[DEBOUNCE] ❌ Erro ao buscar do Redis: {e}. Usando buffer local.")
                messages = local_buffer[chat_id].copy()
                local_buffer[chat_id].clear()
        else:
            # Modo local
            print(f"[DEBOUNCE] Buffer local antes de recuperar: {local_buffer[chat_id]}")
            messages = local_buffer[chat_id].copy()
            local_buffer[chat_id].clear()
            print(f"[DEBOUNCE] ✅ Recuperadas {len(messages)} mensagens do buffer local")
            print(f"[DEBOUNCE] Mensagens recuperadas: {messages}")

        # Se houver múltiplas mensagens, agrupa com informação contextual
        if len(messages) > 1:
            full_message = '\n'.join(messages).strip()
            print(f"\n[DEBOUNCE] 🎉 ✅ AGRUPANDO {len(messages)} MENSAGENS com quebra de linha")
            print(f"[DEBOUNCE] Mensagens individuais:")
            for i, msg in enumerate(messages, 1):
                print(f"  {i}. '{msg}'")
            print(f"\n[DEBOUNCE] Mensagem final enviada para IA:")
            print(f"---\n{full_message}\n---")
        else:
            full_message = messages[0].strip() if messages else ''
            print(f"\n[DEBOUNCE] ⚠️ APENAS 1 MENSAGEM NO BUFFER: '{full_message}'")
        
        if full_message:
            try:
                result = conversational_rag_chain.invoke(
                    input={'input': full_message},
                    config={'configurable': {'session_id': chat_id}},
                )
                # Tenta buscar 'answer' (RAG) ou 'output' (Agent)
                ai_response = result.get('answer') or result.get('output', '')
            except Exception as e:
                print(f'Erro ao invocar o chain: {e}')
                import traceback
                traceback.print_exc()
                ai_response = "Desculpe, houve um erro ao processar sua mensagem."

            try:
                send_whatsapp_message(
                    number=chat_id,
                    text=ai_response,
                )
            except Exception as e:
                print(f'Erro ao enviar mensagem: {e}')

    except asyncio.CancelledError:
        print(f"[DEBOUNCE] Task cancelada - nova mensagem recebida")
        pass
    except Exception as e:
        print(f'[DEBOUNCE] Erro inesperado no debounce: {e}')