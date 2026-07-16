import config
import telebot
bot = telebot.TeleBot(config.token)

dictionary={
    "/start":"Start bot work",
    "/help":"Show command list",
    "/bye":"Finish bot work"
}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""")

@bot.message_handler(commands=["bye"])
def send_bye(message):
    bot.reply_to(message, "Byee, see ya later")

@bot.message_handler(commands=["help"])
def send_help(message):
    text = ""
    for key, value in dictionary.items():
        text += f"{key} - {value}\n"

    bot.reply_to(message, text)

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()