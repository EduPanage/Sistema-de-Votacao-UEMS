# Etapa 1: imagem base leve
FROM python:3.11-slim AS base

# Evita prompts interativos e melhora o desempenho de logs
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Instala dependências do sistema (como libpq para Postgres, se usado)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de dependências primeiro (melhora o cache do Docker)
COPY requirements.txt .

# Atualiza o pip e instala dependências
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia o restante do código do projeto
COPY . .

# Expõe a porta padrão do Django
EXPOSE 8000

# Cria um usuário não root (boa prática de segurança)
RUN adduser --disabled-password --gecos '' django
USER django

# Comando padrão: executa as migrações e inicia o servidor
CMD ["bash", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
