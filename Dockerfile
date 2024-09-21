FROM python:latest
RUN pip install --upgrade pip
RUN pip install fastapi  \
    python-telegram-bot
COPY ./bot /home/bot
WORKDIR /home/bot

# Ejecutar la aplicacion
CMD [ "python3", "bot.py"]