from requests import *
from bs4 import BeautifulSoup, Comment
# import cssutils

def iscomment(elem):
   return isinstance(elem, Comment)

URL = "http://vuoto.challs.olicyber.it/"

soup = BeautifulSoup(get(URL).text, "html.parser")

comments = soup.find_all(string=iscomment)
flag = comments[0].split("\"")[-2]

css = soup.find_all("link")[0].attrs['href']
flag += get(URL + css).text.split("\n")[0].split("\"")[-2]

js = soup.find_all("script")[0].attrs['src']
flag += get(URL + js).text.split("\"")[-2]

# print(get(URL).text)

print(flag)