from dataclasses import dataclass


@dataclass
class LessonStruct():
    Number  : int
    Item    : str
    Point   : str
    Teacher : str
    Date    : str = "" 


@dataclass
class CallBackStruct():
    Command    : str
    Arg        : str
    CallBackID : int
    ChatID     : int
    UserID     : int
    MessageID  : int


@dataclass
class SpecialDayStruct():
    Description : str
    Date        : str


@dataclass
class RecordStruct():
    Command   : str
    ChatID    : int
    MessageID : int


@dataclass
class ReducedScheduleStruct():
    Interval : int
    Lesson   : int
    Date     : str