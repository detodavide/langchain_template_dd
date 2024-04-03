import requests

# Define the URL
url = "http://localhost:8000/users/create"

# Define the payload (data to be sent in the POST request)
payload = {
    "username": "exampldddeeee_user",
    "password": "example_password",
    "randomthings": "sss",
}

# Make the POST request
response = requests.post(url, json=payload)

# Print the response status code and content
print("Response Status Code:", response.status_code)
print("Response Content:", response.content.decode())
