import requests, urllib3

# ОТКЛЮЧАЕМ ПРЕДУПРЕЖДЕНИЯ В КОНСОЛИ
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get(Url: str):
    return requests.get(Url, verify = False, timeout = 2)