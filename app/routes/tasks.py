from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models import Task
from app.schemas import TaskSchema
from app.algorithms import prioritize_tasks

bp = Blueprint("tasks", __name__, url_prefix="/tasks", description="Operations for tasks")


@bp.route("/")
class TaskList(MethodView):
    @bp.response(200, TaskSchema(many=True))
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        tasks = Task.query.filter_by(user_id=current_user).all()

        # Prioritize tasks using the custom algorithm
        prioritized_tasks = prioritize_tasks(tasks, user_id=current_user)

        return [task.to_dict() for task in prioritized_tasks], 200

    @bp.arguments(TaskSchema)
    @bp.response(201, TaskSchema)
    @jwt_required()
    def post(self, task_data):
        current_user = get_jwt_identity()
        task = Task(user_id=current_user, **task_data)
        task.save_to_db()
        return task, 201


@bp.route("/<int:task_id>")
class TaskDetail(MethodView):
    @bp.response(200, TaskSchema)
    @jwt_required()
    def get(self, task_id):
        current_user = get_jwt_identity()
        task = Task.query.filter_by(id=task_id, user_id=current_user).first()
        if not task:
            abort(404, message="Task not found.")
        return task

    @bp.arguments(TaskSchema)
    @bp.response(200, TaskSchema)
    @jwt_required()
    def put(self, task_data, task_id):
        current_user = get_jwt_identity()
        task = Task.query.filter_by(id=task_id, user_id=current_user).first()
        if not task:
            abort(404, message="Task not found.")
        task.update(task_data)
        return task

    @bp.response(204)
    @jwt_required()
    def delete(self, task_id):
        current_user = get_jwt_identity()
        task = Task.query.filter_by(id=task_id, user_id=current_user).first()
        if not task:
            abort(404, message="Task not found.")
        task.delete_from_db()
