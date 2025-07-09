from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")  # Your config class (ensure it's defined in config.py)

    # Initialize extensions with app
    CORS(app)
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # ---------------- Register Blueprints ---------------- #
    from app.routes.auth import auth_bp
    from app.routes.orgs import orgs_bp
    from app.routes.resources import resource_bp
    from app.routes.guest import guest_bp  # Optional — if implemented

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(orgs_bp, url_prefix="/api/orgs")
    app.register_blueprint(resource_bp, url_prefix="/api/resources")
    app.register_blueprint(guest_bp, url_prefix="/api/guest")  # Comment if not yet created

    return app

