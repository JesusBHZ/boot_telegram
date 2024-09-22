#!/usr/bin/env python
import logging
import os
import psutil
from telegram import ForceReply, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Habilitar logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

def is_bot_running():
    """Verificar si el bot ya está en ejecución."""
    current_pid = os.getpid()
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if proc.info['name'] == 'python' and proc.info['pid'] != current_pid:
            if any('bot.py' in part for part in proc.info['cmdline']):
                return True
    return False

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
    
    if is_bot_running():
        logger.warning("El bot ya está en ejecución.")
        return

    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    logger.info("Iniciando el bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
