# User preferences (stored in a dictionary)
user_preferences = {
    "user_id_1": {"due_date": 0.3, "urgency": 0.2, "importance": 0.5, "complexity": 0.1},
    # ... other users
}


# Task prioritization function
def prioritize_tasks(tasks, user_id):
    user_weights = user_preferences.get(user_id, {})  # Get user-specific weights

    # Calculate priority scores for tasks
    for task in tasks:
        task.priority_score = (
                user_weights.get("due_date", 0) * task.due_date +
                user_weights.get("urgency", 0) * task.urgency +
                user_weights.get("importance", 0) * task.importance +
                user_weights.get("complexity", 0) * task.complexity
        )

    # Prioritize tasks based on priority scores
    prioritized_tasks = sorted(tasks, key=lambda x: x.priority_score, reverse=True)
    return prioritized_tasks
