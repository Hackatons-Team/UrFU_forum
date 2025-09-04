# Телеграм бот, осуществляющий функции форума для заинтересованных в деятельности УрФУ
import telebot
from telebot import types
import json


bot = None
with open('key.txt', 'r') as f:
    bot = telebot.TeleBot(f.readline())

previousMessage = {}
previousQuestion = {}
accesibleMessages = ["Введите вопрос", "Напиши то, что помогло тебе или поможет абитуриенту"]

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

def send_question(topic, chatID=None):
    bot.send_message(chatID, f"Тема существующего вопроса: {topic}", reply_markup=create_menu(previousMessage[chatID]))



def get_data(parentID: str, whatFind: str = "category", whereFind: str = "category", chatID: str = "") -> list: # Проверка ответных сообщений происходит тут
    result = []
    if whereFind == "category": # Выбор категории
        if parentID in precalculatedCategories:
            for c in precalculatedCategories[parentID]: # [ { (, ) }, {...}]
                if "itsquestion" in c:
                    send_question(c[2], chatID=chatID) # (..., ..., topic)
                    return get_data(parentID, whatFind="question", whereFind="question", chatID=chatID)
                elif whatFind == "category":
                    result.append(c[1]) # (..., name)
        else:
            result.append("Назад")
        return result.copy()
    elif whereFind == "question": # Выбор вопроса get_data(smID, "question", "question")
        result.append("itsquestion")
        if parentID in precalculatedQuestions:
            for idx in range(len(precalculatedQuestions[parentID])): # [ { ... }, { ... }]
                q = precalculatedQuestions[parentID][idx]
                if whatFind == "question":
                    result.append({"topic": q[2], "text": q[1]}) # (..., text, topic)
                    previousQuestion[chatID] = q[2]
                elif whatFind == "answer": # Ответ пользовател        
                    result.append(q[1]) # (..., text)
        return result.copy()
    return


def take_data(data: str, chatID: str = ""):
    # Проверка предыдущего веденного значения
    if previousMessage[chatID] in accesibleMessages:
        if previousMessage[chatID] == "Введите вопрос": # Создание вопроса
            # Отправление вопроса ИИ
            # Сохранение
            maxID = 0
            for i in categories:
                if int(i["ID"]) > maxID:
                    maxID = int(i["ID"])
            local_data = {
                "ID": maxID+1,
                "topic": data,
                "text": "",
                "parentID": 9,
                "type": "question"
                }
            '''with open("questions.json", "w+") as f:
                someunuseful = json.load(f)
                print(len(someunuseful))
                someunuseful.append(local_data)
                print(len(someunuseful))
                json.dump(someunuseful, f, indent=4)

            local_data['name'] = local_data['topic']

            with open("categories.json", "w+") as f:
                someunuseful = json.load(f)
                print(len(someunuseful))
                someunuseful.append(local_data)
                print(len(someunuseful))
                json.dump(local_data, f, indent=4)'''
            print("Вопрос:", end=" ")
            bot.send_message(chatID, "Данные сохранены", reply_markup=back)
        elif previousMessage[chatID] == "Городские": # Переход в городское общежитие
            # Поиск узла с общагой указанного номера
            pass
        elif previousMessage[chatID] == "НВК": # Переход в НВК общежитие
            pass
        elif previousMessage[chatID] == "Напиши то, что помогло тебе или поможет абитуриенту": # Запись ответа на вопрос
            bot.send_message(chatID, "Ответ записан", reply_markup=back)
        elif previousMessage[chatID] == "Значение 5": # 
            pass
        elif previousMessage[chatID] == "Значение 6": # 
            pass
    # Сохранение



def create_buttons(parentID, chatID=None) -> tuple:
    #return tuple(types.InlineKeyboardButton(text=name, callback_data=str(name)) for name in get_data(parentID, "category"))
    data = get_data(parentID, "category", chatID=chatID)
    if data[0] != "itsquestion":
        result = []
        for name in data:
            result.append(types.KeyboardButton(name))
        return tuple(result)
    else:
        #data = data[1:]
        return "создать кнопки вопросов"



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
            elif "topic" in node:
                precalculatedCategories[nextId] = [(node["ID"], node["name"], node["topic"], "itsquestion")]
            else: 
                precalculatedCategories[nextId] = [(node["ID"], node["name"])]
        else:
            if "answer" in node:
                precalculatedCategories[nextId].append((node["ID"], node["name"], node["answer"]))
            elif "topic" in node:
                precalculatedCategories[nextId].append((node["ID"], node["name"], node["topic"], "itsquestion"))
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
                precalculatedQuestions[nextId].append((node["ID"], node["text"], node["topic"]))
            elif node["type"] == "answer":
                precalculatedQuestions[nextId].append((node["ID"], node["text"]))


def createQuestionButtons():
    return [types.KeyboardButton("Просмотреть ответы"),
            types.KeyboardButton("Написать ответ")]

def create_menu(id: str, chatID=None):
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    tmp_res = create_buttons(id, chatID=chatID)
    if tmp_res != "создать кнопки вопросов":
        for smth in create_buttons(id, chatID=chatID):
            menu.add(smth)
    else:
        for smth in createQuestionButtons():
            menu.add(smth)
        return (menu, "Можете как добавить ответы, так и просмотреть существующие")
    return menu

back = types.ReplyKeyboardMarkup(resize_keyboard=True)
back_button = types.KeyboardButton("Назад")
back.add(back_button)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Вы зашли в \"УРФУ-Форум\" / Хотите задать вопрос или посмотреть имеющиеся?", reply_markup = create_menu('0'))

specialList = ["Введите вопрос"]

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
                    menu = create_menu(idToFind, chatID=chatID)

                    if len(node) > 2:
                        answerText = node[2]
                    try:
                        if len(menu) > 1:
                            answerText = menu[1]
                            menu = menu[0]
                    except:
                        pass
                    

                    return (answerText, menu)
    return (answerText, menu)


@bot.message_handler(content_types=["text"])
def text_messages(message, isInlinePressed = False):
    
    textOfMessage = "" # Сообщение от пользователя
    idOfChat = 1 
    if isInlinePressed:
        textOfMessage = message.data
        idOfChat = message.message.chat.id
    else:
        textOfMessage = message.text
        idOfChat = message.chat.id
        
    if not idOfChat in previousMessage:
        previousMessage[idOfChat] = ""

    if not idOfChat in previousQuestion:
        previousQuestion[idOfChat] = ""
        
    if textOfMessage == "Просмотреть ответы":
        # Найти Ид вопроса
        idToPaste = None
        for ww in precalculatedQuestions:
            if previousQuestion[idOfChat] in precalculatedQuestions[ww][0]: # Если это тот вопрос
                idToPaste = str(precalculatedQuestions[ww][0][0])
        t = get_data(idToPaste, whatFind = "answer", whereFind = "question")
        for mes in t[1:]:
            bot.send_message(idOfChat, mes)
        bot.send_message(idOfChat, "Конец ответов", reply_markup=back)
        return

    
    if previousMessage[idOfChat] in accesibleMessages:
        take_data(textOfMessage, idOfChat) # Обработка занесения данных
        previousMessage[idOfChat] = textOfMessage
        return
    
    
    
    answerText, menu = answer_to_message(textOfMessage, chatID = idOfChat)
    if textOfMessage == "Назад":
        bot.send_message(idOfChat, "Переход назад", reply_markup=create_menu('0'))
        previousMessage[idOfChat] = "Переход назад"
    else:
        bot.send_message(idOfChat, answerText, reply_markup=menu)
    previousMessage[idOfChat] = answerText

bot.infinity_polling()