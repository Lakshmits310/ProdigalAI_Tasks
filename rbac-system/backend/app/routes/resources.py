from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Resource, Department, GuestLink
from app.utils.decorators import role_required
import datetime

resource_bp = Blueprint("resource", __name__)

# ---------------- Create a Resource ---------------- #
@resource_bp.route("/<int:dept_id>/create", methods=["POST"])
@jwt_required()
@role_required(['Admin', 'Manager', 'Contributor'])
def create_resource(dept_id):
    data = request.get_json()
    current_user = get_jwt_identity()

    dept = Department.query.get(dept_id)
    if not dept:
        return jsonify({"error": "Department not found"}), 404

    res = Resource(
        title=data['title'],
        content=data.get('content', ''),
        department_id=dept_id,
        created_by=current_user['id']
    )
    db.session.add(res)
    db.session.commit()

    return jsonify({
        "message": "Resource created",
        "resource_id": res.id
    }), 201

# ---------------- Get Resources by Department ---------------- #
@resource_bp.route("/department/<int:dept_id>", methods=["GET"])
@jwt_required()
def get_resources(dept_id):
    res_list = Resource.query.filter_by(department_id=dept_id).all()
    return jsonify([{
        "id": res.id,
        "title": res.title,
        "content": res.content,
        "created_at": res.created_at
    } for res in res_list]), 200

# ---------------- Generate Guest Link ---------------- #
@resource_bp.route("/<int:resource_id>/share", methods=["POST"])
@jwt_required()
@role_required(['Admin', 'Manager'])
def generate_share_link(resource_id):
    data = request.get_json()
    permission = data.get("permission", "view")  # 'view' or 'edit'
    expires_in_days = data.get("expires_in", 1)

    guest_link = GuestLink(
        resource_id=resource_id,
        permission=permission,
        expires_at=datetime.datetime.utcnow() + datetime.timedelta(days=expires_in_days)
    )

    db.session.add(guest_link)
    db.session.commit()

    return jsonify({
        "message": "Guest link created",
        "guest_url": f"http://127.0.0.1:5000/api/guest/access/{guest_link.token}"
    }), 201
