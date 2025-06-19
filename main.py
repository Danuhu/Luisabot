
import os
import telebot
import mercadopago

# Configurações dos tokens via variáveis de ambiente
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
MERCADO_PAGO_TOKEN = os.getenv("MP_ACCESS_TOKEN")

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN não configurado.")
if not MERCADO_PAGO_TOKEN:
    raise ValueError("MP_ACCESS_TOKEN não configurado.")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

sdk = mercadopago.SDK(MERCADO_PAGO_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Olá! Envie /pagar para receber o link de pagamento Pix.")

@bot.message_handler(commands=['pagar'])
def gerar_link_pix(message):
    preference_data = {
        "items": [
            {
                "title": "Produto Exemplo",
                "quantity": 1,
                "unit_price": 1.00
            }
        ],
        "payment_methods": {
            "excluded_payment_types": [{"id": "credit_card"}],
            "installments": 1
        },
        "back_urls": {
            "success": "https://www.seusite.com/sucesso",
            "failure": "https://www.seusite.com/falha",
            "pending": "https://www.seusite.com/pendente"
        },
        "auto_return": "approved"
    }

    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]
    link_pagamento = preference["init_point"]

    bot.send_message(message.chat.id, f"💳 Clique para pagar via Pix: {link_pagamento}")

bot.infinity_polling()
