from db import db


class UserPreferences(db.Model):
    __tablename__ = "user_preferences"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), unique=True, nullable=False)
    due_date = db.Column(db.Float, default=0.2)
    urgency = db.Column(db.Float, default=0.3)
    importance = db.Column(db.Float, default=0.4)
    complexity = db.Column(db.Float, default=0.1)

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "due_date": self.due_date,
            "urgency": self.urgency,
            "importance": self.importance,
            "complexity": self.complexity,
        }

    def update(self, data):
        self.due_date = data.get('due_date', self.title)
        self.urgency = data.get('urgency', self.description)
        self.importance = data.get('importance', self.priority)
        self.complexity = data.get('complexity', self.priority)

        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
