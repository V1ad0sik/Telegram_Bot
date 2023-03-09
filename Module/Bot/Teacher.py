
List = {
    "Иванов И.И": {"Почта": "ivanov@mail.ru"},
    "Петров П.П": {"Почта": "petrov@mail.ru", "Телефон": "79000000000"},
    "Сидоров С.С": {"Почта": "sidorov@mail.ru"}
}


def getName():
    return list(List.keys())


def getInfo(Name):
    Result = f"{Name}\n"
    Info   = list(List[Name].keys())

    for i in range(len(Info)):
        Result += f"> {Info[i]}: {List[Name][Info[i]]}\n"

    return Result
