#!/usr/bin/python3
# William Zhang
# import requests
import os
import json
import requests
from pprint import pprint

API_KEY="DkTKSYVEWJFfrZ2XoBKKxenb3qHN4jUn"
BASE_URL="https://dev.wzhang.me"

def main():
#    r = requests.get("https://dev.wzhang.me/api/topology/")
    data = {}
    with open("test.json", "r") as f:
        data = json.load(f)
    pprint(data)
    url = BASE_URL + "/api/receive/" + data["id"] + "/?key=" + API_KEY
    print(url)
    r = requests.post(url, data=json.dumps(data))
    print(r.text)

    return


if __name__ == '__main__':
    main()
