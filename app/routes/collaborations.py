from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_socketio import emit

from app import socketio
from app.models import Collaboration, Task
from app.schemas import CollaborationSchema

bp = Blueprint("collaborations", __name__, url_prefix="/collaborations", description="Operations for collaborations")


@bp.route("/")
class CollaborationList(MethodView):
    @bp.arguments(CollaborationSchema)
    @bp.response(201, CollaborationSchema)
    def post(self, collaboration_data):
        collaboration = Collaboration(**collaboration_data)
        collaboration.save_to_db()

        task = Task.query.get(collaboration_data["task_id"])
        if not task:
            abort(404, message="Task not found.")

        emit("collaboration_added", {"task_id": task.id, "user_id": collaboration_data["user_id"]}, broadcast=True)

        return collaboration, 201


@socketio.on("connect")
def handle_connect():
    print("Client connected")


@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")
