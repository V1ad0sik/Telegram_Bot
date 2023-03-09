import sqlite3


def readInfo(Path: str, Request: str):
    with sqlite3.connect(Path) as Base:
        Method = Base.cursor()

        try:                        Method.execute(Request)
        except Exception as Except: print(f"[SQL]> {Except}")

        return Method.fetchall()


def writeInfo(Path: str, Request: str):
    with sqlite3.connect(Path) as Base:
        Method = Base.cursor()
        Method.execute(Request)