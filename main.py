
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
app = Flask(__name__)

sdk = mercadopago.SDK(MP_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Olá! Envie /pagar para receber o link de pagamento Pix.")

@bot.message_handler(commands=['pagar'])
def pagar(message):
    preference_data = {
        "items": [
            {
                "title": "Produto Exemplo",
                "quantity": 1,
                "currency_id": "BRL",
                "unit_price": 1.00
            }
        ]
    }
    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]
    link_pagamento = preference["init_point"]
    bot.reply_to(message, f"Clique para pagar via Pix: {link_pagamento}")

@app.route("/" + API_TOKEN, methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/")
def index():
    return "Bot está rodando."

if __name__ == "__main__":
    bot.remove_webhook()
    bot.polling()
