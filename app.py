from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.config['APP_NAME'] = "Chef Credit Cookup"

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Database and Migrations
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

# Create database tables (first-time setup)
with app.app_context():
    db.create_all()

# Routes
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        return jsonify({"error": "Name and email are required"}), 400

    # Check for existing user
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 409

    try:
        new_user = User(name=name, email=email)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({
            "message": f"User {name} successfully signed up!",
            "user_id": new_user.id,
            "created_at": new_user.created_at.isoformat()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/notifications', methods=['GET'])
def notifications():
    return jsonify({
        "message": f"Stay tuned for updates from {app.config['APP_NAME']}!",
        "total_users": User.query.count()
    })

if __name__ == '__main__':
    app.run(debug=True)
    from flask import Flask
from datetime import datetime

app = Flask(__name__)

# Configuration that works without a domain
app.config.update({
    'APP_NAME': "Chef Credit Cookup",
    'BASE_URL': 'http://localhost:5000',  # Will auto-update to real domain later
    'CURRENT_YEAR': datetime.now().year
})

@app.context_processor
def inject_global_vars():
    """Makes these available in all templates"""
    return {
        'current_year': app.config['CURRENT_YEAR'],
        'base_url': app.config['BASE_URL']
    }