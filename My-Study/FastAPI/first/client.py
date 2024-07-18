import requests
import json

response = requests.get("http://127.0.0.1:8000/calculator/sum?first=123&second=22")
answer = json.loads(response.content)
print(answer['result'])