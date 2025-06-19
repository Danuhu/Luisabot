
import os
import telebot
from flask import Flask, request

API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    raise ValueError("API_TOKEN não definido. Verifique as variáveis de ambiente no Render.")

bot = telebot.TeleBot(API_TOKEN)

bot.remove_webhook()  # Linha que corrige o erro 409

app = Flask(__name__)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Olá! Eu sou um bot do Telegram.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

if __name__ == "__main__":
    bot.polling()
