# Телеграм бот, осуществляющий функции форума для заинтересованных в деятельности УрФУ
import telebot
from telebot import types
import json


bot = None
with open('key.txt', 'r') as f:
    bot = telebot.TeleBot(f.readline())

previousMessage = {}
accesibleMessages = ["Допустимые", "предыдущие", "значения", "для", "ввода", "текущего", "значения"]

categories = None
# category = {
#   ID: int,
#   name: string,
#   parentID: int / int[],
# }
with open('categories.json', 'r', encoding="UTF-8") as f:
    categories = json.load(f)

questions = None
with open('questions.json', 'r', encoding="UTF-8") as f:
    questions = json.load(f)


def get_data(parentID: str, whatFind: str = "category", whereFind: str = "category", chatID: str = "") -> list: # Проверка ответных сообщений происходит тут
    result = []
    if whereFind == "category": # Выбор категории
        if parentID in precalculatedCategories:
            for c in precalculatedCategories[parentID]: # [ { (, ) }, {...}]
                if whatFind == "category":
                    result.append(c[1]) # (..., name)
        else:
            result.append("Назад")
        print()
        print(result)
        print()
        return result.copy()
    elif whereFind == "question": # Выбор вопроса
        if parentID in precalculatedQuestions:
            for q in precalculatedQuestions[parentID]: # [ { ... }, { ... }]
                if whatFind == "question":
                    result.append({"topic": q[2], "text": q[1]}) # (..., text, topic)
                elif whatFind == "answer": # Ответ пользователя
                    result.append({"text": q[1]}) # (..., text)
        return result.copy()
    return


def take_data(data: str, chatID: str = ""):
    # Проверка предыдущего веденного значения
    if previousMessage[chatID] in accesibleMessages:
        if previousMessage[chatID] == "Значение 1": # Создание вопроса
            # Отправление вопроса ИИ
            # Сохранение
            # data = {"ID": max(n)+1,
            #         "topic": some text 1,
            #         "text": some text 2,
            #         "parentID": const,
            #         "type": question
            #        }
            # with open("questions.json", "w") as f:
            #     json.dump(data, f, indent=4)
            pass
        elif previousMessage[chatID] == "Значение 2": # Переход в городское общежитие
            # Поиск узла с общагой указанного номера
            pass
        elif previousMessage[chatID] == "Значение 3": # Переход в НВК общежитие
            pass
        elif previousMessage[chatID] == "Значение 4": # 
            pass
        elif previousMessage[chatID] == "Значение 5": # 
            pass
        elif previousMessage[chatID] == "Значение 6": # 
            pass
    # Сохранение


def create_buttons(parentID) -> tuple:
    #return tuple(types.InlineKeyboardButton(text=name, callback_data=str(name)) for name in get_data(parentID, "category"))
    return tuple(types.KeyboardButton(name) for name in get_data(parentID, "category"))



precalculatedCategories={}
# precalculatedCategories = {
#   "1": [
#           (
#               nodeID: int,
#               nodeName: string,
#               nodeAnswer?: string,
#           ), 
#           (...)
#   ],
#   "2": ...,
# }
precalculatedQuestions={}
# precalculatedQuestions = {
#   "100": [
#           (
#               "ID": 100,
#               "topic": "Название вопроса",
#               "text": "Основной текст"
#           ), 
#           {
#              "ID": 101,
#              "text": "Текст ответа"
#           }
#(...)
#   ],
#   "200": ...,
# }

for node in categories: # Формирование дерева категорий
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
            if "answer" in node:
                precalculatedCategories[nextId] = [(node["ID"], node["name"], node["answer"])]
            else: 
                precalculatedCategories[nextId] = [(node["ID"], node["name"])]
        else:
            if "answer" in node:
                precalculatedCategories[nextId].append((node["ID"], node["name"], node["answer"]))
            else:
                precalculatedCategories[nextId].append((node["ID"], node["name"]))
            
for node in questions: # Формирование дерева вопросов
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
        if not nextId in precalculatedQuestions:
            if node["type"] == "question":
                precalculatedQuestions[nextId] = [(node["ID"], node["text"], node["topic"])]
            elif node["type"] == "answer":
                precalculatedQuestions[nextId] = [(node["ID"], node["text"])]
        else:
            if node["type"] == "question":
                precalculatedQuestions[nextId].append([(node["ID"], node["text"], node["topic"])])
            elif node["type"] == "answer":
                precalculatedQuestions[nextId].append([(node["ID"], node["text"])])

def create_menu(id: str):
    #menu = types.InlineKeyboardMarkup(row_width=1)
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for smth in create_buttons(id):
        menu.add(smth)
    #menu.add(*create_buttons(id))
    return menu

back = types.ReplyKeyboardMarkup(resize_keyboard=True)
back_button = types.KeyboardButton("Назад")
back.add(back_button)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Вы зашли в \"УРФУ-Форум\" / Хотите задать вопрос или посмотреть имеющиеся?", reply_markup = create_menu('0'))

specialList = ["Не Входящие В Иерархию Значения"]

def answer_to_message(messageText, chatID = None):
    idToFind = None
    answerText = "Выберите подкатегорию"
    menu = None
    for category in precalculatedCategories: # category: string (key)
        for node in precalculatedCategories[category]: # node: tuple
            if node[1] == messageText: # name
                if str(node[1]) in specialList: # Если будет введен текст
                    answerText = take_data(chatID = chatID)[0]
                    return (answerText, back)
                else:
                    idToFind = str(node[0])
                    menu = create_menu(idToFind)

                    if len(node) > 2:
                        answerText = node[2]

                    return (answerText, menu)
    return (answerText, menu)

"""@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    text_messages(call, isInlinePressed = True)"""


@bot.message_handler(content_types=["text"])
def text_messages(message, isInlinePressed = False):
    textOfMessage = ""
    idOfChat = 1
    if isInlinePressed:
        textOfMessage = message.data
        idOfChat = message.message.chat.id
    else:
        textOfMessage = message.text
        idOfChat = message.chat.id
    
    print(textOfMessage)
    previousMessage[idOfChat] = message
    answerText, menu = answer_to_message(textOfMessage, chatID = idOfChat)
    if textOfMessage == "Назад":
        bot.send_message(idOfChat, "Переход назад", reply_markup=create_menu('0'))
    else:
        bot.send_message(idOfChat, answerText, reply_markup=menu)
    

bot.infinity_polling()