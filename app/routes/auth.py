from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_jwt,
    jwt_required,
)
import logging

from app.models import User
from app.schemas import UserSchema, UserLoginResponseSchema, TokenRefreshResponseSchema
from blocklist import BLOCKLIST


bp = Blueprint("auth", __name__, description="Operations for user authentication")


@bp.route("/register")
class UserRegister(MethodView):
    @bp.arguments(UserSchema)
    @bp.response(201, description="User created successfully. You can now log in.")
    def post(self, user_data):
        if User.find_by_username(user_data["username"]):
            abort(409, message="A user with that username already exists.")
        try:
            user = User(**user_data)
            user.set_password(user_data["password"])  # Hash the password
            user.save_to_db()
        except Exception as e:
            logging.error(str(e))
            abort(500, message="An error occurred while processing your request")

        return {"message": "User created successfully. You can now log in."}, 201


@bp.route("/login")
class UserLogin(MethodView):
    @bp.arguments(UserSchema)
    @bp.response(200, UserLoginResponseSchema)
    def post(self, user_data):
        try:
            user = User.find_by_username(user_data["username"])

            if user and user.check_password(user_data["password"]):
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)
                return {"access_token": access_token, "refresh_token": refresh_token}, 200
        except Exception as e:
            logging.error(str(e))
            abort(500, message="An error occurred while processing your request")

        abort(401, message="Invalid credentials.")


@bp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    @bp.response(200, description="Successfully logged out.")
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out."}, 200


@bp.route("/user/<int:user_id>")
class User(MethodView):
    """
    This resource can be useful when testing our Flask app.
    We may not want to expose it to public users, but for the
    sake of testing.
    """

    @bp.response(200, UserSchema)
    def get(self, user_id):
        user = User.find_by_id(user_id)
        if not user:
            abort(404, message="User not found.")
        return user

    def delete(self, user_id):
        user = User.find_by_id(user_id)
        if not user:
            abort(404, message="User not found.")
        user.delete_from_db()
        return {"message": "User deleted."}, 200


@bp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    @bp.response(TokenRefreshResponseSchema, 200)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200
