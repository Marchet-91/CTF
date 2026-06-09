import requests

URL = "http://store98.challs.cyberchallenge.it"

s = requests.Session()

def search(p, payload):
    print(requests.get(URL + "/search?"+ payload).text)

def users(p):
    print(p.)



search("c'or1=1UNIONselect")