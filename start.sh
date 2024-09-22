#!/bin/bash

# Iniciar la aplicación FastAPI
uvicorn api.main:app --host 0.0.0.0 --port 8000 &

# Guardar el PID del proceso de FastAPI
UVICORN_PID=$!

# Iniciar el bot de Telegram solo si no hay otra instancia
if ! pgrep -f "bot/bot.py" > /dev/null; then
    python bot/bot.py &
    # Guardar el PID del proceso del bot
    BOT_PID=$!
else
    echo "El bot de Telegram ya está en ejecución."
fi

# Iniciarla API
python api/get.py &
# Guardar el PID del proceso de la api
API_PID=$!

# Función para manejar la terminación
cleanup() {
    echo "Shutting down..."
    kill $UVICORN_PID
    kill $BOT_PID
    kill $API_PID
    exit
}

# Capturar señales de terminación
trap cleanup SIGINT SIGTERM

# Mantener el script en ejecución
wait $UVICORN_PID
wait $BOT_PID
wait $API_PID
