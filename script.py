import pathlib
import textwrap
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import google.generativeai as genai
import json
import os
import logging
import PIL.Image
from io import BytesIO

# Список ID пользователей, которым разрешен доступ
ALLOWED_USER_IDS = [1474138637, 1474121637]

# Функция для проверки доступа пользователя
def check_user_access(update: Update) -> bool:
    return update.effective_user.id in ALLOWED_USER_IDS

# Функция для отправки сообщения о запрете доступа
def access_denied_message(update: Update):
    update.message.reply_text("У вас нет доступа к этому боту.")

# ... Ваш предыдущий код ...

# Функция для старта бота
def start(update: Update, context: CallbackContext):
    if not check_user_access(update):
        return access_denied_message(update)
    global chat
    update.message.reply_text("Привет! Я ваш чат-бот. ИДИ НАХУЙ. Отправьте мне сообщение, чтобы начать.")
    chat = model.start_chat(history=[])

# Функция для обработки текстовых сообщений
def handle_message(update: Update, context: CallbackContext):
    if not check_user_access(update):
        return access_denied_message(update)
    user_message = update.message.text
    global chat
    if chat is None:
        chat = model.start_chat(history=[])
    response = chat.send_message(user_message)
    response_text = response.text if hasattr(response, 'text') else "Извините, я не смог обработать ваш запрос."
    update.message.reply_text(response_text)

# Функция для обработки фотографий
def handle_photo(update: Update, context: CallbackContext):
    if not check_user_access(update):
        return access_denied_message(update)
    photo = update.message.photo[-1]
    file = context.bot.get_file(photo.file_id)
    file.download('photo.jpg')
    img = PIL.Image.open('photo.jpg')

    # ... Оставшаяся часть вашего кода для обработки фото ...

# Основная функция
def main():
    TOKEN = os.getenv("TELEGRAM_API_KEY")
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Добавляем обработчики
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dp.add_handler(MessageHandler(Filters.photo, handle_photo))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
