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

# Iniciar la API (si es diferente del bot)
python api/get.py &
# Guardar el PID del proceso de la API
API_PID=$!

# Función para manejar la terminación
cleanup() {
    echo "Shutting down..."
    # Asegurarse de que solo se intenten matar procesos en ejecución
    if kill -0 $UVICORN_PID >/dev/null 2>&1; then
        kill $UVICORN_PID
    fi
    if [[ -n "$BOT_PID" ]] && kill -0 $BOT_PID >/dev/null 2>&1; then
        kill $BOT_PID
    fi
    if [[ -n "$API_PID" ]] && kill -0 $API_PID >/dev/null 2>&1; then
        kill $API_PID
    fi
    exit
}

# Capturar señales de terminación
trap cleanup SIGINT SIGTERM

# Mantener el script en ejecución
wait $UVICORN_PID
wait $BOT_PID
wait $API_PID
