import requests
import json
import time


while True:
    response = requests.get("http://0.0.0.0:1111/")
    print(response.json())
    time.sleep(5)
