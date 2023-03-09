import os

import Module.Tool.SQLite as SQLite
import Module.Tool.Time as Time

from Module.Tool.IsAdmin import *
from Module.Tool.Struct import *
from Module.Tool.BotSDK import *


def saveLog(Message, Function):
    Name = f"[{Message.from_user.username}] {Message.from_user.first_name} {Message.from_user.last_name}"
    ID = Message.from_user.id
    ChatID = Message.chat.id

    DateLite = Time.getCurrentDateStr()
    TimeLite = Time.getCurrentTimeStr()

    if (not isAdmin(ChatID)):
        SQLite.writeInfo("DataBase/History.db", f"INSERT INTO История (ID, Имя, Команда, Время) VALUES ('{ID}', '{Name}', '{Function}', '{DateLite} {TimeLite}')")

    SQLite.writeInfo("DataBase/UserList.db", f"CREATE TABLE IF NOT EXISTS '{ChatID}' ('CallBack'  TEXT, 'ChatID' INT, 'MessageID' INT)")
    SQLite.writeInfo("DataBase/UserList.db", f"INSERT INTO '{ChatID}' ('CallBack', 'ChatID', 'MessageID') VALUES ('Command', {0}, {0})")


def saveCallBackLog(CallBack: CallBackStruct):
    SQLite.writeInfo("DataBase/UserList.db", f"CREATE TABLE IF NOT EXISTS '{CallBack.ChatID}' ('CallBack'  TEXT, 'ChatID' INT, 'MessageID' INT)")
    SQLite.writeInfo("DataBase/UserList.db", f"INSERT INTO '{CallBack.ChatID}' ('CallBack', 'ChatID', 'MessageID') VALUES ('{CallBack.Command}', {CallBack.ChatID}, {CallBack.MessageID + 1})")


def getLastRecord(CallBack):
    # tryExcept

    ChatID = CallBack.message.chat.id
    Record = SQLite.readInfo("DataBase/UserList.db", f"SELECT * FROM '{ChatID}' ORDER BY rowid DESC LIMIT 1")

    if (Record):
        return Record[0][0], Record[0][1], Record[0][2]
    
    else:
        return 0, 0, 0


def getFile():
    History = SQLite.readInfo("DataBase/History.db", "SELECT * FROM 'История'")
    Logs    = ""

    for Log in History:
        Logs += f"{Log[1]} | {Log[2]} | {Log[3]}\n"

    File = open("History.txt", "w", encoding = "utf-8")
    File.write(Logs)
    File.close()

    return Logs


def deleteFile(Path: str):
    try   : os.remove(Path)
    except: pass