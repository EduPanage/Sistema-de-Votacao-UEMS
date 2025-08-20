FROM python:3.11

WORKDIR /app

# Copia e instala dependências
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código do projeto e o script de espera
COPY . .

# Porta padrão do Django
EXPOSE 8000

# Comando de inicialização
CMD ["python", "wait_for_db.py", "&&", "python", "manage.py", "runserver", "0.0.0.0:8000"]
