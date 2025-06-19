
from flask import Flask, request
import os
import telebot
import mercadopago
import threading

app = Flask(__name__)

API_TOKEN_TELEGRAM = os.environ.get("TELEGRAM_TOKEN")
print("TOKEN DO TELEGRAM:", API_TOKEN_TELEGRAM)

ACCESS_TOKEN_MP = os.environ.get("MP_ACCESS_TOKEN")
print("TOKEN MP:", ACCESS_TOKEN_MP)

bot = telebot.TeleBot(API_TOKEN_TELEGRAM)
sdk = mercadopago.SDK(ACCESS_TOKEN_MP)

@app.route("/render/notify", methods=["POST"])
def webhook_notify():
    data = request.json
    print("Webhook recebido:", data)

    if data and data.get("type") == "payment":
        payment_id = data["data"]["id"]
        result = sdk.payment().get(payment_id)
        status = result["response"]["status"]
        external_reference = result["response"]["external_reference"]

        if status == "approved":
            bot.send_message(external_reference, "✅ Pagamento confirmado com sucesso!")

    return {"status": "ok"}, 200

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Olá! Envie /pagar para receber o link de pagamento Pix.")

@bot.message_handler(commands=["pagar"])
def pagar(message):
    preference_data = {
        "items": [{"title": "Pagamento via Pix", "quantity": 1, "unit_price": 1}],
        "payer": {"email": "comprador@email.com"},
        "notification_url": "https://bot-pix-telegram.onrender.com/render/notify",
        "external_reference": str(message.chat.id),
        "payment_methods": {"excluded_payment_types": [{"id": "credit_card"}]}
    }

    preference_response = sdk.preference().create(preference_data)
    init_point = preference_response["response"].get("init_point")

    # Tenta pegar o código Pix
    pix_code = (
        preference_response["response"]
        .get("point_of_interaction", {})
        .get("transaction_data", {})
        .get("qr_code")
    )

    if pix_code:
        mensagem = (
            "💸 *Seu Pix foi gerado!*

"
            "*Copia e Cola:*
"
            f"`{pix_code}`

"
            f"Ou clique abaixo para pagar:
{init_point}"
        )
        bot.send_message(message.chat.id, mensagem, parse_mode="Markdown")
    else:
        bot.send_message(
            message.chat.id,
            f"Não foi possível gerar o código Pix copia e cola. Mas você pode pagar por aqui:
{init_point}"
        )

if __name__ == "__main__":
    threading.Thread(target=bot.infinity_polling, daemon=True).start()
    app.run(host="0.0.0.0", port=10000)
