import os
import subprocess
import sys
import time
import threading

# Start the FastAPI application
try:
    uvicorn_process = subprocess.Popen(
        ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"],
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
        ["python", "bot/bot.py"],  # Ajusta la ruta según tu estructura
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    print("Telegram bot started.")
except Exception as e:
    print(f"Failed to start Telegram bot: {e}")
    sys.exit(1)

# Function to capture and print output
def log_output(process, name):
    while True:
        output = process.stdout.readline()
        if output == b"" and process.poll() is not None:
            break
        if output:
            print(f"{name}: {output.decode().strip()}")

# Start logging output for both processes
threading.Thread(target=log_output, args=(uvicorn_process, "UVICORN")).start()
threading.Thread(target=log_output, args=(bot_process, "BOT")).start()

# Keep the main process running
try:
    while True:
        time.sleep(1)  # Avoid excessive CPU consumption
except KeyboardInterrupt:
    print("Shutting down...")
    uvicorn_process.terminate()
    bot_process.terminate()
