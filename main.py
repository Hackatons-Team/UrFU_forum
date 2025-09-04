# Телеграм бот, осуществляющий функции форума для заинтересованных в деятельности УрФУ

import telebot
from telebot import types
import json


bot = None

with open('key.txt', 'r') as f:
    bot = telebot.TeleBot(f.readline())

categories = None
with open('categories.json', 'r', encoding="UTF-8") as f:
    categories = json.load(f)

# category = {
#   ID: int,
#   name: string,
#   parentID: int / int[],
# }

def get_categories(parentID: str) -> list:
    result = []
    for c in precalculatedCategories[parentID]: # [ { (, ) }, {...}]
        result.append(c[1]) # (id, name)
    return result.copy()

def create_buttons(parentID) -> tuple:
    return tuple(types.KeyboardButton(name) for name in get_categories(parentID))

precalculatedCategories={}
precalculatedCategories.keys()
for node in categories: # Формирование дерева вопросов
    cnt = 1
    isList = False
    if type(node["parentID"]) == type([]):
        cnt = len(node["parentID"])
        isList = True
    while cnt > 0:
        cnt -= 1
        nextId = None
        if isList:
            nextId = str(node["parentID"][cnt])
        else:
            nextId = str(node["parentID"])
        if not nextId in precalculatedCategories:
            precalculatedCategories[nextId] = [(node["ID"], node["name"])]
        else:
            precalculatedCategories[nextId].append((node["ID"], node["name"]))


menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
menu.add(*create_buttons('0'))

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