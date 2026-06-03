import requests
import base64

URL = "http://localhost:3000"

s = requests.Session()

time = 0
for i in range(5):
    time = time + 1 + 24 * 60 * 60 * 1000
    body = {"timestamp": time}
    resp = s.post(URL, data=body)
    time = time + 1 + 24 * 60 * 60 * 1000

print(resp.content)
