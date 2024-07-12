import requests

URL = 'https://api.telegram.org/bot7335489186:AAGvytPLouKdRyPMkd-ew7Or-SJq73gumsI/getMe'


def getOwner():
    res = requests.get(URL)
    if res.status_code == 200:
        return res.json()
    else:
        return None