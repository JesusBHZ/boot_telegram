import requests
import time
import os

API_URL = os.getenv("TELEGRAM_BOT_API")  # Cambia esto a tu URL de API

def keep_alive():
    while True:
        try:
            response = requests.get(API_URL)
            if response.status_code == 200:
                print("API está despierta.")
            else:
                print(f"Error al acceder a la API: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
        
        time.sleep(600)  # Espera 10 minutos (600 segundos) antes de la siguiente solicitud

if __name__ == "__main__":
    keep_alive()
