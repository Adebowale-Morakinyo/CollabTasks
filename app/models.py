from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_password(self, password):
        self.password = pbkdf2_sha256.hash(password)

    def check_password(self, password):
        return pbkdf2_sha256.verify(self.password, password)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    priority = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('tasks', lazy=True))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def update(self, data):
        self.title = data.get('title', self.title)
        self.description = data.get('description', self.description)
        self.priority = data.get('priority', self.priority)

        # Ensuring that the updated_at field is always updated
        self.updated_at = datetime.utcnow()

        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class Collaboration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class UserPreferences(db.Model):
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
