# coding=utf-8
""""
Main and the telegram bot logic
"""
from db_manager import DBManager
from config import *
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = TeleBot(TOKEN)


def gen_cancel_button():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Отмена", callback_data="cancel"))
    return markup


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, """Привет! Я бот-менеджер полезных скриптов!
Ты можешь сохранить здесь свой скрипт и поделиться им с остальным миром.

/start - вызвать это сообщение
/upload_script - опубликовать скрипт

Сделано @BlockMaster777

Исходный код - github.com/BlockMaster777/Scrypto
""")


@bot.message_handler(commands=['upload_script'])
def upload_script(message):
    manager.register_user(message.from_user.username)
    bot.send_message(message.chat.id, "Отправь название для скрипта", reply_markup=gen_cancel_button())
    bot.register_next_step_handler(message, upload_name_for_script)


def upload_name_for_script(message):
    name = message.text
    user_id = manager.get_user_id(message.from_user.username)
    bot.send_message(message.chat.id, "Отправь мне описание скрипта ('-' чтобы не указывать)", reply_markup=gen_cancel_button())
    bot.register_next_step_handler(message, upload_description_for_script, name=name, user_id=user_id)


def upload_description_for_script(message, name, user_id):
    description = message.text
    bot.send_message(message.chat.id, "Отправь скрипт", reply_markup=gen_cancel_button())
    bot.register_next_step_handler(message, upload_script_final, name=name, user_id=user_id, description=description)


def upload_script_final(message, name, user_id, description):
    script = message.text
    manager.add_script(name, script, user_id=user_id, description="" if description == "-" else description)
    bot.send_message(message.chat.id, "Готово! Скрипт опубликован!")


@bot.message_handler(commands=["find"])
def find_script(message):
    # Функция не готова. Нужна для тестирования карточки скрипта.
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("MultiLine", callback_data="s5"))
    bot.send_message(message.chat.id, "Выбери", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data[0] == "s")
def select_script_for_view(call):
    script_id = call.data[1:]
    name = manager.get_script_name(script_id)
    author = manager.get_script_creator(script_id)
    description = manager.get_script_description(script_id)
    script_text = manager.get_script_data(script_id)
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Back", callback_data="find"))
    bot.send_message(call.message.chat.id,
                     f"*{name.capitalize()}*\nОт @{author.capitalize()}\nОписание: {description.capitalize()}\n\n```"f"\n{script_text}\n```",
                     parse_mode="MarkdownV2")


@bot.callback_query_handler(func=lambda call: call.data == "cancel")
def cancel_button_handler(call):
    bot.clear_step_handler_by_chat_id(call.message.chat.id)
    bot.send_message(call.message.chat.id, "Отмена действия выполнена!")


if __name__ == '__main__':
    manager = DBManager(DATABASE_PATH)
    bot.infinity_polling()