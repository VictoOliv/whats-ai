FROM python:3.12

WORKDIR /whats_ai

# Copia apenas o requirements primeiro para otimizar cache
COPY requirements.txt .

RUN apt update && apt install -y --no-install-recommends \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copia todo o restante do projeto
COPY . .

# Garante que a pasta prompts/ exista
RUN mkdir -p prompts

EXPOSE 8000

# Comando para rodar o bot
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
