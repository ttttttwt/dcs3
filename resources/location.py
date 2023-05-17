import os 

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy import or_

from db import db
from models import ActiveModel
from models import LocationModel

from schemas import LocationSchema


blp = Blueprint("Locations", "locations", description="Operations on locations")

@blp.route("/location/<int:active_id>")
class Location(MethodView):
    
    @blp.response(200,LocationSchema(many=True))
    def get(self, active_id):
        locations = LocationModel.query.filter_by(active_id=active_id).all()
        
        if not locations:
            abort(404, message=f"active_id {active_id} not found")
            
        return locations, 200
    
@blp.route("/add-location/<int:active_id>")
class AddLocation(MethodView):
    
    @blp.arguments(LocationSchema(many=True))
    def post(self, location_datas, active_id):
        if not ActiveModel.query.filter(
                ActiveModel.id == active_id,
            ).first():
            abort(409, message="active_id not found.")
        
        for location_data in location_datas:
            location = LocationModel(
                active_id=active_id,
                latitude=location_data["latitude"],
                longitude=location_data["longitude"],
                time = location_data["time"],
            )
            db.session.add(location)
        
        db.session.commit()
        
        return {"message": "Location created successfully."}, 201
        
            
            
        