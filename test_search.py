import urllib.request
import urllib.error

try:
    with urllib.request.urlopen("http://127.0.0.1:8000/search?q=test") as response:
        print(response.status)
        print(response.read().decode())
except urllib.error.HTTPError as e:
    print(e.code)
    print(e.read().decode())
