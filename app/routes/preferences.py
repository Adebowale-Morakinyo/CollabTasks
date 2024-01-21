from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import UserPreferences
from app.schemas import UserPreferencesSchema


bp = Blueprint("preferences", "preferences", url_prefix="/preferences")


@bp.route("/")
class UserPreferencesView(MethodView):
    @jwt_required()
    @bp.arguments(UserPreferencesSchema)
    @bp.response(200, description="User preferences updated successfully")
    @bp.doc(description="""
    Endpoint that allows users to set their preferences for different factors. 
    A practical way to gather testing data.
    """)
    def post(self, user_preferences_data):
        user_id = get_jwt_identity()

        # Validate and save user preferences
        user_preferences = UserPreferences.query.filter_by(user_id=user_id).first()
        if user_preferences:
            user_preferences.update(user_preferences_data)
        else:
            user_preferences = UserPreferences(user_id=user_id, **user_preferences_data)
            user_preferences.save_to_db()

        return {"message": "User preferences updated successfully"}, 200
