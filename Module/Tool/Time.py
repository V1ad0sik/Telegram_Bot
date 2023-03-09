import datetime
import locale, pymorphy2, calendar

# ЗАДАЕМ РУССКУЮ ЛОКАЛИЗАЦИЮ
locale.setlocale(locale.LC_ALL, 'ru_RU.utf8')


def getDayName(Day: int):
    return calendar.day_name[Day - 1].capitalize()


def getMonthName(Date: datetime):
    Morph = pymorphy2.MorphAnalyzer()
    Mounth = Morph.parse(Date.strftime("%B"))[0]
    Mounth = Mounth.inflect({'gent'})

    return Mounth.word


def getDateFromWeekday(Day: int):
    Today = datetime.datetime.now()

    Days = ((Day - 1) - Today.weekday() + 7) % 7
    Days = Today + datetime.timedelta(days = Days)

    Day = Days.day
    Month = getMonthName(Days)
    Year = Days.year

    return Day, Month, Year


def getDateFromWeekdayStr(Day: int):
    Date = getDateFromWeekday(Day = Day)
    return f"{Date[0]} {Date[1]} {Date[2]}"


def getDateFromWeekdayStrReplace(Day: int):
    Date = getDateFromWeekday(Day = Day)
    return f"{Date[0]:02} {Date[1]} {Date[2]}"


def normalizeTime(Seconds: int):
    Hours, Remainder  = divmod(Seconds.seconds, 3600)
    Minutes, Seconds  = divmod(Remainder, 60)

    return {"Hours": f"{Hours:02}", "Minutes": f"{Minutes:02}"}


def getCurrentDate():
    Today = datetime.datetime.now()

    Day = Today.strftime("%d")
    Month = getMonthName(Today)

    return Day, Month


def getCurrentDateStr():
    Date = getCurrentDate()
    return f"{Date[0]} {Date[1]}"


def getNextWorkingDay():
    Today = datetime.datetime.now()
    NextDay = Today + datetime.timedelta(days = 1)

    if (datetime.datetime.today().isoweekday() == 6):
        NextDay = Today + datetime.timedelta(days = 2)

    if (datetime.datetime.today().isoweekday() == 7):
        NextDay = Today + datetime.timedelta(days = 1)

    Day = NextDay.strftime("%d")
    Month = getMonthName(NextDay)

    return Day, Month


def getCurrentTimeStr():
    Date = datetime.datetime.now()
    return f"{Date.hour:02}:{Date.minute:02}"


def getDateTimeStr():
    Date = datetime.datetime.now()
    return f"{getCurrentDateStr()}, [{Date.hour:02}.{Date.minute:02}.{Date.second:02}]"