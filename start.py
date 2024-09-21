import os
import subprocess

# Start the FastAPI application
subprocess.Popen(["uvicorn", "api:app", "--host", "0.0.0.0", "--port", os.environ.get("PORT", "8000")])

# Start the Telegram bot
subprocess.Popen(["python", "bot/bot.py"])  # Ajusta la ruta según tu estructura de archivos

# Mantener el proceso principal en ejecución
while True:
    pass
