from datetime import datetime, timedelta, timezone
import jwt

SECRET_KEY = "123123"


def generate_token(user_id):
    """
    Generate encoded token
    """
    acc_payload = {
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'user_id': str(user_id)
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