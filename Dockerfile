# Usar a imagem oficial do Python
FROM python:3.11

# Definir a pasta onde o código vai rodar dentro do contêiner
WORKDIR /app

# Copiar o arquivo de dependências para dentro do contêiner
COPY requirements.txt requirements.txt

# Instalar as dependências
RUN pip install -r requirements.txt

# Copiar todo o código do projeto para dentro do contêiner
COPY . .

# Rodar o servidor Django dentro do contêiner
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

