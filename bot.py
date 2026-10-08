import os
import json
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

ARQUIVO_TAREFAS = "tarefas.json"


# =========================
# SERVIDOR WEB
# =========================

@app_web.route("/")
def home():
    return "ORION ONLINE", 200


def iniciar_web():
    porta = int(os.environ.get("PORT", 10000))

    app_web.run(
        host="0.0.0.0",
        port=porta,
        debug=False,
        use_reloader=False
    )


# =========================
# TAREFAS
# =========================

def carregar_tarefas():
    try:
        with open(ARQUIVO_TAREFAS, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def salvar_tarefas(tarefas):
    with open(ARQUIVO_TAREFAS, "w", encoding="utf-8") as arquivo:
        json.dump(tarefas, arquivo, ensure_ascii=False, indent=2)


# =========================
# COMANDOS
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Olá! Eu sou o Orion.\n\n"
        "Seu assistente pessoal está online.\n\n"
        "Digite /ajuda para ver os comandos."
    )


async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "COMANDOS DO ORION\n\n"
        "/start - Iniciar o Orion\n"
        "/ajuda - Ver os comandos\n"
        "/tarefas - Ver suas tarefas\n"
        "/addtarefa - Adicionar uma tarefa"
    )


async def tarefas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lista = carregar_tarefas()

    if not lista:
        await update.message.reply_text(
            "Você não tem tarefas cadastradas."
        )
        return

    texto = "SUAS TAREFAS\n\n"

    for i, tarefa in enumerate(lista, start=1):
        texto += f"{i}. {tarefa}\n"

    await update.message.reply_text(texto)


async def adicionar_tarefa(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    if not context.args:
        await update.message.reply_text(
            "Use assim:\n\n"
            "/addtarefa comprar arroz"
        )
        return

    nova_tarefa = " ".join(context.args)

    lista = carregar_tarefas()
    lista.append(nova_tarefa)
    salvar_tarefas(lista)

    await update.message.reply_text(
        f"Tarefa adicionada:\n\n"
        f"✓ {nova_tarefa}"
    )


async def mensagem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text

    await update.message.reply_text(
        f"Orion recebeu:\n\n{texto}"
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
    app.add_handler(CommandHandler("tarefas", tarefas))
    app.add_handler(CommandHandler("addtarefa", adicionar_tarefa))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            mensagem
        )
    )

    app.run_polling()


if __name__ == "__main__":
    main()
