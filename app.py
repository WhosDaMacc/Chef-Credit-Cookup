from flask import Flask, request, jsonify

app = Flask(__name__)
app.config['APP_NAME'] = "Chef Credit Cookup"

users = []

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    if any(user['email'] == email for user in users):
        return jsonify({"error": "Email already registered"}), 400
    users.append(data)
    return jsonify({"message": f"User {data.get('name')} signed up!"}), 201

@app.route('/notifications', methods=['GET'])
def notifications():
    return jsonify({"message": f"Updates coming soon from {app.config['APP_NAME']}!"})

if __name__ == '__main__':
    app.run(debug=True)