from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Organization, Department
from app import db
from app.utils.decorators import role_required

orgs_bp = Blueprint('orgs_bp', __name__)

# ---------------- Create Organization ---------------- #
@orgs_bp.route("/create", methods=["POST"])
@jwt_required()
@role_required(['Admin'])
def create_organization():
    data = request.get_json()
    current_user = get_jwt_identity()

    new_org = Organization(
        name=data['name'],
        created_by=current_user['id']
    )
    db.session.add(new_org)
    db.session.commit()

    return jsonify({"message": "Organization created"}), 201

# ---------------- Get All Organizations ---------------- #
@orgs_bp.route("/", methods=["GET"])
@jwt_required()
def get_organizations():
    orgs = Organization.query.all()
    org_list = [{"id": org.id, "name": org.name} for org in orgs]
    return jsonify(org_list), 200

# ---------------- Create Department ---------------- #
@orgs_bp.route("/<int:org_id>/departments", methods=["POST"])
@jwt_required()
@role_required(['Admin', 'Manager'])
def create_department(org_id):
    data = request.get_json()
    current_user = get_jwt_identity()

    org = Organization.query.get(org_id)
    if not org:
        return jsonify({"error": "Organization not found"}), 404

    dept = Department(
        name=data['name'],
        org_id=org_id,
        created_by=current_user['id']
    )
    db.session.add(dept)
    db.session.commit()

    return jsonify({"message": "Department created"}), 201

# ---------------- Get Departments by Organization ---------------- #
@orgs_bp.route("/<int:org_id>/departments", methods=["GET"])
@jwt_required()
def get_departments(org_id):
    org = Organization.query.get(org_id)
    if not org:
        return jsonify({"error": "Organization not found"}), 404

    departments = Department.query.filter_by(org_id=org_id).all()
    dept_list = [{
        "id": dept.id,
        "name": dept.name,
        "created_by": dept.created_by
    } for dept in departments]

    return jsonify(dept_list), 200
