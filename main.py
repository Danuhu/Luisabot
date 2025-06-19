import os
import telebot
import mercadopago
from flask import Flask, request

# Tokens de ambiente (seguros)
API_TOKEN_TELEGRAM = os.environ.get("TELEGRAM_TOKEN")
ACCESS_TOKEN_MP = os.environ.get("MP_ACCESS_TOKEN")

bot = telebot.TeleBot(API_TOKEN_TELEGRAM)
sdk = mercadopago.SDK(ACCESS_TOKEN_MP)

# Flask app
app = Flask(__name__)
chat_ids = {}

@bot.message_handler(commands=['start'])
def boas_vindas(message):
    bot.reply_to(message, "Olá! Digite /pagar para gerar um Pix.")

@bot.message_handler(commands=['pagar'])
def pagar(message):
    chat_id = message.chat.id
    chat_ids[chat_id] = True

    preference_data = {
        "items": [{
            "title": "Pagamento via Pix",
            "quantity": 1,
            "unit_price": 10.00
        }],
        "notification_url": "https://SEU_LINK_RENDER/render/notify"
    }

    preference_response = sdk.preference().create(preference_data)
    link = preference_response["response"]["init_point"]
    bot.send_message(chat_id, "Seu link de pagamento Pix: {}".format(link))

@app.route("/render/notify", methods=["POST"])
def notificar():
    data = request.json
    print("Notificação recebida:", data)

    for cid in chat_ids:
        bot.send_message(cid, "✅ Pagamento confirmado com sucesso!")
    return "ok", 200

# Rodar bot + servidor Flask
import threading

def start_bot():
    bot.polling()

def start_web():
    app.run(host="0.0.0.0", port=10000)

threading.Thread(target=start_bot).start()
threading.Thread(target=start_web).start()
