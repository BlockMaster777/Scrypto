# coding=utf-8
""""
Main and the telegram bot logic
"""
import html
from db_manager import DBManager
from config import *
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = TeleBot(TOKEN)


def gen_cancel_button():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("⛔ Отмена ⛔", callback_data="cancel"))
    return markup


def gen_like_button(script_id):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("👍", callback_data="l"+ str(script_id)))
    return markup


def gen_search_results_markup(search_results):
    markup = InlineKeyboardMarkup()
    for result in search_results:
        markup.add(InlineKeyboardButton(f"{result[0]} | {result[2]} | {result[3]}👍 | {result[4]}👁️", callback_data="s" + str(result[1])))
    return markup



@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, """👋 Привет! Я бот-менеджер полезных скриптов!\n"""
                                      """Ты можешь сохранить здесь свой скрипт и поделиться им с остальным миром.\n\n"""
                                      
                                      """👋 /start | /help - вызвать это сообщение\n"""
                                      """📃 /upload_script - опубликовать скрипт\n"""
                                      """🗑️ /delete - удалить свой скрипт\n"""
                                      """🔎 /search - искать скрипты\n\n"""
                                      
                                      """🏭 Сделано @BlockMaster777\n"""
                                      
                                      """🤖 Исходный код - github.com/BlockMaster777/Scrypto""", disable_web_page_preview=True)


@bot.message_handler(commands=['upload_script'])
def upload_script(message):
    manager.register_user(message.from_user.username)
    bot.send_message(message.chat.id, "🆕 Отправь название для скрипта", reply_markup=gen_cancel_button())
    bot.register_next_step_handler(message, upload_name_for_script)


def upload_name_for_script(message):
    name = message.text
    user_id = manager.get_user_id(message.from_user.username)
    bot.send_message(message.chat.id, "✏️ Отправь мне описание скрипта", reply_markup=gen_cancel_button())
    bot.register_next_step_handler(message, upload_description_for_script, name=name, user_id=user_id)


def upload_description_for_script(message, name, user_id):
    description = message.text
    bot.send_message(message.chat.id, "📃 Отправь скрипт", reply_markup=gen_cancel_button())
    bot.register_next_step_handler(message, upload_script_final, name=name, user_id=user_id, description=description)


def upload_script_final(message, name, user_id, description):
    script = message.text
    manager.add_script(name, script, user_id, description)
    bot.send_message(message.chat.id, "✅ Готово! Скрипт опубликован!")


@bot.message_handler(commands=["search"])
def ask_search_name(message):
    bot.send_message(message.chat.id, "Отправь поисковый запрос", reply_markup=gen_cancel_button())
    bot.register_next_step_handler(message, search_script)


def search_script(message):
    search_text = " ".join(message.text.split()[1:]).lower()
    results = manager.search_scripts(search_text)
    if results:
        bot.send_message(message.chat.id, "📃 Выбери скрипт 📃", reply_markup=gen_search_results_markup(results))
    else:
        bot.send_message(message.chat.id, "🙈 Ничего не найдено!")


@bot.callback_query_handler(func=lambda call: call.data[0] == "s")
def select_script_for_view(call):
    script_id = call.data[1:]
    name = html.escape(manager.get_script_name(script_id))
    author = manager.get_script_author(script_id)
    description = html.escape(manager.get_script_description(script_id))
    script_text = html.escape(manager.get_script_data(script_id))
    manager.view_script(script_id)
    bot.edit_message_text(f"<strong>{name.capitalize()}</strong>\nОт @{author.capitalize()}\nОписание: {description.capitalize()}\n\n<pre><code>"
                     f"{script_text}</code></pre>", call.message.chat.id, call.message.message_id, parse_mode="html", reply_markup=gen_like_button(script_id))


@bot.callback_query_handler(func=lambda call: call.data[0] == "l")
def like_script(call):
    script_id = call.data[1:]
    manager.like_script(script_id)
    for entity in call.message.entities:
        if hasattr(entity, 'language'):
            if entity.language is None:
                entity.language = ""
            elif not isinstance(entity.language, str):
                entity.language = str(entity.language)
    bot.edit_message_text(call.message.text, call.message.chat.id, call.message.message_id, entities=call.message.entities, reply_markup=None)



@bot.callback_query_handler(func=lambda call: call.data == "cancel")
def cancel_button_handler(call):
    bot.clear_step_handler_by_chat_id(call.message.chat.id)
    bot.send_message(call.message.chat.id, "⛔ Отмена действия выполнена!")


if __name__ == '__main__':
    manager = DBManager(DATABASE_PATH)
    bot.infinity_polling()
