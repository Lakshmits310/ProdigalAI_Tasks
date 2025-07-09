from flask import Blueprint, request, jsonify
from app.models import User
from app import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint("auth", __name__)

# ---------------- Signup ---------------- #
@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    if not all(k in data for k in ("name", "email", "password")):
        return jsonify({"error": "Name, email, and password are required"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"message": "Email already exists"}), 400

    user = User(
        name=data["name"],
        email=data["email"],
        role=data.get("role", "Viewer")  # Default to Viewer
    )
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201

# ---------------- Login ---------------- #
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data["email"]).first()

    if user and user.check_password(data["password"]):
        token = create_access_token(identity={
            "id": user.id,
            "email": user.email,
            "role": user.role
        })
        return jsonify({
            "token": token,
            "user": {
                "name": user.name,
                "email": user.email,
                "role": user.role
            }
        }), 200
    return jsonify({"message": "Invalid credentials"}), 401

# ---------------- Assign Role ---------------- #
@auth_bp.route("/assign-role", methods=["POST"])
@jwt_required()
def assign_role():
    current_user = get_jwt_identity()
    if current_user['role'] != 'Admin':
        return jsonify({"error": "Access denied. Only Admins can assign roles."}), 403

    data = request.get_json()
    user_email = data.get("email")
    new_role = data.get("role")

    if not user_email or not new_role:
        return jsonify({"error": "Email and role are required"}), 400

    user = User.query.filter_by(email=user_email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.role = new_role
    db.session.commit()

    return jsonify({"message": f"Role '{new_role}' assigned to {user_email}"}), 200
