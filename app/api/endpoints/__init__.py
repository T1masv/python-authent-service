from datetime import datetime, timezone
from datetime import timedelta
from functools import wraps

import jwt
from flask import request, jsonify

from app.dependencies import get_db

SECRET_KEY = "123123"


class User:
    def __init__(self, token, id, role):
        self.token = token
        self.id = id
        self.role = role


def generate_token(user):
    """
    Generate encoded token
    """
    acc_payload = {
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'user_id': str(user["_id"]),
        "role": user['role']
    }

    access_token = jwt.encode(acc_payload, SECRET_KEY, algorithm='HS256')

    return access_token


def decode_auth_token(auth_token):
    """
    Decodes the auth token
    """
    try:
        payload = jwt.decode(auth_token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'


def is_token_expired(token):
    """
    Checks if a JWT token has expired.

    Args:
    token (str): JWT token string.

    Returns:
    bool: True if the token has expired, False otherwise.
    """
    try:
        # Decode the token using the same secret key and algorithm used to encode
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        # Check if the token expiration time is less than the current UTC time
        if payload['exp'] < datetime.now(tz=timezone.utc).timestamp():
            return True  # Token has expired
        return False  # Token is still valid
    except jwt.ExpiredSignatureError:
        # This exception is raised when the token's expiration time is past
        return True
    except jwt.InvalidTokenError:
        # This includes various other errors such as missing fields or bad formatting
        return True


def get_user_info(token):
    user_info = decode_auth_token(token)
    return user_info


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        db = get_db()
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Authorization token is missing!'}), 403

        try:
            # Optional: Remove 'Bearer ' prefix if it exists
            if token.startswith('Bearer '):
                token = token[7:]

            if db.sessions.find_one({"token" : token}) is None:
                return jsonify({'message': 'Token expired'}), 401


            # Decode token
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])


            # Check for expiration explicitly if needed
            if payload['exp'] < datetime.now(tz=timezone.utc).timestamp():
                return jsonify({'message': 'Token has expired. Please log in again.'}), 401

            # You can add 'current_user' to kwargs if you want to pass user details to the route

            current_user = User(token, payload['user_id'], payload['role'])
            kwargs['current_user'] = current_user


        except jwt.ExpiredSignatureError:
            db = get_db()
            db.sessions.delete_one({"token":token})
            return jsonify({'message': 'Token has expired. Please log in again.'}), 401
        except (jwt.InvalidTokenError, Exception) as e:
            return jsonify({'message': 'Invalid token. Please log in again.', 'error': str(e)}), 401

        return f(*args, **kwargs)

    return decorated_function
