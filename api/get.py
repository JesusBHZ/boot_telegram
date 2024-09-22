import requests
import time
import os

API_URL = os.getenv("TELEGRAM_BOT_API")  # Cambia esto a tu URL de API

def keep_alive():
    while True:
        try:
            # Hacer una petición GET a tu API
            response = requests.get(API_URL)
            if response.status_code == 200:
                print("API está activa, respuesta exitosa.")
            else:
                print(f"Error: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error al hacer la petición: {e}")

        # Esperar 5 minutos antes de la siguiente petición
        time.sleep(200)  # 300 segundos = 5 minutos

if __name__ == "__main__":
    keep_alive()