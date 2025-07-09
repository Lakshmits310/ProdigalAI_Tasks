from flask import Blueprint, jsonify
from app.models import GuestLink, Resource
from datetime import datetime
from app import db

guest_bp = Blueprint('guest', __name__)

@guest_bp.route("/access/<string:token>", methods=["GET"])
def access_resource(token):
    link = GuestLink.query.filter_by(token=token).first()
    if not link:
        return jsonify({"error": "Invalid token"}), 404

    if link.expires_at and datetime.utcnow() > link.expires_at:
        return jsonify({"error": "Link expired"}), 403

    resource = Resource.query.get(link.resource_id)
    if not resource:
        return jsonify({"error": "Resource not found"}), 404

    return jsonify({
        "resource_id": resource.id,
        "title": resource.title,
        "content": resource.content,
        "permission": link.permission
    }), 200

