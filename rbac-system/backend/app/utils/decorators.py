from flask_jwt_extended import get_jwt_identity
from functools import wraps
from flask import jsonify

def role_required(required_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = get_jwt_identity()
            if user['role'] not in required_roles:
                return jsonify({"error": "Access denied"}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator
