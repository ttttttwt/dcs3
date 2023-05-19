from db import db


class AdminModel(db.Model):
    __tablename__ = "admin"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(265), nullable=False)
