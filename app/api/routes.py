from flask import request, jsonify, session
from . import api_bp
from ..extensions import db
from ..models.user import User
from werkzeug.security import generate_password_hash, check_password_hash

# POST /api/register
# {"email": "user@example.com", "password": "secret", "city": "Moscow"}
@api_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    city = data.get('city')
    
    if not email or not password:
        return jsonify({'error': 'email and password required'}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'user already exists'}), 400
    
    user = User(email=email, password_hash=generate_password_hash(password), city=city)
    db.session.add(user)
    db.session.commit()
    
    return jsonify(user.to_dict()), 201


# POST /api/login
# {"email": "user@example.com", "password": "secret"}
@api_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'email and password required'}), 400
    
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'error': 'invalid credentials'}), 401

    session['user_id'] = user.id
    return jsonify({'token': str(user.id), 'user': user.to_dict()}), 200


def get_current_user():
    uid = session.get('user_id')
    if not uid:
        return None
    return User.query.get(int(uid))


# GET /api/me
@api_bp.route('/me', methods=['GET'])
def me():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'unauthorized'}), 401
    
    return jsonify(user.to_dict()), 200
