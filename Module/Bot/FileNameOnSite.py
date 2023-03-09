import requests, bs4

import Module.Tool.Requests as Requests

cookies = {
}

headers = {
}

params = {
}


def getSiteState(Url: str):
    try:    return Requests.get(Url).status_code == 200
    except: return False



def getFileNameOnSite(Date: str):
    if (getSiteState("")):

        Response = requests.get("", params = params, cookies = cookies, headers = headers)
        Site = bs4.BeautifulSoup(Response.text, "lxml").html

        for Tag in Site.find_all("a"):
            if (Date in str(Tag)):
                return Tag.text.replace("Новый", "")

        return False