import datetime

import Module.Tool.Time as Time


Default = {
    1: {"time": "8.00 - 9.30"},
    2: {"time": "9.40 - 11.10"},
    3: {"time": "11.30 - 13.00"},
    4: {"time": "13.10 - 14.40"},
    5: {"time": "15.00 - 16.30"},
    6: {"time": "16.40 - 18.10"},
    7: {"time": "18.20 - 19.50"}
}


def writeTimeSchedule(interval, lesson):
    TimeSchedule, Parsed = dict(), False

    for i in range(1, len(Default.keys()) + 1):
        if (i >= lesson):
            StartEndTime = (Default[i]["time"].split(" - ") if (i > 1) else Default[i]["time"].split(" - ")) if (not Parsed) else TimeSchedule[i - 1]["time"].split(" - ")

            Hours   = int(StartEndTime[0].split('.')[0]) if (not Parsed) else int(StartEndTime[1].split('.')[0])
            Minutes = int(StartEndTime[0].split('.')[1]) if (not Parsed) else int(StartEndTime[1].split('.')[1])

            Start = datetime.timedelta(hours = Hours, minutes = Minutes) if (not Parsed) else datetime.timedelta(hours = Hours, minutes = Minutes) + datetime.timedelta(minutes = 10)
            End   = Start + datetime.timedelta(minutes = interval)

            Start = Time.normalizeTime(Start)
            End   = Time.normalizeTime(End)

            TimeSchedule[i] = {"time": f"{Start['Hours']}.{Start['Minutes']} - {End['Hours']}.{End['Minutes']}"}

            if (not Parsed): Parsed = True

        else:
            TimeSchedule[i] = Default[i]


    return TimeSchedule


def get():
    Result = ""

    for Lesson in range(1, len(Default) + 1):
        Result += f"{Lesson}. {Default[Lesson]['time']}\n"

    return Result