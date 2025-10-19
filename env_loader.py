import os
from dotenv import load_dotenv

def load_env_with_file_contents(env_path=".env"):
    """
    Carrega variáveis do .env.
    Substitui variáveis que terminam com _FILE pelo conteúdo do arquivo.
    Retorna um dicionário com todas as variáveis.
    """
    # Carrega o .env
    load_dotenv(env_path)

    env_vars = {}
    for key, value in os.environ.items():
        if key.endswith("_FILE"):
            file_path = value
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    value = f.read().strip()
            else:
                raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

        env_vars[key] = value

    return env_vars
