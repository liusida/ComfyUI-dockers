import requests

# Server endpoint URL
url = "http://118.180.21.248:56789/set_maximum_caching"

# JSON data to enable maximum caching
payload = {
    "use_maximum_caching": True  # Set to `False` if you want to disable it
}

# Bearer token
token = "$2b$12$VOBzQhf8qjUWmG6LbpirteNRwsbBWJ3YAnWx13wpo4vQSbBga2R02"

# Headers with the Bearer token
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Send a POST request with the JSON payload and headers
response = requests.post(url, json=payload, headers=headers)

# Check for a successful response
if response.status_code == 200:
    print("Successfully set maximum caching.")
else:
    print(f"Failed to set maximum caching. Status code: {response.status_code}")
    print(f"Response text: {response.text}")
