import requests

url = "http://localhost:8000/run-task/"

while True:
    resp = requests.get(url)
    print(resp.status_code)
