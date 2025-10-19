from config import REDIS_URL
from langchain_community.chat_message_histories import RedisChatMessageHistory
import redis.asyncio as redis

def get_session_history(session_id, max_messages=10):
    """
    Retorna o histórico da sessão com limite de mensagens.
    Mantém apenas as últimas 'max_messages' mensagens para evitar confusão de contexto.
    """
    history = RedisChatMessageHistory(
        session_id=session_id,
        url=REDIS_URL,
        ttl=7200,  # TTL de 2 horas (7200 segundos) - após isso, histórico expira
    )
    
    # Limita o histórico às últimas N mensagens
    messages = history.messages
    if len(messages) > max_messages:
        # Mantém apenas as últimas max_messages mensagens
        messages_to_keep = messages[-max_messages:]
        # Limpa o histórico e readiciona apenas as mensagens recentes
        history.clear()
        for msg in messages_to_keep:
            history.add_message(msg)
    
    return history

async def clear_session_history(session_id):
    """Limpa completamente o histórico de uma sessão específica"""
    redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)
    pattern = f"evolution:{session_id}*"
    keys = await redis_client.keys(pattern)
    if keys:
        await redis_client.delete(*keys)