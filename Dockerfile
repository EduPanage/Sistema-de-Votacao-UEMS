# Usa a imagem oficial do Python 3.11
FROM python:3.11

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo de dependências e instala as bibliotecas
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código do projeto para o diretório de trabalho
COPY . .

# Expõe a porta que o Django vai usar
EXPOSE 8000

# Executa as migrações e, em seguida, inicia o servidor.
# O uso de "shell form" (sem colchetes) permite o encadeamento com "&&".
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000