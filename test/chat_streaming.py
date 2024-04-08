import json

import requests


url = "http://localhost:8000/chat/message-streaming"
message = "Hello, What is mamba architecture?"
data = {"content": message}

headers = {"Content-type": "application/json"}

with requests.post(url, data=json.dumps(data), headers=headers, stream=True) as r:
    for chunk in r.iter_content(1024):
        print(chunk)
