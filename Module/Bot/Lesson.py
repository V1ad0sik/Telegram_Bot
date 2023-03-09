import Module.Bot.FlexTime as FlexTime
import Module.Bot.Setting as Setting
import Module.Bot.Replace as Replace

import Module.Tool.Time as Time
import Module.Tool.SQLite as SQLite
import Module.Tool.FilePath as FilePath

from Module.Tool.Struct import *
from Module.Tool.BotSDK import *


def getSchedule(DayName: str, Date: str):
    Schedule              = SQLite.readInfo(FilePath.Schedule, f"SELECT №, Предмет, Аудитория, Преподаватель FROM {DayName}")
    ScheduleForCurrentDay = dict({"Day": DayName, "Date": Date, "Args": list(), "Schedule": dict()})

    for Lesson in Schedule:
        ThisLesson = LessonStruct(Lesson[0], Lesson[1], Lesson[2], Lesson[3])

        ScheduleForCurrentDay["Schedule"][ThisLesson.Number] = {
             "Item": ThisLesson.Item,
             "Point": ThisLesson.Point,
             "Teacher": ThisLesson.Teacher
        }

    return ScheduleForCurrentDay


def setSpecialPairs(Schedule: dict, Date: str, ReplaceList = list()):
    Replace = (len(ReplaceList) != 0)

    SpecialPairs = SQLite.readInfo(FilePath.SpecialPairs, f"SELECT №, Предмет, Аудитория, Преподаватель FROM '{Date}'") if (not (Replace)) else ReplaceList
    Description  = list()

    for Lesson in SpecialPairs:
        ThisLesson = LessonStruct(Lesson[0], Lesson[1], Lesson[2], Lesson[3])

        if (ThisLesson.Number in Schedule.keys()):
            Schedule["Schedule"].update({ThisLesson.Number: { "Item": ThisLesson.Item, "Point": ThisLesson.Point, "Teacher": ThisLesson.Teacher}})

        else:
            Schedule["Schedule"][ThisLesson.Number] = {
                "Item": ThisLesson.Item,
                "Point": ThisLesson.Point,
                "Teacher": ThisLesson.Teacher
            }

            Description.append(ThisLesson.Number)

            
    if (Description):
        Description.sort()
        Description = list(map(str, Description))

        if (not strInArray(Schedule["Args"], "по ручной замене")):

            if (len(Description) == 1):
                Schedule["Args"].append(f"Пара по {'ручной' if not (Replace) else ''} замене: {', '.join(Description)}")
            
            else:
                Schedule["Args"].append(f"Пары по {'ручной' if not (Replace) else ''} замене: {', '.join(Description)}")


    for Arg in Setting.LessonArgs:
        if (not (Arg in Schedule["Args"])):
            Schedule["Args"].append(Arg)

        
    Schedule["Schedule"] = dict(sorted(Schedule["Schedule"].items()))
    return Schedule


def getSpecialDay(Day: str, Date: str):
    SpecialDay  = SQLite.readInfo(FilePath.SpecialDay, f"SELECT Описание FROM 'Специальные дни' WHERE Дата = '{Date}'")
    Description = ""

    for Number in SpecialDay:
        for DescriptionForThisDay in Number:
            Description = f"{Day.upper()}\n\n{DescriptionForThisDay}"

    return Description


def getTemporarySchedule(Day: str, Date: str):
    Schedule              = SQLite.readInfo(FilePath.TemporarySchedule, f"SELECT №, Предмет, Аудитория, Преподаватель FROM '{Date}'")
    ScheduleForCurrentDay = dict({"Day": Day, "Date": Date, "Args": list(), "Schedule": dict()}) if Schedule else dict()

    for Lesson in Schedule:
        ThisLesson = LessonStruct(Lesson[0], Lesson[1], Lesson[2], Lesson[3])

        ScheduleForCurrentDay["Schedule"][ThisLesson.Number] = {
             "Item": ThisLesson.Item,
             "Point": ThisLesson.Point,
             "Teacher": ThisLesson.Teacher
        }

    if (Schedule):
        ScheduleForCurrentDay["Args"].append("Временное расписание")

    return ScheduleForCurrentDay


def setTime(Schedule: dict, Date: str):
    Setting = SQLite.readInfo(FilePath.AbbreviatedСlasses, f"SELECT Интервал, Пара FROM 'Сокращенные пары' WHERE Дата = '{Date}'")
    Time = FlexTime.Default if not (Setting) else FlexTime.writeTimeSchedule(Setting[0][0], Setting[0][1])
    
    for Lesson in Schedule["Schedule"]:
        Number = Lesson
        Lesson = Schedule["Schedule"][Lesson]

        ThisLesson = LessonStruct(Number, Lesson["Item"], Lesson["Point"], Lesson["Teacher"])

        Schedule["Schedule"][ThisLesson.Number] = {
            "Item": ThisLesson.Item,
            "Point": ThisLesson.Point,
            "Teacher": ThisLesson.Teacher,
            "Time": Time[Number]
        }

    if (Setting):
        Schedule["Args"].append("Сокращенные пары")

    return Schedule


def lessonToStr(Schedule: dict):
    Lessons = f"{Schedule['Day'].upper()}"
    

    for Lesson in Schedule["Schedule"]:
        Number = Lesson
        Item = Schedule["Schedule"][Lesson]["Item"]
        Point = Schedule["Schedule"][Lesson]["Point"]
        Teacher = Schedule["Schedule"][Lesson]["Teacher"]
        Time = Schedule["Schedule"][Lesson]["Time"]["time"]

        Lessons += "\n\n"
        Lessons += (f"{Number}. НБ") if (Item.upper() == "НБ" or Item.upper() == "Н/Б") else (f"{Number}. {Item} ({Point}) [{Time}]\n> {Teacher}")


    if (Schedule["Args"]):
        Lessons += f"\n-----------------------------------------------"

        for Description in Schedule["Args"]:
            Lessons += f"\n* {Description}"

    return Lessons


def getLessons(Day: int):
    DayName    = Time.getDayName(Day)
    DateForDay = Time.getDateFromWeekdayStr(Day)

    Schedule   = getSpecialDay(DayName, DateForDay)

    if (not (Schedule)):
        Schedule = getTemporarySchedule(DayName, DateForDay)

        if (not (Schedule)):
            Schedule = getSchedule(DayName, DateForDay)
            Schedule = setSpecialPairs(Schedule, DateForDay, Replace.getReplace(Day)) if (Setting.API) else Schedule
            Schedule = setSpecialPairs(Schedule, DateForDay)
            Schedule = setTime(Schedule, DateForDay)

            return lessonToStr(Schedule)
        
        else:
            Schedule = setSpecialPairs(Schedule, DateForDay)
            Schedule = setTime(Schedule, DateForDay)

            return lessonToStr(Schedule)
        
    else:
        return Schedule