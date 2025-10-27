import requests

URL = "http://127.0.0.1:5000/chat"

while True:
    msg = input("You: ")
    if msg.lower() in ["quit", "exit", "bye"]:
        print("ChinguBot: Goodbye👋! Come back soon💖")
        break

    response = requests.post(URL, json={"message": msg})
    if response.status_code == 200:
        print("ChinguBot:", response.json().get("reply"))
    else:
        print("Error:", response.status_code)
