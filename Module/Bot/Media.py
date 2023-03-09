import Module.Tool.Files as FilesSDK


def getMedia(Folder: str):
    Files = FilesSDK.getFiles(Folder)
    Files = FilesSDK.sortFiles(Files)

    Media = dict()

    for Index in range(len(Files)):
        Name = FilesSDK.getFileName(Files[Index])
        Path = f"{Folder}/{Name}"
        Size = FilesSDK.getFileSize(Path)

        Media[Name] = f"({Size} МБ)" if Size > 0 else f"(~ 1 МБ)"

    return Media