import socket
import time
import os

DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = int(os.getenv("DB_PORT", 5432))
RETRIES = 10
DELAY = 3  # segundos

for attempt in range(RETRIES):
    try:
        with socket.create_connection((DB_HOST, DB_PORT), timeout=5):
            print(f"Banco de dados disponível em {DB_HOST}:{DB_PORT}")
            break
    except OSError:
        print(f"Tentativa {attempt + 1}/{RETRIES}: banco de dados ainda não disponível, esperando {DELAY}s...")
        time.sleep(DELAY)
else:
    print("Não foi possível conectar ao banco de dados após várias tentativas.")
    exit(1)
