
import os
import telebot
from flask import Flask, request

API_TOKEN = os.getenv("API_TOKEN")

if not API_TOKEN:
    raise ValueError("API_TOKEN não definido. Verifique as variáveis de ambiente no Render.")

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

@app.route('/' + API_TOKEN, methods=['POST'])
def getMessage():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '', 200

@app.route('/')
def webhook():
    return 'Bot está online!', 200

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Olá! Envie /pagar para receber o link de pagamento Pix.")

@bot.message_handler(commands=['pagar'])
def send_payment(message):
    link_pagamento = "https://www.mercadopago.com.br/checkout/v1/redirect?pref_id=EXEMPLO"
    bot.reply_to(message, f"Clique para pagar via Pix: {link_pagamento}")

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url='https://bot-pix-telegram.onrender.com/' + API_TOKEN)
    app.run(host='0.0.0.0', port=10000)
