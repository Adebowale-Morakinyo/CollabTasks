from flask_socketio import emit, SocketIO

socketio = SocketIO()


@socketio.on("connect")
def handle_connect():
    print("Client connected")


@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")


@socketio.on("collaboration_added")
def handle_collaboration_added(data):
    task_id = data["task_id"]
    user_id = data["user_id"]

    # Handle collaboration added event, e.g., send a notification to the task owner
    # For simplicity, we'll print a message here
    print(f"Collaboration added on task {task_id} by user {user_id}")
