import requests
from config import (
    EVOLUTION_API_URL,
    EVOLUTION_INSTANCE_NAME,
    EVOLUTION_AUTHENTICATION_API_KEY,
)

def send_whatsapp_message(number, text):
    clean_number = number.replace("@s.whatsapp.net", "").replace("@g.us", "")

    url = f"{EVOLUTION_API_URL}/message/sendText/{EVOLUTION_INSTANCE_NAME}"
    headers = {
        "apikey": EVOLUTION_AUTHENTICATION_API_KEY,
        "Content-Type": "application/json"
    }

    # Tentar formatos diferentes de número
    for payload in [
        {"number": f"{clean_number}@s.whatsapp.net", "text": text},
        {"number": clean_number, "text": text}
    ]:
        try:
            response = requests.post(url=url, json=payload, headers=headers, timeout=10)
            
            if response.status_code in [200, 201]:
                response_data = response.json()
                # Verificar se o número existe
                if "exists" in response.text and "false" in response.text:
                    continue
                    
                return True
                
        except Exception as e:
            continue
            
    return False
