import Module.Bot.Setting as Setting


def isAdmin(UserID: int):
    return UserID in Setting.AdminList