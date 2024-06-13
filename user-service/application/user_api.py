from flask import Blueprint, make_response, request, jsonify
from .models import User
from . import db, login_manager
from flask_login import current_user, login_user, logout_user, login_required
from passlib.hash import pbkdf2_sha256
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

user_api_blueprint = Blueprint('user_api', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@login_manager.request_loader
def load_user_from_request(request):
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Basic ', '', 1)
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return user
    return None

@user_api_blueprint.route('/allUsers', methods=['GET'])
def get_users():
    data = []
    for row in User.query.all():
        data.append(row.to_json())

    response = jsonify(data)
    return response

@user_api_blueprint.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']
    username = data['username']

    password = pbkdf2_sha256.hash((str(data['password'])))

    user = User()
    user.email = email
    user.first_name = first_name
    user.last_name = last_name
    user.password = password
    user.username = username,
    user.api_key = pbkdf2_sha256.hash(username + str(datetime.utcnow))
    user.authenticated = True

    db.session.add(user)
    db.session.commit()

    response = jsonify({'message': 'User added', 'result': user.to_json()}),200

    return response


@user_api_blueprint.route('/login', methods=['POST'])
def post_login():
    data = request.get_json()
    username = data['username']
    logger.info('Username: %s'+username)

    user = User.query.filter_by(username=username).first()
    if user:
        if pbkdf2_sha256.verify(str(data['password']), user.password):
            user.encode_api_key()
            db.session.commit()
            login_user(user)

            return make_response(jsonify({'message': 'Logged in', 'api_key': user.api_key}),200)

    return make_response(jsonify({'message': 'Not logged in'}), 401)


@user_api_blueprint.route('/logout', methods=['POST'])
@login_required
def post_logout():
    if current_user.is_authenticated:
        logout_user()
        return make_response(jsonify({'message': 'You are logged out'}))
    return make_response(jsonify({'message': 'You are not logged in'}))

@login_required
@user_api_blueprint.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({
            'user':user.to_json()
        }), 200
    return jsonify({'message': 'User not found'}), 404


@user_api_blueprint.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = User.query.get(user_id)
    if user:
        user.username = data['username']
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.email = data['email']
        db.session.commit()
        return jsonify({'message': 'User updated successfully'}), 200
    return jsonify({'message': 'User not found'}), 404


@user_api_blueprint.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    return jsonify({'message': 'User not found'}), 404
