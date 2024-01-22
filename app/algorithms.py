from app.models import UserPreferences


# Fetch user preferences from the database
def fetch_user_preferences(user_id):
    # Logic to fetch user preferences from the database
    # Example: Assuming UserPreferences model has been defined
    user_preferences = UserPreferences.query.filter_by(user_id=user_id).first()
    return user_preferences.to_dict() if user_preferences else {}


# Task prioritization function
def prioritize_tasks(tasks, user_id):
    # Fetch user preferences from the database
    user_preferences = fetch_user_preferences(user_id)

    # Calculate priority scores for tasks
    for task in tasks:
        task.priority_score = calculate_priority_score(task, user_preferences)

    # Prioritize tasks based on priority scores
    prioritized_tasks = sorted(tasks, key=lambda x: x.priority_score, reverse=True)
    return prioritized_tasks


# Function to calculate priority score for a task
def calculate_priority_score(task, user_preferences):
    # Get user-specific weights or use defaults if not set
    due_date_weight = user_preferences.get("due_date", 0.2)
    urgency_weight = user_preferences.get("urgency", 0.3)
    importance_weight = user_preferences.get("importance", 0.4)
    complexity_weight = user_preferences.get("complexity", 0.1)

    # Calculate priority score using a weighted sum
    priority_score = (
            due_date_weight * task.due_date +
            urgency_weight * task.urgency +
            importance_weight * task.importance +
            complexity_weight * task.complexity
    )

    return priority_score
