import telebot # библиотека telebot
from config import token # импорт токена
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import config as config
import telebot
from config import session, User
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot(config.token)
LOG_CHAT=-1004385885513

from telebot.types import ReplyKeyboardMarkup, KeyboardButton

@bot.message_handler(commands=["start"])
def start(message):
    user = session.query(User).filter_by(id=message.from_user.id).first()

    if user and user.verified:
        bot.send_message(message.chat.id, "✅ Добро пожаловать!")
        return

    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    button = KeyboardButton(
        "✅Подтвердить что вы не бот",
        request_contact=True
    )

    markup.add(button)

    bot.send_message(
        message.chat.id,
        "Для использования бота необходимо подтвердить что вы не бот.",
        reply_markup=markup
    )


@bot.message_handler(content_types=["contact"])
def contact_handler(message):
    user = session.query(User).filter_by(id=message.from_user.id).first()

    if not user:
        user = User(
            id=message.from_user.id,
            first_name=message.from_user.first_name,
            username=message.from_user.username,
            phone=message.contact.phone_number,
            verified=True
        )
        session.add(user)
    else:
        user.phone = message.contact.phone_number
        user.verified = True

    session.commit()

    bot.send_message(
        message.chat.id,
        "✅ Проверка успешно пройдена!"
    )

    bot.send_message(
        LOG_CHAT,
        f"""📥 Новый пользователь

ID: {message.from_user.id}
Имя: {message.from_user.first_name}
Username: @{message.from_user.username}
Телефон: {message.contact.phone_number}
"""
    )


def is_verified(user_id):
    user = session.query(User).filter_by(id=user_id).first()
    return user is not None and user.verified
def contact_handler(message):
    user = session.query(User).filter_by(id=message.from_user.id).first()

    if not user:
        user = User(
            id=message.from_user.id,
            first_name=message.from_user.first_name,
            username=message.from_user.username,
            phone=message.contact.phone_number,
            verified=True
        )
        session.add(user)
    else:
        user.phone = message.contact.phone_number
        user.verified = True

    session.commit()

    bot.send_message(
        message.chat.id,
        "✅ Вы успешно прошли проверку на бота!"
    )

dictionary={
    "/start":"Start bot work",
    "/help":"Show command list",
    "/bye":"Finish bot work"
}

@bot.message_handler(commands=["bye"])
def send_bye(message):
    bot.reply_to(message, "Byee, see ya later")

@bot.message_handler(commands=["help"])
def send_help(message):
    if not is_verified(message.from_user.id):
            bot.reply_to(
                message,
                "❌ Для использования бота сначала подтвердите что вы не бот."
            )
            return
    text = ""
    for key, value in dictionary.items():
        text += f"{key} - {value}\n"

    bot.reply_to(message, text)

@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.reply_to_message: #проверка на то, что эта команда была вызвана в ответ на сообщение 
        chat_id = message.chat.id # сохранение id чата
         # сохранение id и статуса пользователя, отправившего сообщение
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status 
         # проверка пользователя
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Невозможно забанить администратора.")
        else:
            bot.ban_chat_member(chat_id, user_id) # пользователь с user_id будет забанен в чате с chat_id
            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был забанен.")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите забанить.")

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text) 

bot.infinity_polling(none_stop=True)
