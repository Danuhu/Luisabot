
from flask import Flask, request
import telebot
import os

API_TOKEN = os.getenv("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

app = Flask(__name__)

@app.route('/' + API_TOKEN, methods=['POST'])
def getMessage():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/", methods=['GET'])
def webhook():
    bot.remove_webhook()
    webhook_url = os.getenv("RENDER_EXTERNAL_URL") + API_TOKEN
    bot.set_webhook(url=webhook_url)
    return "Webhook set!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
