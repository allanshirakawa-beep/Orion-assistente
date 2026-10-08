import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = os.getenv("TELEGRAM_TOKEN")

app_web = Flask(__name__)


@app_web.route("/")
def home():
    return "ORION ONLINE", 200


# =========================
# COMANDOS DO ORION
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Olá! Eu sou o Orion.\n\n"
        "Seu assistente pessoal está online.\n\n"
        "Digite /ajuda para ver o que posso fazer."
    )


async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "COMANDOS DO ORION\n\n"
        "/start - Iniciar o Orion\n"
        "/ajuda - Ver os comandos disponíveis\n\n"
        "Novos recursos serão adicionados em breve."
    )


async def mensagem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text

    await update.message.reply_text(
        f"Orion recebeu:\n\n{texto}"
    )


# =========================
# SERVIDOR WEB
# =========================

def iniciar_web():
    porta = int(os.environ.get("PORT", 10000))

    app_web.run(
        host="0.0.0.0",
        port=porta,
        debug=False,
        use_reloader=False
    )


# =========================
# INICIALIZAÇÃO
# =========================

def main():
    servidor = threading.Thread(target=iniciar_web)
    servidor.daemon = True
    servidor.start()

    print("ORION ONLINE")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ajuda", ajuda))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            mensagem
        )
    )

    app.run_polling()


if __name__ == "__main__":
    main()
