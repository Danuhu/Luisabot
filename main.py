import os
import telebot
from flask import Flask, request
import mercadopago

API_TOKEN = os.getenv("API_TOKEN")
MP_TOKEN = os.getenv("MP_TOKEN")

if not API_TOKEN:
    raise ValueError("API_TOKEN não definido. Verifique as variáveis de ambiente no Render.")
if not MP_TOKEN:
    raise ValueError("MP_TOKEN não definido. Verifique as variáveis de ambiente no Render.")

bot = telebot.TeleBot(API_TOKEN)
sdk = mercadopago.SDK(MP_TOKEN)

app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(mensagem):
    bot.reply_to(mensagem, "Bem-vindo! Envie /pagar para gerar o link de pagamento via Pix.")

@bot.message_handler(commands=['pagar'])
def pagar(mensagem):
    preference_data = {
        "items": [
            {
                "title": "Produto Exemplo",
                "quantity": 1,
                "currency_id": "BRL",
                "unit_price": 1.0
            }
        ]
    }
    preference = sdk.preference().create(preference_data)
    link_pagamento = preference["response"]["init_point"]
    bot.reply_to(mensagem, f"Clique para pagar via Pix: {link_pagamento}")

@app.route('/', methods=['GET'])
def home():
    return "Bot de pagamento via Telegram e Mercado Pago está ativo."

if __name__ == '__main__':
    import threading
    polling_thread = threading.Thread(target=bot.polling, kwargs={"none_stop": True})
    polling_thread.start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
