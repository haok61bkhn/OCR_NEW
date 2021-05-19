import requests

img_path="data/uyquyen.png"
values ={ "pattern_name": "giấy ủy nhiệm1", "keyword": "giấy ủy nhiệm; V/v bổ nhiệm", "type": "line", "image_sample": "http://10.9.3.50:8888/iPM/ImageCustomer/16192439553595584.jpg", "attribute": [ { "key_name": "1. nội dung ủy nhiệm", "start_c": "1. nội dung ủy nhiệm", "end_c": "2. bên ủy quyền", "type": "title", "num_of_appeer": -1 }, { "key_name": "người ủy nhiệm", "start_c": "ông", "end_c": "chức vụ", "type": "field", "num_of_appeer": -1 }, { "key_name": "chức vụ", "start_c": "-; chức vụ", "end_c": "2. bên ủy quyền", "type": "field", "num_of_appeer": -1 }, { "key_name": "2. bên ủy quyền", "start_c": "2. bên ủy quyền", "end_c": "-1", "type": "title", "num_of_appeer": -1 }, { "key_name": "người ủy nhiệm", "start_c": "ông", "end_c": "chức vụ", "type": "field", "num_of_appeer": -1 }, { "key_name": "chức vụ", "start_c": "-; chức vụ", "end_c": "-1", "type": "field", "num_of_appeer": -1 } ] }


files = {
   
    'image_file': open(img_path, 'rb'),
}

response = requests.post('http://0.0.0.0:1313/config/', files=files,json=values)
print(response.json())