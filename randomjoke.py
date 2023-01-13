import requests
import json


url = "https://icanhazdadjoke.com/"

headers = {"Accept": "application/json"}


def get_joke():
    response = requests.get(url, headers=headers)
    raw_joke = json.loads(response.content)
    return raw_joke["joke"]
