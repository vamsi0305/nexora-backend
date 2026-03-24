import urllib.request
import urllib.error
import json

base_url = "http://127.0.0.1:8000"

def test_register():
    data = json.dumps({
        "email": "testuser2@example.com",
        "password": "Password123!",
        "full_name": "Test User 2",
        "phone_number": "8888888888"
    }).encode('utf-8')
    req = urllib.request.Request(f"{base_url}/auth/register", data=data, headers={"Content-Type": "application/json"})
    try:
        res = urllib.request.urlopen(req)
        print("Register:", res.status)
        return json.loads(res.read().decode())
    except urllib.error.HTTPError as e:
        print("Register Error:", e.code, e.read().decode())
        return None

def test_login():
    data = json.dumps({
        "email": "testuser2@example.com",
        "password": "Password123!"
    }).encode('utf-8')
    req = urllib.request.Request(f"{base_url}/auth/login", data=data, headers={"Content-Type": "application/json"})
    try:
        res = urllib.request.urlopen(req)
        print("Login:", res.status)
        return json.loads(res.read().decode())
    except urllib.error.HTTPError as e:
        print("Login Error:", e.code, e.read().decode())
        return None

print("Starting E2E Auth Test...")
reg_res = test_register()
log_res = test_login()
if log_res and "access_token" in log_res:
    print("Success! JWT Token received:", log_res["access_token"][:15] + "...")
else:
    print("Failed to get JWT token.")
