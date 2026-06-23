from bs4 import BeautifulSoup
from base64 import b64decode
from requests import * 

URL = "http://titan.picoctf.net:65126/about.html"

def getFlag():
    s = BeautifulSoup(get(URL).text, "html.parser")
    ct =s.find("section").get_attribute_list("notify_true")[0]
    return b64decode(ct).decode()

print(getFlag())