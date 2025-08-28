#!/bin/sh

# Espera o banco de dados estar disponível (usando o comando pg_isready)
# Você precisará instalar o postgresql-client em seu Dockerfile para que este comando funcione
echo "Aguardando o banco de dados..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "Banco de dados iniciado!"

# Aplica as migrações do Django
python manage.py makemigrations
python manage.py migrate

# Inicia o servidor do Django
python manage.py runserver 0.0.0.0:8000