import telebot

from Module.Tool.Struct import *


def strInArray(Array, String):
    for Object in Array:
        if (String.lower() in Object.lower()): return True

    return False


def checkStrBotCommand(Message, FirstCommand, LastCommand):
    return True if (Message.text == FirstCommand) or (Message.text == LastCommand) else False


def getCallBackStruct(CallBack):
    return CallBackStruct(CallBack.data.split(" ", 1)[0], CallBack.data.split(" ", 1)[1], CallBack.id, CallBack.message.chat.id, CallBack.message.from_user.id, CallBack.message.message_id)


def getRecordStruct(History):
    return RecordStruct(History[0], History[1], History[2])


def getSpecialLessonStruct(Message):
    Command = Message.text.split(" -", 6)
    return LessonStruct(int(Command[1]), Command[2], Command[3], Command[4], Command[5])


def getReducedScheduleStruct(Message):
    Command = Message.text.split(" -", 4)
    return ReducedScheduleStruct(int(Command[1]), int(Command[2]), Command[3])


def getSpecialDayStruct(Message):
    Command = Message.text.split(" -", 3)
    return SpecialDayStruct(Command[1], Command[2])


def getNotificationDescription(Message):
    Command = Message.text.split(" -", 2)
    return Command[1]


def setDefaultBotCommand(Bot: telebot.TeleBot, ChatID: int):
    Bot.set_my_commands(commands = [
        telebot.types.BotCommand("schedule", "Расписание занятий"),
        telebot.types.BotCommand("practice", "Расписание практик"),
        telebot.types.BotCommand("lessons", "Время занятий"),
        telebot.types.BotCommand("teachers", "Контакты преподавателей"),
        telebot.types.BotCommand("media", "Файлы"),
        telebot.types.BotCommand("switch", "Тип взаимодействия с ботом"),
        telebot.types.BotCommand("admin", "Панель администратора")
    ], 

    scope = telebot.types.BotCommandScopeChat(ChatID)
    )


def removeBotCommand(Bot: telebot.TeleBot, ChatID: int):
    Bot.set_my_commands(commands = [], scope = telebot.types.BotCommandScopeChat(ChatID))


def setDefaultBotKeyboard(Bot: telebot.TeleBot, ChatID: int):
    Markup = telebot.types.ReplyKeyboardMarkup(row_width = 1    , resize_keyboard = True)

    Button_1 = telebot.types.KeyboardButton("Расписание занятий")
    Button_2 = telebot.types.KeyboardButton("Расписание практик")
    Button_3 = telebot.types.KeyboardButton("Время занятий")
    Button_4 = telebot.types.KeyboardButton("Контакты преподавателей")
    Button_5 = telebot.types.KeyboardButton("Файлы")
    Button_6 = telebot.types.KeyboardButton("Тип взаимодействия с ботом")

    Markup.add(Button_1, Button_2, Button_3, Button_4, Button_5, Button_6)
    Bot.send_message(chat_id = ChatID, text = "Тип взаимодействия: КЛАВИАТУРА", reply_markup = Markup)


def removeDefaultBotKeyboard(Bot: telebot.TeleBot, ChatID: int):
    Bot.send_message(chat_id = ChatID, text = "Тип взаимодействия: КОМАНДЫ", reply_markup = telebot.types.ReplyKeyboardRemove())