import re


def slashDis(Name: str):
    Name = Name.lower()
    return Name


def removeTeacher(Name: str):
    return re.sub('\([^)]*\)', '()', Name).replace(")", "").replace("(", "")


def getTeacherInStr(Lesson: str):
    return Lesson.split("(")[-1].split(")")[0]
    

def getTeacher(Dis: str):
    return "Неизвестно"