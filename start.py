import os
import subprocess
import sys
import time

# Start the FastAPI application
try:
    uvicorn_process = subprocess.Popen(
        ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", os.environ.get("PORT", "8000")],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    print("FastAPI application started.")
except Exception as e:
    print(f"Failed to start FastAPI application: {e}")
    sys.exit(1)

# Start the Telegram bot
try:
    bot_process = subprocess.Popen(
        ["python", "/bot/bot.py"],  # Asegúrate de que la ruta sea correcta
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    print("Telegram bot started.")
except Exception as e:
    print(f"Failed to start Telegram bot: {e}")
    sys.exit(1)

# Mantener el proceso principal en ejecución
try:
    while True:
        time.sleep(1)  # Evitar consumo excesivo de CPU
except KeyboardInterrupt:
    print("Shutting down...")
    uvicorn_process.terminate()
    bot_process.terminate()
