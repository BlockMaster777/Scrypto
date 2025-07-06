# coding=utf-8
""""
Main and the telegram bot logic
"""
from db_manager import DBManager
from config import *
from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

bot = TeleBot(TOKEN)


def gen_markup(rows):
    markup = ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 1
    for row in rows:
        markup.add(KeyboardButton(row))
    return markup


@bot.message_handler(commands=['start'])
def start_command(message):
    manager.register_user(message.from_user.username)
    bot.send_message(message.chat.id, """Привет! Я бот-менеджер полезных скриптов!
Ты можешь сохранить здесь свой скрипт и поделиться им с остальным миром.)

/start - вызвать это сообщение
/upload_script - опубликовать скрипт

Сделано @BlockMaster777

Исходный код - github.com/BlockMaster777/Scrypto
""")


@bot.message_handler(commands=['upload_script'])
def upload_script(message):
    bot.send_message(message.chat.id, "Отправь название для скрипта")
    bot.register_next_step_handler(message, upload_name_for_script)


def upload_name_for_script(message):
    name = message.text
    user_id = manager.get_user_id(message.from_user.username)
    bot.send_message(message.chat.id, "Отправь мне описание скрипта ('-' чтобы не указывать)")
    bot.register_next_step_handler(message, upload_description_for_script, name=name, user_id=user_id)


def upload_description_for_script(message, name, user_id):
    description = message.text
    bot.send_message(message.chat.id, "Отправь скрипт")
    bot.register_next_step_handler(message, upload_script_final, name=name, user_id=user_id, description=description)


def upload_script_final(message, name, user_id, description):
    script = message.text
    manager.add_script(name, script, user_id=user_id, description="" if description == "-" else description)
    bot.send_message(message.chat.id, "Готово! Скрипт опубликован!")


if __name__ == '__main__':
    manager = DBManager(DATABASE_PATH)
    bot.infinity_polling()