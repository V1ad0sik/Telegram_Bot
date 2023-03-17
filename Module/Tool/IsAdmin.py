from Module.Bot import Setting


def isAdmin(UserID: int):
    return UserID in Setting.AdminList