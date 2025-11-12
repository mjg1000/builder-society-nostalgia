
import requests
import base64
import webbrowser
import time 

client_id = "84cab4d0435646a582d44a829ae1a548"
client_secret = "dbc27f39d3ce46a78207cd33cd8db099"
redirect_uri = "http://127.0.0.1:8888/callback"
scope = "user-modify-playback-state user-read-playback-state streaming"


auth_str = f"{client_id}:{client_secret}"
b64_auth_str = base64.b64encode(auth_str.encode()).decode()

token_url = "https://accounts.spotify.com/api/token"

auth_url = (
    f"https://accounts.spotify.com/authorize?client_id={client_id}"
    f"&response_type=code&redirect_uri={redirect_uri}&scope={scope}"
)
# threading.Thread(target=lambda: app.run(host="127.0.0.1", port=8888)).start()

webbrowser.open(auth_url)
auth_code = None
while auth_code is None:
    try:
        r = requests.get("http://127.0.0.1:8888/get_code")
        if r.status_code == 200 and r.text:
            auth_code = r.text
    except requests.ConnectionError:
        pass
    time.sleep(0.5)
print(auth_code)
token_url = "https://accounts.spotify.com/api/token"
data = {
    "grant_type": "authorization_code",
    "code": auth_code,
    "redirect_uri": redirect_uri,
    "client_id": client_id,
    "client_secret": client_secret
}

response = requests.post(token_url, data=data)
tokens = response.json()
print(tokens)


ACCESS_TOKEN = tokens['access_token']

# Get the list of devices
response = requests.get(
    "https://api.spotify.com/v1/me/player/devices",
    headers={"Authorization": f"Bearer {ACCESS_TOKEN}"}
)

devices = response.json()["devices"]
device = devices[0]

track_uri = "spotify:track:4uLU6hMCjMI75M1A2tKUQC"  # replace with your track


# Optional: specify a device ID if you have multiple active devices
# data["device_id"] = "YOUR_DEVICE_ID"

data = {
    "uris": [track_uri],  # you can provide multiple URIs to play a playlist
    "devivce_id": device
}
response = requests.put(
    "https://api.spotify.com/v1/me/player/play",
    headers={
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    },
    json=data
)

if response.status_code == 204:
    print("Playback started!")
else:
    print("Error:", response.status_code, response.text)



# headers = {"Authorization": f"Basic {b64_auth_str}"}
# data = {"grant_type": "client_credentials"}

# response = requests.post(token_url, headers=headers, data=data)
# print(response.json())
