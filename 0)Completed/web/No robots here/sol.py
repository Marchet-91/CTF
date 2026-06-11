from requests import *
from bs4 import BeautifulSoup

URL = "http://no-robots.challs.olicyber.it"

s = get(URL + "/robots.txt").text.split(":")[-1][1:]
s = BeautifulSoup(get(URL + s).text, "html.parser")

h = s.find("h2")
print(h.contents[0])