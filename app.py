import os
import flask
from flask import Flask, request
import telebot

# Token env var से लेंगे
TOKEN = os.environ.get('TOKEN')

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Bot handlers
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "नमस्ते! मैं echo bot हूँ। कुछ message भेजो, मैं वापस भेजूंगा। /start या /help के लिए ये message।")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)  # Echo back

# Webhook route
@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)

# Root route for health check
@app.route('/', methods=['GET'])
def index():
    return 'Bot is alive!'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
