from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.config['APP_NAME'] = "Chef Credit Cookup"

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.email}>'

# Create tables (run once)
with app.app_context():
    db.create_all()

# Routes
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    name = data.get('name')
    email = data.get('email')

    # Check for existing email
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400

    # Create new user
    new_user = User(name=name, email=email)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": f"User {name} successfully signed up for {app.config['APP_NAME']}",
        "user_id": new_user.id
    }), 201

@app.route('/notifications', methods=['GET'])
def notifications():
    return jsonify({
        "message": f"Stay tuned for updates on your credit repair status with {app.config['APP_NAME']}!"
    })

if __name__ == '__main__':
    app.run(debug=True)