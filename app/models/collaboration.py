from db import db


class Collaboration(db.Model):
    __tablename__ = "collaboration"

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()