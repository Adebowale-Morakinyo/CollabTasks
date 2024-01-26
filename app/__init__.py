from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
import logging

from blocklist import BLOCKLIST
from .models import db
from .socketio.events import socketio

migrate = Migrate()
cors = CORS()


def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(f"config.{config_name.capitalize()}Config")

    # Configure logging
    logging.basicConfig(filename='error.log', level=logging.ERROR)

    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app, cors_allowed_origins="http://127.0.0.1:5000")

    api = Api(app)
    jwt = JWTManager(app)

    # @jwt.additional_claims_loader
    # def add_claims_to_jwt(identity):
    #     # TODO: Read from a config file instead of hard-coding
    #     if identity == 1:
    #         return {"is_admin": True}
    #     return {"is_admin": False}

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required",
                }
            ),
            401,
        )

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )

    from .routes import auth, tasks, collaborations, preferences
    api.register_blueprint(auth.bp)
    api.register_blueprint(tasks.bp)
    api.register_blueprint(collaborations.bp)
    api.register_blueprint(preferences.bp)

    with app.app_context():
        db.create_all()

    return app
