import telebot, traceback, time

import Module.Bot.FlexTime as FlexTime
import Module.Bot.Teacher as Teacher
import Module.Bot.Lesson as Lesson
import Module.Bot.Media as MediaContent
import Module.Bot.Group as Group
import Module.Bot.Practice as Practice

import Module.Tool.SQLite as SQLite
import Module.Tool.History as History
import Module.Tool.FilePath as FilePath
import Module.Tool.Files as Files
import Module.Tool.Users as Users
import Module.Tool.Time as Time

from Module.Tool.Struct import *
from Module.Tool.IsAdmin import *
from Module.Tool.BotSDK import *


# ВЫПОЛНИТЬ АВТОРИЗАЦИЮ
Bot = telebot.TeleBot(Setting.Token)


# ДОБАВИТЬ АРГУМЕНТ РАСПИСАНИЮ
# ====================================================================================================

@Bot.message_handler(commands = ["addSpecialArgForLesson"])
def addSpecialArgForLesson(Message):
    if (isAdmin(UserID = Message.from_user.id)):
        Command, Arg = Message.text.split(" -", 2)

        if (Arg in Setting.LessonArgs):
            Setting.LessonArgs.remove(Arg)
            Bot.send_message(chat_id = Message.chat.id, text = f"Аргумент '{Arg}' удален")

        else:
            Setting.LessonArgs.append(Arg)
            Bot.send_message(chat_id = Message.chat.id, text = f"Аргумент '{Arg}' добавлен")

    History.saveLog(Message, addSpecialArgForLesson.__name__)

# ====================================================================================================


# СОЗДАТЬ УВЕДОМЛЕНИЕ
# ====================================================================================================

@Bot.message_handler(commands = ["notification"])
def notification(Message):
    if (isAdmin(UserID = Message.from_user.id)):
        Description = getNotificationDescription(Message)
        ChatID   = SQLite.readInfo(FilePath.UserList,"SELECT name FROM sqlite_master where type = 'table'")

        for Chat in ChatID:
            try   : Bot.send_message(chat_id = int(Chat[0]), text = f"УВЕДОМЛЕНИЕ\n\n{Description}")
            except: pass
            
            time.sleep(0.1)

    History.saveLog(Message, notification.__name__)

# ====================================================================================================


# ВКЛЮЧИТЬ / ВЫКЛЮЧИТЬ ЗАМЕНЫ
# ====================================================================================================

@Bot.message_handler(commands = ["switchAPI"])
def switchAPI(Message):
    if (isAdmin(UserID = Message.from_user.id)):
        Setting.API = not(Setting.API)
        Bot.send_message(chat_id = Message.chat.id, text = f"Значение API изменено на {Setting.API}")

    History.saveLog(Message, switchAPI.__name__)

# ====================================================================================================

# РАСПИСАНИЕ ПРАКТИКИ
# ====================================================================================================

@Bot.message_handler(func = lambda message: (message.text == "/practice") or (message.text == "Расписание практик"))
def getPractice(Message):
    Bot.send_message(chat_id = Message.chat.id, text = Practice.get())
    History.saveLog(Message, getPractice.__name__)

# ====================================================================================================


# ИСТОРИЯ ПОЛЬЗОВАНИЯ
# ====================================================================================================

@Bot.message_handler(commands = ["history"])
def serverHistory(Message):
    if (isAdmin(UserID = Message.from_user.id)):
        History.getFile()
        Bot.send_document(chat_id = Message.chat.id, document = open(FilePath.History, "rb"))
        History.deleteFile(FilePath.History)

    History.saveLog(Message, serverHistory.__name__)

# ====================================================================================================

        
# СПИСОК ГРУППЫ
# ====================================================================================================

@Bot.message_handler(commands = ["group"])
def myGroup(Message):
    if (isAdmin(UserID = Message.from_user.id)):
        Bot.send_message(chat_id = Message.chat.id, text = Group.get())

    History.saveLog(Message, myGroup.__name__)

# ====================================================================================================


# ДОБАВИТЬ ЗАМЕНУ В РАСПИСАНИЕ
# ====================================================================================================

@Bot.message_handler(commands = ["setSpecialLesson"])
def setSpecialLesson(Message):
    if (isAdmin(UserID = Message.from_user.id)):
        Command = getSpecialLessonStruct(Message)

        SQLite.writeInfo(FilePath.SpecialPairs, f"CREATE TABLE IF NOT EXISTS '{Command.Date}' ('№' INTEGER, 'Предмет'  TEXT, 'Аудитория'  TEXT, 'Преподаватель'  TEXT)")

        if (SQLite.readInfo(FilePath.SpecialPairs, f"SELECT * FROM '{Command.Date}' WHERE № = {Command.Number}")):
            SQLite.writeInfo(FilePath.SpecialPairs, f"DELETE FROM '{Command.Date}' WHERE № = {Command.Number}")

            Bot.send_message(chat_id = Message.chat.id, text = f"[{Command.Date}] Замена удалена (№{Command.Number}).")

        else:
            SQLite.writeInfo(FilePath.SpecialPairs, f"INSERT INTO '{Command.Date}' (№, Предмет, Аудитория, Преподаватель) VALUES ('{Command.Number}', '{Command.Item}', '{Command.Point}',  '{Command.Teacher}')")
            Bot.send_message(chat_id = Message.chat.id, text = f"[{Command.Date}] Замена добавлена.")

    History.saveLog(Message, setSpecialLesson.__name__)

# ====================================================================================================


# ДОБАВИТЬ СПЕЦИАЛЬНОЕ РАСПИСАНИЕ
# ====================================================================================================

@Bot.message_handler(commands = ["addSchedule"])
def addSchedule(Message):
    if (isAdmin(UserID = Message.from_user.id)):
        Command = getSpecialLessonStruct(Message)

        SQLite.writeInfo(FilePath.TemporarySchedule, f"CREATE TABLE IF NOT EXISTS '{Command.Date}' ('№' INTEGER, 'Предмет'  TEXT, 'Аудитория'  TEXT, 'Преподаватель'  TEXT)")

        if (SQLite.readInfo(FilePath.TemporarySchedule, f"SELECT * FROM '{Command.Date}' WHERE № = {Command.Number}")):
            SQLite.writeInfo(FilePath.TemporarySchedule, f"DELETE FROM '{Command.Date}' WHERE № = {Command.Number}")
            Bot.send_message(chat_id = Message.chat.id, text = f"[{Command.Date}] Данные удалены ({Command.Number}).")

        else:
            SQLite.writeInfo(FilePath.TemporarySchedule, f"INSERT INTO '{Command.Date}' (№, Предмет, Аудитория, Преподаватель) VALUES ('{Command.Number}', '{Command.Item}', '{Command.Point}',  '{Command.Teacher}')")
            Bot.send_message(chat_id = Message.chat.id, text = f"[{Command.Date}] Расписание добавлено.")

    History.saveLog(Message, addSchedule.__name__)

# ====================================================================================================
    

# ДОБАВИТЬ СПЕЦИАЛЬНЫЙ ДЕНЬ
# ====================================================================================================

@Bot.message_handler(commands = ["setSpecialDay"])
def specialDay(Message):
    if (isAdmin(UserID = Message.from_user.id)):
        Command = getSpecialDayStruct(Message)

        if (SQLite.readInfo(FilePath.SpecialDay, f"SELECT * FROM 'Специальные дни' WHERE Дата = '{Command.Date}' LIMIT 1")):
            SQLite.writeInfo(FilePath.SpecialDay, f"DELETE FROM 'Специальные дни' WHERE Дата = '{Command.Date}'")

            Bot.send_message(chat_id = Message.chat.id, text = f"[{Command.Date}] Специальный день удален.")

        else:
            SQLite.writeInfo(FilePath.SpecialDay, f"INSERT INTO 'Специальные дни' ('Описание', 'Дата') VALUES ('{Command.Description}', '{Command.Date}')")
            Bot.send_message(chat_id = Message.chat.id, text = f"[{Command.Date}] Специальный день ({Command.Description}) добавлен.")

    History.saveLog(Message, specialDay.__name__)

# ====================================================================================================


# УСТАНОВИТЬ СОКРАЩЕННОЕ ВРЕМЯ НА ОПРЕДЕЛЕННЫЙ ДЕНЬ
# ====================================================================================================

@Bot.message_handler(commands = ["setReducedSchedule"])
def reducedSchedule(Message):
    if (isAdmin(UserID = Message.from_user.id)):
        Command = getReducedScheduleStruct(Message)

        if (SQLite.readInfo(FilePath.AbbreviatedСlasses, f"SELECT * FROM 'Сокращенные пары' WHERE Дата = '{Command.Date}' LIMIT 1")):
            SQLite.writeInfo(FilePath.AbbreviatedСlasses, f"DELETE FROM 'Сокращенные пары' WHERE Дата = '{Command.Date}'")

            Bot.send_message(chat_id = Message.chat.id, text = f"[{Command.Date}] Сокращенные пары удалены.")

        else:
            SQLite.writeInfo(FilePath.AbbreviatedСlasses, f"INSERT INTO 'Сокращенные пары' (Интервал, Пара, Дата) VALUES ('{Command.Interval}', '{Command.Lesson}', '{Command.Date}')")
            Bot.send_message(chat_id = Message.chat.id, text = f"[{Command.Date}] Сокращенные пары установлены (interval = {Command.Interval}, lesson = {Command.Lesson})")

    History.saveLog(Message, reducedSchedule.__name__)

# ====================================================================================================


# ПАНЕЛЬ АДМИНИСТРАТОРА
# ====================================================================================================

@Bot.message_handler(commands = ["admin"])
def admin(Message):
    if (isAdmin(UserID = Message.from_user.id)):
        Bot.send_message(chat_id = Message.chat.id, text = "/setReducedSchedule -interval -lesson -date")
        Bot.send_message(chat_id = Message.chat.id, text = "/addSchedule -№ -item -point -teacher -date")
        Bot.send_message(chat_id = Message.chat.id, text = "/setSpecialLesson -№ -item -point -teacher -date")
        Bot.send_message(chat_id = Message.chat.id, text = "/setSpecialDay -description -date")
        Bot.send_message(chat_id = Message.chat.id, text = "/addSpecialArgForLesson -description")
        Bot.send_message(chat_id = Message.chat.id, text = "/notification -description")
        Bot.send_message(chat_id = Message.chat.id, text = "/switchAPI")
        Bot.send_message(chat_id = Message.chat.id, text = "/group")
        Bot.send_message(chat_id = Message.chat.id, text = "/history")

    History.saveLog(Message, admin.__name__)

# ====================================================================================================


# ДОБАВЛЯЕМ КОМАНДЫ ПО НАЧАЛУ РАБОТЫ
# ====================================================================================================

@Bot.message_handler(commands = ["start"])
def start(Message):
    setDefaultBotCommand(Bot, Message.chat.id)
    History.saveLog(Message, start.__name__)

# ====================================================================================================


# ИЗМЕНИТЬ ТИП ВЗАИМОДЕЙСТВИЯ С БОТОМ
# ====================================================================================================

@Bot.message_handler(func = lambda Message: checkStrBotCommand(Message, "/switch", "Тип взаимодействия с ботом"))
def switch(Message):
    Markup = telebot.types.InlineKeyboardMarkup(row_width = 1)

    Button_1 = telebot.types.InlineKeyboardButton("Команды", callback_data = "!switch commands")
    Button_2 = telebot.types.InlineKeyboardButton("Клавиатура", callback_data = "!switch keyboard")

    Markup.add(Button_1, Button_2)
    Bot.send_message(chat_id = Message.chat.id, text = "Выберите тип взаимодействия", reply_markup = Markup)

    History.saveLog(Message, switch.__name__)

# ====================================================================================================


# РАСПИСАНИЕ ЗАНЯТИЙ
# ====================================================================================================

@Bot.message_handler(func = lambda Message: checkStrBotCommand(Message, "/schedule", "Расписание занятий"))
def schedule(Message):
    Markup = telebot.types.InlineKeyboardMarkup(row_width = 1)

    Button_1 = telebot.types.InlineKeyboardButton("Понедельник", callback_data = "!расписание 1")
    Button_2 = telebot.types.InlineKeyboardButton("Вторник", callback_data = "!расписание 2")
    Button_3 = telebot.types.InlineKeyboardButton("Среда", callback_data = "!расписание 3")
    Button_4 = telebot.types.InlineKeyboardButton("Четверг", callback_data = "!расписание 4")
    Button_5 = telebot.types.InlineKeyboardButton("Пятница", callback_data = "!расписание 5")
    Button_6 = telebot.types.InlineKeyboardButton("Суббота", callback_data = "!расписание 6")

    Markup.add(Button_1, Button_2, Button_3, Button_4, Button_5, Button_6)

    Bot.send_message(chat_id = Message.chat.id, text = f"Какой день недели?", reply_markup = Markup)
    History.saveLog(Message, schedule.__name__)

# ====================================================================================================


# ВРЕМЯ ЗАНЯТИЙ
# ====================================================================================================

@Bot.message_handler(func = lambda Message: checkStrBotCommand(Message, "/lessons", "Время занятий"))
def lessonsTime(Message):
    Bot.send_message(chat_id = Message.chat.id, text = FlexTime.get())
    History.saveLog(Message, lessonsTime.__name__)

# ====================================================================================================


# КОНТАКТЫ ПРЕПОДАВАТЕЛЕЙ
# ====================================================================================================

@Bot.message_handler(func = lambda Message: checkStrBotCommand(Message, "/teachers", "Контакты преподавателей"))
def teachers(Message):
        Markup = telebot.types.InlineKeyboardMarkup(row_width = 1)
        List = Teacher.getName()

        for Number in range(len(List)):
            Markup.add(telebot.types.InlineKeyboardButton(List[Number], callback_data = f"!преподаватель {List[Number]}"))


        Bot.send_message(chat_id = Message.chat.id, text = "Список преподавателей", reply_markup = Markup)
        History.saveLog(Message, teachers.__name__)


# ====================================================================================================


# ОТПРАВКА МЕДИА-ФАЙЛОВ
# ====================================================================================================

@Bot.message_handler(func = lambda Message: checkStrBotCommand(Message, "/media", "Файлы"))
def mediaFiles(Message):
    ChatId = Message.chat.id
    Markup = telebot.types.InlineKeyboardMarkup(row_width = 1)
    
    Folders = list(Files.getFileList("Media").keys())
    Folders = Files.sortByName(Folders)

    if (ChatId not in Users.UserList):
        Users.UserList[ChatId] = {"activeFolder": ["Media"]}

    else:
        Users.setUserHomePath(ChatId)

    for Folder in range(len(Folders)):
        Markup.add(telebot.types.InlineKeyboardButton(f"{Folders[Folder]}", callback_data = f"!открыть {Folders[Folder]}"))

    Bot.send_message(chat_id = Message.chat.id, text = "Media", reply_markup = Markup)
    History.saveLog(Message, mediaFiles.__name__)

# ====================================================================================================


# ОБРАБОТЧИК СОБЫТИЙ
# ====================================================================================================

@Bot.callback_query_handler(func = lambda CallBack: True)
def callBackHandler(CallBack):
    Message    = getCallBackStruct(CallBack)
    LastRecord = getRecordStruct(History.getLastRecord(CallBack))


    if (Message.Command == "!преподаватель"):
        if (LastRecord.Command == Message.Command):
            try   : Bot.edit_message_text(chat_id = LastRecord.ChatID, message_id = LastRecord.MessageID, text = Teacher.getInfo(Name = Message.Arg))
            except: pass

        else:
            Bot.send_message(chat_id = Message.ChatID, text = Teacher.getInfo(Name = Message.Arg))


    if (Message.Command == "!отправить"):
        Path = Users.getNextActivePath(Message.ChatID, Message.Arg)
        
        if (Files.isFile(Path)):
           Bot.send_document(chat_id = Message.ChatID, document = open(Path, "rb"))


    if (Message.Command == "!расписание"):
        if (LastRecord.Command == Message.Command):
            try   : Bot.edit_message_text(chat_id = LastRecord.ChatID, message_id = LastRecord.MessageID, text = Lesson.getLessons(int(Message.Arg)))
            except: pass

        else:
            Bot.send_message(chat_id = Message.ChatID, text = Lesson.getLessons(int(Message.Arg)))


    if (Message.Command == "!открыть"):
        if (Message.ChatID in Users.UserList):
            Folder = Users.addNewUserFolder(Message.ChatID, Message.Arg)
            Folder = Users.getUserActivePath(Message.ChatID)

            Folders = list(Files.getFileList(Folder))
            Folders = Files.sortFiles(Folders)

            Markup = telebot.types.InlineKeyboardMarkup(row_width = 1)

            for Path in Folders:
                ActivePath = Users.getNextActivePath(Message.ChatID, Path)

                if (Files.isFile(ActivePath)):
                    Size = "~1" if Files.getFileSize(ActivePath) < 1 else Files.getFileSize(ActivePath)
                    Markup.add(telebot.types.InlineKeyboardButton(f"{Path} ({Size} МБ)", callback_data = f"!отправить {Path}"))
 
                else:
                    Markup.add(telebot.types.InlineKeyboardButton(f"{Path}", callback_data = f"!открыть {Path}"))


            Markup.add(telebot.types.InlineKeyboardButton(f"⬅️", callback_data = f"!назад CallBack"))
                
            try   : Bot.edit_message_text(chat_id = Message.ChatID, message_id = Message.MessageID, text = Folder, reply_markup = Markup) 
            except: Bot.send_message(chat_id = Message.ChatID, text = Folder, reply_markup = Markup)


    if (Message.Command == "!назад"):
        if (Message.ChatID in Users.UserList):
            Users.removeUserLastFolder(Message.ChatID)

            Folder = Users.getUserActivePath(Message.ChatID)
            Folders = list(Files.getFileList(Folder))

            if (not Users.activePathIsHome(Message.ChatID)):
                Folders = Files.sortFiles(Folders)
            
            else:
                Folders = Files.sortByName(Folders)

            Markup = telebot.types.InlineKeyboardMarkup(row_width = 1)

            for Path in Folders:
                ActivePath = Users.getNextActivePath(Message.ChatID, Path)

                if (Files.isFile(ActivePath)):
                    Size = "~1" if Files.getFileSize(ActivePath) < 1 else Files.getFileSize(ActivePath)
                    Markup.add(telebot.types.InlineKeyboardButton(f"{Path} ({Size} МБ)", callback_data = f"!отправить {Path}"))

                else:
                    Markup.add(telebot.types.InlineKeyboardButton(f"{Path}", callback_data = f"!открыть {Path}"))

            if (not Users.activePathIsHome(Message.ChatID)):
                Markup.add(telebot.types.InlineKeyboardButton(f"⬅️", callback_data = f"!назад CallBack"))

            try   : Bot.edit_message_text(chat_id = Message.ChatID, message_id = Message.MessageID, text = Folder, reply_markup = Markup) 
            except: Bot.send_message(chat_id = Message.ChatID, text = Folder, reply_markup = Markup)


    if (Message.Command == "!switch"):
        if (Message.Arg == "commands"):
            removeDefaultBotKeyboard(Bot, Message.ChatID)
            setDefaultBotCommand(Bot, Message.ChatID)
        
        elif (Message.Arg == "keyboard"):
            removeBotCommand(Bot, Message.ChatID)
            setDefaultBotKeyboard(Bot, Message.ChatID)


    Bot.answer_callback_query(Message.CallBackID)
    History.saveCallBackLog(Message)


# ====================================================================================================


while (True):
    try:
        Bot.polling(timeout = 10)

    except Exception:
        Except = traceback.format_exc()
        
        File = open(f"Logs/log {Time.getDateTimeStr()}.txt", "w")
        File.write(Except)
        File.close()

        print(f"[EXCEPT]\n\n{Except}\n\n")