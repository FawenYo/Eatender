import requests

# Login
data = {"id": "10524966", "name": "test", "password": ""}
response = requests.post("https://www.when2meet.com/ProcessLogin.php", data=data)
print(response.text)