#!/bin/bash

# Iniciar la aplicación FastAPI
uvicorn api.main:app --host 0.0.0.0 --port 8000 &
# Guardar el PID del proceso de FastAPI
UVICORN_PID=$!

# Iniciar el bot de Telegram solo si no hay otra instancia
if ! pgrep -f "python.*bot/bot.py" > /dev/null; then
    echo "Iniciando el bot de Telegram..."
    python bot/bot.py &
    BOT_PID=$!
else
    echo "El bot de Telegram ya está en ejecución."
    BOT_PID=""
fi


# Iniciar la API (si es diferente del bot)
python api/get.py &
# Guardar el PID del proceso de la API
API_PID=$!

# Función para manejar la terminación
cleanup() {
    echo "Shutting down..."

    # Asegurarse de que solo se intenten matar procesos en ejecución
    if [[ -n "$UVICORN_PID" ]] && kill -0 $UVICORN_PID >/dev/null 2>&1; then
        kill $UVICORN_PID
        echo "Uvicorn detenido."
    fi
    if [[ -n "$BOT_PID" ]] && kill -0 $BOT_PID >/dev/null 2>&1; then
        kill $BOT_PID
        echo "Bot de Telegram detenido."
    fi
    if [[ -n "$API_PID" ]] && kill -0 $API_PID >/dev/null 2>&1; then
        kill $API_PID
        echo "API adicional detenida."
    fi
    exit
}

# Capturar señales de terminación
trap cleanup SIGINT SIGTERM

# Mantener el script en ejecución y manejar adecuadamente los procesos
if [[ -n "$UVICORN_PID" ]]; then wait $UVICORN_PID; fi
if [[ -n "$BOT_PID" ]]; then wait $BOT_PID; fi
if [[ -n "$API_PID" ]]; then wait $API_PID; fi
