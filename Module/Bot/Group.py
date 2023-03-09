
Students = {
}


def get():
    Count, Result = 1, ""

    for Group in Students:
        Result += f"* {Group}\n\n"
        
        for Student in Students[Group]:
            Result += f"[{Count}] {Student}\n"
            Count  += 1

        Result += "\n"

    return Result