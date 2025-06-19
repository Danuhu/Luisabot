import os
import telebot
import requests
from flask import Flask, request

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
MP_ACCESS_TOKEN = os.getenv("MP_ACCESS_TOKEN")
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# Comando /start
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Olá! Envie /pagar para receber o link de pagamento Pix.")

# Comando /pagar
@bot.message_handler(commands=["pagar"])
def handle_pagar(message):
    url = "https://api.mercadopago.com/checkout/preferences"
    headers = {
        "Authorization": f"Bearer {MP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "items": [{
            "title": "Produto Exemplo",
            "quantity": 1,
            "currency_id": "BRL",
            "unit_price": 1.00
        }],
        "notification_url": "https://bot-pix-telegram.onrender.com/webhook"
    }
    response = requests.post(url, json=data, headers=headers)
    link = response.json().get("init_point", "Erro ao gerar link.")
    bot.send_message(message.chat.id, f"Clique para pagar via Pix: {link}")

# Webhook para o Telegram
@app.route("/" + API_TOKEN, methods=["POST"])
def telegram_webhook():
    json_str = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "ok", 200

@app.route("/")
def index():
    return "Bot está rodando via webhook."

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url="https://bot-pix-telegram.onrender.com/" + API_TOKEN)
    app.run(host="0.0.0.0", port=10000)