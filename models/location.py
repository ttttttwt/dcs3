from db import db


class LocationModel(db.Model):
    __tablename__ = "locations"
    
    id = db.Column(db.Integer, primary_key=True)
    active_id = db.Column(db.Integer, db.ForeignKey('actives.id'), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    distance = db.Column(db.Float, nullable=False)
    time = db.Column(db.DateTime, nullable=False)