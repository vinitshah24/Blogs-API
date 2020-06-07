import json
import requests
import os

AUTH = "http://127.0.0.1:8000/api/auth/"
REFRESH = f"{AUTH}refresh/"
BLOGS = "http://127.0.0.1:8000/api/blogs/"
IMG_PATH = os.path.join(os.getcwd(), "test.png")
HEADER = {"Content-Type": "application/json"}

# GET JWT TOKEN
data = {'username': 'admin', 'password': 'admin'}
req_token = requests.post(AUTH, data=json.dumps(data), headers=HEADER)
token = req_token.json()

if token is not None:
    print(token['token'])
    jwt_token = token['token']
    # REFRESH TOKEN USING EXISTING JWT TOKEN
    refresh_data = {'token': jwt_token}
    req_refresh = requests.post(
        REFRESH, data=json.dumps(refresh_data), headers=HEADER)
    if token is not None:
        new_token = req_refresh.json()
        print(new_token)
    else:
        print("REFRESH API Failed!")
else:
    print("TOKEN API Failed!")


