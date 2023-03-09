import os, re


def getFiles(Folder: str):
    FileList = list()

    for Root, Dirs, Files in os.walk(Folder):  
        for File in Files:
            FileList.append(os.path.join(Root, File))

    return FileList


def getFolders(Folder: str):
    FileList = list()

    for Root, Dirs, Files in os.walk(Folder):  
        for Dir in Dirs:
            FileList.append(Dir)

    return FileList


def getAbsPath(Path, MyFile):
    for Root, Dirs, Files in os.walk(Path):  
        for File in Files:
            if (File == MyFile):
                return os.path.join(Root, File)

    return False


def fileIsDownloaded(Path, Name):
    Files = os.listdir(Path)

    for File in Files:
        if (Name in File): return File

    return False


def getFileList(Path):
    for Root, Dirs, Files in os.walk(Path):
        Tree = {Dir: getFileList(os.path.join(Root, Dir)) for Dir in Dirs}
        Tree.update({File: getFileSize(os.path.join(Root, File)) for File in Files})

        return Tree


def getAllFiles(Folder: str):
    return os.listdir(Folder)


def sortByName(Folders):
    Folders.sort(key = lambda s: len(s), reverse = True)
    return Folders


def sortFiles(Array):
    Folders = []
    Files   = []

    for Path in Array:
        if (os.path.splitext(Path)[1]):
            Files.append(Path)

        else:
            Folders.append(Path)

    Folders.sort(key = lambda File: int(re.sub("\D", "1", File)))

    Files.sort(key = lambda File: int(re.sub("\D", "1", File)))
    Files.sort(key = lambda File: os.path.splitext(File)[1])

    return Folders +  Files


#print(sortFiles(["Практическая 2", "Практическая 3", "Практическая 5", "Практическая 1",
#                 "Практическая 4", "Задания.docx", "Варианты.docx", "Данные.txt", "Текст.docx", "Практические по PHP", 
#                 "1.pptx", "3.pptx", "8.pptx", "2.pptx"
#                 ]))


#def sortFiles(FileList):
#    return sorted(FileList, key = lambda x: os.path.splitext(x)[1])


def getFileSize(Path: str):
    return int(round(os.path.getsize(Path) / (1024 ** 2), 0))


def getFileName(Path: str):
    return os.path.basename(Path)


def showFiles(Array: dict or list):
    return "\n".join(Array)


def isFile(Path):
    return os.path.isfile(Path)