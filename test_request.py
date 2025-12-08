import requests

url = "http://127.0.0.1:5000/api/search"
data = {"query": "nejlepsi kava"}

response = requests.post(url, json=data)
print(response.json())