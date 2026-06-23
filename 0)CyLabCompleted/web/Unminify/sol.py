from bs4 import BeautifulSoup
from requests import * 

URL = "http://titan.picoctf.net:62931/"

def getFlag():
    s = BeautifulSoup(get(URL).text, "html.parser")
    p = s.find_all("p")
    for test in p:
        if test.get_attribute_list("class")[0] != "picoctf{}":
            return test.get_attribute_list("class")[0]

print(getFlag())