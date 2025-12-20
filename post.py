import requests

# The API endpoint URL
URL = "http://localhost:5000/api/signup"

# The teacher JSON data (as a Python dictionary)
teacher_data = {
    "username": "Thierry Nguyen",
    "email": "thierryminht4@gmail.com",
    "password": "SecurePassword123",
    "userType": "teacher",
    "employeeId": "676767",
}

try:
    # Use the 'json' parameter. The requests library automatically
    # sets the 'Content-Type: application/json' header for you.
    response = requests.post(URL, json=teacher_data)

    # Print the results
    print(f"Status Code: {response.status_code}")
    print("Response JSON:")
    print(response.json())

except requests.exceptions.ConnectionError as e:
    print(f"Error: Could not connect to the Flask server. Is app.py running? {e}")