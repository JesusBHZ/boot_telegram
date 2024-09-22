#!/usr/bin/env python
import logging
import os
import sys
from telegram import ForceReply, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

LOCK_FILE = "/tmp/bot.lock"

# Habilitar logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

def create_lock_file():
    """Crea un archivo de bloqueo para evitar múltiples instancias."""
    try:
        if os.path.exists(LOCK_FILE):
            logger.warning("El bot ya está en ejecución (bloqueo detectado).")
            sys.exit(0)
        with open(LOCK_FILE, 'w') as f:
            f.write(str(os.getpid()))
    except Exception as e:
        logger.error(f"Error al crear el archivo de bloqueo: {e}")
        sys.exit(1)

def remove_lock_file():
    """Elimina el archivo de bloqueo al finalizar."""
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Enviar un mensaje cuando se emita el comando /start."""
    user = update.effective_user
    await update.message.reply_html(
        rf"¡Hola {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Enviar un mensaje cuando se emita el comando /help."""
    await update.message.reply_text("¡Ayuda!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Repetir el mensaje del usuario."""
    await update.message.reply_text(update.message.text)

def main() -> None:
    """Iniciar el bot."""
    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not BOT_TOKEN:
        logger.error("No se ha encontrado el token del bot en las variables de entorno.")
        return

    # Verifica si el bot ya está en ejecución
    if is_bot_running():
        logger.warning("El bot ya está en ejecución.")
        return

    # Crear el archivo de bloqueo
    lock_file = create_lock_file()

    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    logger.info("Iniciando el bot...")

    try:
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    finally:
        remove_lock_file(lock_file)

if __name__ == "__main__":
    main()
