# Телеграм бот, осуществляющий функции форума для заинтересованных в деятельности УрФУ

import telebot
from telebot import types


bot = None

with open('key.txt', 'r') as f:
    bot = telebot.TeleBot(f.readline())

menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
name1 = types.KeyboardButton("Название 1") # Сделать прикол с JSON сериализацией из файла
name2 = types.KeyboardButton("Название 2")
name3 = types.KeyboardButton("Название 3")
name4 = types.KeyboardButton("Название 4")
name5 = types.KeyboardButton("Название 5")
menu.add(name1, name2, name3, name4, name5)

back = types.ReplyKeyboardMarkup(resize_keyboard=True)
back_button = types.KeyboardButton("Назад")
back.add(back_button)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет от Брекоткина", reply_markup = menu)

@bot.message_handler(content_types=["text"])
def text_messages(message):
    if message.text == "Назад":
        bot.send_message(message.chat.id, "Переход назад", reply_markup=menu)
    elif message.text == "Название 1":
        bot.send_message(message.chat.id, "Сообщение после нажатия на первое название", reply_markup=back)
    elif message.text == "Название 2":
        bot.send_message(message.chat.id, "Сообщение после нажатия на второе название", reply_markup=back)
    elif message.text == "Название 3":
        bot.send_message(message.chat.id, "Сообщение после нажатия на третье название", reply_markup=back)
    elif message.text == "Название 4":
        bot.send_message(message.chat.id, "Сообщение после нажатия на четвертое название", reply_markup=back)
    elif message.text == "Название 5":
        bot.send_message(message.chat.id, "Сообщение после нажатия на пятое название", reply_markup=back)

bot.infinity_polling()