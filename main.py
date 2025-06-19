
import os
import telebot
from flask import Flask, request

API_TOKEN = os.getenv("API_TOKEN")
MP_TOKEN = os.getenv("MP_TOKEN")

if not API_TOKEN:
    raise ValueError("API_TOKEN não definido. Verifique as variáveis de ambiente no Render.")
if not MP_TOKEN:
    raise ValueError("MP_TOKEN não definido. Verifique as variáveis de ambiente no Render.")

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start', 'pagar'])
def send_payment_link(message):
    link = "https://www.mercadopago.com.br/checkout/v1/redirect?pref_id=SEU_ID_AQUI"
    bot.send_message(message.chat.id, f"Clique para pagar via Pix: {link}")

@app.route(f"/{API_TOKEN}", methods=['POST'])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "OK", 200

@app.route("/", methods=['GET'])
def index():
    return "Bot Telegram com Webhook funcionando!", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    bot.remove_webhook()
    bot.set_webhook(url=f"https://bot-pix-telegram.onrender.com/{API_TOKEN}")
    app.run(host="0.0.0.0", port=port)
