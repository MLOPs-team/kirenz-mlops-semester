import requests

r = requests.get("http://localhost:5432")
print(r.json())