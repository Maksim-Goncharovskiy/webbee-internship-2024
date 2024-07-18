import requests
import json

response = requests.get("http://127.0.0.1:8001/admin/users")
print(json.loads(response.content))