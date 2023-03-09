
UserList = {}


def getUserActivePath(CharId: int):
    return "/".join(UserList[CharId]["activeFolder"])


def removeUserLastFolder(CharId: int):
    UserList[CharId]["activeFolder"].pop()


def setUserHomePath(CharId: int):
    UserList[CharId]["activeFolder"].clear()
    UserList[CharId]["activeFolder"].append("Media")


def getNextActivePath(CharId: int, Folder: str):
    return f"{getUserActivePath(CharId)}/{Folder}"


def addNewUserFolder(CharId: int, Folder: str):
    UserList[CharId]["activeFolder"].append(Folder)


def activePathIsHome(CharId: int):
    return len(UserList[CharId]["activeFolder"]) == 1