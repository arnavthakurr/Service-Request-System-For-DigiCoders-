import requests
import json

# Test the new /submit-request endpoint
url = "http://localhost:5000/submit-request"

# Test data
test_data = {
    "name": "Kairav",
    "email": "kairav@example.com",
    "mobile": "9876543210",
    "service": "PAN Card Apply",
    "message": "I need help with PAN card application"
}

print("Testing /submit-request endpoint with valid data...")
try:
    response = requests.post(url, json=test_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")

# Test with invalid data
print("\nTesting with invalid data (missing required fields)...")
invalid_data = {
    "name": "",
    "email": "invalid-email",
    "phone": "123",
    "service_type": "",
    "description": ""
}

try:
    response = requests.post(url, json=invalid_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")