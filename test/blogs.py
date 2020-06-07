import json
import requests
import os

AUTH = "http://127.0.0.1:8000/api/auth/"
REFRESH = f"{AUTH}refresh/"
BLOGS = "http://127.0.0.1:8000/api/blogs/"
IMG_PATH = os.path.join(os.getcwd(), "test.png")
HEADER = {"Content-Type": "application/json"}

GET_DETAILS = f"{BLOGS}1"

# GET Details for individual Blog Post
detail_req = requests.get(GET_DETAILS)
print(detail_req.text)

# GET List of all Blogs
list_req = requests.get(BLOGS)
print(list_req.status_code)

# POST New Blog
data = json.dumps({"content": "Some random content"})
post_response = requests.post(BLOGS, data=data, headers=HEADER)
print(post_response.text)


def perform_action(method='get', data={}, is_json=True):
    headers = {}
    if is_json:
        headers['content-type'] = 'application/json'
        data = json.dumps(data)
    r = requests.request(method, BLOGS, data=data, headers=headers)
    print(r.text)
    print(r.status_code)
    return r


perform_action(method='DELETE', data={'id': 13})
edited_data = {'id': 13, "content": "Edited Data", 'user': 1}
perform_action(method='PUT', data=edited_data)
perform_action(method='POST', data={"content": "New Data", 'user': 1})


def post_with_image(method='GET', data={}, is_json=True, img_path=None):
    data = json.dumps(data)
    if img_path is not None:
        with open(IMG_PATH, 'rb') as image:
            file_data = {'image': image}
            img_req = requests.request(
                method, BLOGS, data=data, files=file_data, headers=HEADER)
    else:
        img_req = requests.request(method, BLOGS, data=data)
    print(img_req.text)
    print(img_req.status_code)
    return img_req


payload = {'id': 23, 'user': 1, "content": "DataImage"}
post_with_image(method='post', data=payload, is_json=True)
