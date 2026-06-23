from requests import * 
from urllib.parse import quote,unquote
from base64 import b64decode

URL = "http://verbal-sleep.picoctf.net:64909"

def login(s):
    data = {"username": "ciao", "password": "ciao"}
    s.post(URL + "/login.php", data=data)
    return s

s = Session()

s = login(s)
print(b64decode(unquote(s.cookies["secret_recipe"])).decode())
