from requests import * 

URL = "http://headache.challs.olicyber.it"

print(get(URL).headers['Flagls'])