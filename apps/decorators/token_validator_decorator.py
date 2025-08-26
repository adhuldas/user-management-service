

from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import decode_token
from apps.database.models import TokenBlockListDb



def get_token_from_header(request):
    """
    Extracts the JWT access token from the Authorization header.

    Expected header format:
        Authorization: Bearer <token>
    """
    auth_header = request.headers.get("Authorization", None)
    if not auth_header:
        return None  # No header present

    parts = auth_header.split()

    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None  # Invalid format

    return parts[1]  # Return the token string

def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = get_token_from_header(request)
        payload = decode_token(token)
        jti = payload["jti"]

        if TokenBlockListDb().find_one({"jti": jti}):
            return jsonify(message="Token revoked"), 401
        
        return f(*args, **kwargs)
    return wrapper