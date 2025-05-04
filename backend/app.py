from flask import Flask, request, jsonify

app = Flask(__name__)

# Hardcoded credentials (for demo only - upgrade to database later)
VALID_CREDENTIALS = {
    "syida": "8888"
}

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username in VALID_CREDENTIALS and VALID_CREDENTIALS[username] == password:
        return jsonify({"success": True, "message": "Welcome Syida!"})
    else:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

if __name__ == '__main__':
    app.run()
