import requests

# Base URL
base_url = "http://localhost:5000"

# Start a session to maintain cookies
session = requests.Session()

# First, login to get authenticated
login_data = {
    'username': 'admin',
    'password': 'admin123'
}

print("Logging in...")
login_response = session.post(f"{base_url}/admin/login", data=login_data)
print(f"Login Status: {login_response.status_code}")

# Now test the GET /requests endpoint
print("\nTesting GET /requests endpoint...")
try:
    response = session.get(f"{base_url}/requests")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Success: {data['success']}")
        print(f"Total requests: {data['total']}")
        if data['requests']:
            print("Sample request:")
            print(data['requests'][0])
        else:
            print("No requests found")
    else:
        print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")

# Test accessing admin.html
print("\nTesting admin.html page...")
try:
    response = session.get(f"{base_url}/admin.html")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("admin.html loaded successfully")
    else:
        print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")