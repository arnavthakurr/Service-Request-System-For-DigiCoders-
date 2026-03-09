import requests
import json

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

# Submit a test request
test_request = {
    "name": "Test User",
    "email": "test@example.com",
    "phone": "9876543210",
    "service_type": "PAN Card Apply",
    "description": "Test request for deletion"
}

print("\nSubmitting test request...")
submit_response = session.post(f"{base_url}/submit-request", json=test_request)
print(f"Submit Status: {submit_response.status_code}")
if submit_response.status_code == 201:
    submit_data = submit_response.json()
    request_id = submit_data.get('request_id')
    print(f"Created request with ID: {request_id}")

    # Now test the GET /requests endpoint
    print("\nFetching requests...")
    get_response = session.get(f"{base_url}/requests")
    print(f"GET Status: {get_response.status_code}")
    if get_response.status_code == 200:
        get_data = get_response.json()
        print(f"Total requests: {get_data['total']}")

        # Now test delete
        print(f"\nDeleting request {request_id}...")
        delete_response = session.delete(f"{base_url}/api/requests/{request_id}")
        print(f"Delete Status: {delete_response.status_code}")
        if delete_response.status_code == 200:
            delete_data = delete_response.json()
            print(f"Delete response: {delete_data}")

            # Verify deletion by fetching requests again
            print("\nVerifying deletion...")
            get_response2 = session.get(f"{base_url}/requests")
            get_data2 = get_response2.json()
            print(f"Total requests after deletion: {get_data2['total']}")
        else:
            print(f"Delete failed: {delete_response.text}")
    else:
        print(f"GET failed: {get_response.text}")
else:
    print(f"Submit failed: {submit_response.text}")