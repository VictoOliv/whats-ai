from fastapi import FastAPI, Request
from message_buffer import buffer_message
from env_loader import load_env_with_file_contents
from chains import get_conversational_rag_chain

app = FastAPI()

# Carrega variáveis do .env e conteúdos de arquivos
env = load_env_with_file_contents()

contextualize_prompt_text = env.get("AI_CONTEXTUALIZE_PROMPT_FILE")
system_prompt_text = env.get("AI_SYSTEM_PROMPT_FILE")

# Cria o chain conversacional
conversational_rag_chain = get_conversational_rag_chain(
    contextualize_prompt_text, 
    system_prompt_text
)


@app.post('/webhook')
async def webhook(request: Request):
    try:
        data = await request.json()
        
        # Extração segura dos dados
        event_type = data.get('event')
        data_obj = data.get('data', {})
        
        # Verificar se a mensagem é do próprio bot (fromMe)
        key_data = data_obj.get('key', {})
        from_me = key_data.get('fromMe', False)
        
        chat_id = key_data.get('remoteJid')
        
        # Tentar extrair mensagem de diferentes locais
        message_data = data_obj.get('message', {})
        message = (
            message_data.get('conversation') or 
            message_data.get('extendedTextMessage', {}).get('text') or
            message_data.get('imageMessage', {}).get('caption') or
            None
        )

        # Ignorar mensagens do próprio bot
        if from_me:
            return {'status': 'ok'}

        if chat_id and message and not '@g.us' in chat_id:            
            await buffer_message(
                chat_id=chat_id,
                message=message,
                conversational_rag_chain=conversational_rag_chain,
            )
        
        return {'status': 'ok'}
    except Exception as e:
        print(f"Erro ao processar webhook: {e}")
        import traceback
        traceback.print_exc()
        return {'status': 'error', 'message': str(e)}
