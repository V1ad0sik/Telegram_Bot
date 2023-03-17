import wget

from Module.Bot import FileNameOnSite
from Module.Tool import (
    Requests,
    Time,
    DocxParser as Docx
)


def getSiteState(Url: str):
    try:    return Requests.get(Url).status_code == 200
    except: return False


def downloadFile(Url: str):
    try:    return wget.download(Url, "Files", bar = None)
    except: return False


def getFilePath(Date: str):
    Path = Files.fileIsDownloaded("Files", Date)

    if (not Path):
        FileName = FileNameOnSite.getFileNameOnSite(Date)

        if (FileName):
            return downloadFile(f"")

        return False

    return Path


def getReplace(Day: int):
    Date = Time.getDateFromWeekdayStrReplace(Day)
    Path = getFilePath(Date)

    if (Path):
        Document = Docx.openDocument(f"Files/{Path}" if "Files" not in Path else Path)

        if (Docx.groupInRows(Document = Document, MyGroup = "")):
            return Docx.parceReplace(Document = Document, MyGroup = "")

        else:
            return list()

    else:
        return list()