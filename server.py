from flask import Flask, request

app = Flask(__name__)
auth_code = None  # Global variable to store the code

@app.route("/callback")
def callback():
    global auth_code
    auth_code = request.args.get("code")
    return "Authorization code received! You can close this tab now."

@app.route("/get_code")
def get_code():
    """Endpoint for main script to fetch the code"""
    global auth_code
    if auth_code:
        return auth_code
    return "", 204  # No content yet

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8888)
