from flask import Flask, request, jsonify, session
from flask_cors import CORS
import json
import os
import bcrypt
import uuid
from datetime import datetime, timedelta
import jwt

app = Flask(__name__)
app.secret_key = 'ghar_ka_guide_secret_key_2024'  # Change this in production
CORS(app, supports_credentials=True)

# JWT configuration
JWT_SECRET = 'ghar_ka_guide_jwt_secret_2024'  # Change this in production
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION = 24 * 60 * 60  # 24 hours

# File paths
USERS_FILE = 'users.json'
SESSIONS_FILE = 'sessions.json'

def load_users():
    """Load users from JSON file"""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {"users": [], "sessions": []}

def save_users(data):
    """Save users to JSON file"""
    with open(USERS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def hash_password(password):
    """Hash password using bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def verify_password(password, hashed):
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

def generate_jwt(user_id, email):
    """Generate JWT token"""
    payload = {
        'user_id': user_id,
        'email': email,
        'exp': datetime.utcnow() + timedelta(seconds=JWT_EXPIRATION),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_jwt(token):
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

@app.route('/api/auth/signup', methods=['POST'])
def signup():
    """User registration endpoint"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'phone', 'password']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'{field.capitalize()} is required'
                }), 400
        
        # Load existing users
        users_data = load_users()
        
        # Check if email already exists
        if any(user['email'] == data['email'] for user in users_data['users']):
            return jsonify({
                'success': False,
                'error': 'Email already registered'
            }), 409
        
        # Create new user
        new_user = {
            'id': str(uuid.uuid4()),
            'name': data['name'],
            'email': data['email'],
            'phone': data['phone'],
            'password': hash_password(data['password']).decode('utf-8'),
            'created_at': datetime.utcnow().isoformat(),
            'last_login': None,
            'profile': {
                'age': data.get('age', 25),
                'income': data.get('income', 500000),
                'risk_tolerance': data.get('risk_tolerance', 'moderate'),
                'investment_experience': data.get('investment_experience', 'beginner')
            }
        }
        
        # Add user to database
        users_data['users'].append(new_user)
        save_users(users_data)
        
        # Generate JWT token
        token = generate_jwt(new_user['id'], new_user['email'])
        
        return jsonify({
            'success': True,
            'message': 'Account created successfully',
            'user': {
                'id': new_user['id'],
                'name': new_user['name'],
                'email': new_user['email'],
                'phone': new_user['phone'],
                'profile': new_user['profile']
            },
            'token': token
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('email') or not data.get('password'):
            return jsonify({
                'success': False,
                'error': 'Email and password are required'
            }), 400
        
        # Load users
        users_data = load_users()
        
        # Find user by email
        user = None
        for u in users_data['users']:
            if u['email'] == data['email']:
                user = u
                break
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'Invalid email or password'
            }), 401
        
        # Verify password
        if not verify_password(data['password'], user['password']):
            return jsonify({
                'success': False,
                'error': 'Invalid email or password'
            }), 401
        
        # Update last login
        user['last_login'] = datetime.utcnow().isoformat()
        save_users(users_data)
        
        # Generate JWT token
        token = generate_jwt(user['id'], user['email'])
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'user': {
                'id': user['id'],
                'name': user['name'],
                'email': user['email'],
                'phone': user['phone'],
                'profile': user['profile']
            },
            'token': token
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/auth/verify', methods=['POST'])
def verify_token():
    """Verify JWT token endpoint"""
    try:
        data = request.get_json()
        token = data.get('token')
        
        if not token:
            return jsonify({
                'success': False,
                'error': 'Token is required'
            }), 400
        
        # Verify token
        payload = verify_jwt(token)
        if not payload:
            return jsonify({
                'success': False,
                'error': 'Invalid or expired token'
            }), 401
        
        # Load users to get user data
        users_data = load_users()
        user = None
        for u in users_data['users']:
            if u['id'] == payload['user_id']:
                user = u
                break
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        return jsonify({
            'success': True,
            'user': {
                'id': user['id'],
                'name': user['name'],
                'email': user['email'],
                'phone': user['phone'],
                'profile': user['profile']
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """User logout endpoint"""
    try:
        # In a real application, you might want to blacklist the token
        # For now, we'll just return success
        return jsonify({
            'success': True,
            'message': 'Logout successful'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/auth/profile', methods=['GET'])
def get_profile():
    """Get user profile endpoint"""
    try:
        # Get token from headers
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                'success': False,
                'error': 'Authorization header required'
            }), 401
        
        token = auth_header.split(' ')[1]
        
        # Verify token
        payload = verify_jwt(token)
        if not payload:
            return jsonify({
                'success': False,
                'error': 'Invalid or expired token'
            }), 401
        
        # Load users to get user data
        users_data = load_users()
        user = None
        for u in users_data['users']:
            if u['id'] == payload['user_id']:
                user = u
                break
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        return jsonify({
            'success': True,
            'user': {
                'id': user['id'],
                'name': user['name'],
                'email': user['email'],
                'phone': user['phone'],
                'profile': user['profile']
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/auth/profile', methods=['PUT'])
def update_profile():
    """Update user profile endpoint"""
    try:
        # Get token from headers
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                'success': False,
                'error': 'Authorization header required'
            }), 401
        
        token = auth_header.split(' ')[1]
        
        # Verify token
        payload = verify_jwt(token)
        if not payload:
            return jsonify({
                'success': False,
                'error': 'Invalid or expired token'
            }), 401
        
        data = request.get_json()
        
        # Load users
        users_data = load_users()
        
        # Find and update user
        user_updated = False
        for user in users_data['users']:
            if user['id'] == payload['user_id']:
                # Update allowed fields
                if 'name' in data:
                    user['name'] = data['name']
                if 'phone' in data:
                    user['phone'] = data['phone']
                if 'profile' in data:
                    user['profile'].update(data['profile'])
                
                user_updated = True
                break
        
        if not user_updated:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        # Save updated data
        save_users(users_data)
        
        return jsonify({
            'success': True,
            'message': 'Profile updated successfully',
            'user': {
                'id': user['id'],
                'name': user['name'],
                'email': user['email'],
                'phone': user['phone'],
                'profile': user['profile']
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("🔐 Starting Ghar Ka Guide Authentication API...")
    print("📊 Available endpoints:")
    print("   - POST /api/auth/signup - User registration")
    print("   - POST /api/auth/login - User login")
    print("   - POST /api/auth/verify - Verify JWT token")
    print("   - POST /api/auth/logout - User logout")
    print("   - GET  /api/auth/profile - Get user profile")
    print("   - PUT  /api/auth/profile - Update user profile")
    print("\n🌐 Server running on http://localhost:5001")
    print("💡 Use Ctrl+C to stop the server")
    
    app.run(debug=True, host='0.0.0.0', port=5001)

