from db import db


class ActiveModel(db.Model):
    __tablename__ = "actives"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    distance = db.Column(db.Float)
    time = db.Column(db.Float)
    speed = db.Column(db.Float)
    