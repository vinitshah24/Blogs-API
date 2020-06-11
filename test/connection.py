import json
import requests
import os

AUTH = "http://127.0.0.1:8000/api/auth/"
REFRESH = f"{AUTH}jwt/refresh/"
BLOGS = "http://127.0.0.1:8000/api/blogs/"
IMG_PATH = os.path.join(os.getcwd(), "test.png")
HEADER = {"Content-Type": "application/json"}


print('----------GET JWT Token----------')
data = {'username': 'admin', 'password': 'admin'}
req = requests.post(AUTH, data=json.dumps(data), headers=HEADER)
print(req.status_code)

reqJSON = req.json()
API_token = reqJSON['token']


print('----------POST data----------')
JWT_HEADER = {
    "Content-Type": "application/json",
    "Authorization": "JWT " + API_token
}
postData = {
    "content": "Data from Script",
}
req = requests.post(
    BLOGS,
    headers=JWT_HEADER,
    data=json.dumps(postData)
)
print(req.status_code)

postedJSON = req.json()
ID = postedJSON['id']
CONTENT = postedJSON['content']

print('----------DELETE data----------')

BLOG_ID = f"{BLOGS}{ID}"
deleteData = {
    'content': CONTENT
}
req = requests.delete(
    BLOG_ID,
    headers=JWT_HEADER,
    data=json.dumps(deleteData)
)
print(req.status_code)


# print('----------POST data with image----------')
# JWT_ONLY_HEADER = {
#     "Authorization": "JWT " + API_token
# }
# postwithImageData = {
#     "content": "Data & Image from Script",
# }
# with open(IMG_PATH, 'rb') as image:
#     file_data = {'image': image}

# req = requests.post(
#     BLOGS,
#     headers=JWT_ONLY_HEADER,
#     data=postwithImageData,
#     files=file_data
# )
# postedImgDataJSON = req.json()
# print(postedImgDataJSON)


print('----------REFRESH TOKEN----------')
body = {
    "token": str(API_token)
}
req = requests.post(
    REFRESH,
    headers=HEADER,
    data=json.dumps(body)
)
refTokenJSON = req.json()
print(req.status_code)
#print(refTokenJSON)

