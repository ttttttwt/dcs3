import os 

from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy import or_
import datetime

from db import db
from models import ActiveModel
from models import UserModel
from models import LocationModel

from schemas import ActiveSchema



blp = Blueprint("Actives", "actives", description="Operations on actives")


@blp.route("/actives/<int:user_id>")
class Actives(MethodView):
    
    @blp.response(200, ActiveSchema(many=True))
    def get(self, user_id):
        actives = ActiveModel.query.filter_by(user_id=user_id).all()
        
        if not actives:
            abort(404, message=f"user_id {user_id} not found")
            
        return actives
    

@blp.route("/add-active/")
class AddActive(MethodView):
    
    @blp.arguments(ActiveSchema)
    def post(self, active_data):
        
        if not UserModel.query.filter(
                UserModel.id == active_data["user_id"],
            ).first():
            abort(409, message="user_id not found.")
        
        active = ActiveModel(
            user_id=active_data["user_id"],
            date= active_data["date"],
            time = active_data["time"],
            distance = active_data["distance"],
            speed = active_data["speed"],
        )
        db.session.add(active)
        db.session.commit()
        
        return {"message": "Active created successfully.", "id": active.id}, 201
    
# count distance
@blp.route("/count-distance/<int:active_id>")
class CountDistance(MethodView):
    
    @blp.response(200, ActiveSchema)
    def get(self, active_id):
        active = ActiveModel.query.filter_by(id=active_id).first()
        
        if not active:
            abort(404, message=f"active_id {active_id} not found")
            
        locations = LocationModel.query.filter_by(active_id=active_id).all()
        
        if not locations:
            abort(404, message=f"no location not found")
            
        distance = 0
       
        return active

@blp.route("/statistical/<int:user_id>")
class Statistical(MethodView):
    
    @blp.response(200)
    def get(self, user_id):
        actives = ActiveModel.query.filter_by(user_id=user_id).all()
        user = UserModel.query.filter_by(id=user_id).first()
        if not user:
            abort(404, message=f"user_id {user_id} not found")
                    
        distance = 0
        average_speed = 0
        time = 0
        for active in actives:
            if active.distance == None:
                distance += 0
            else:
                distance += active.distance
 
            if active.speed == None:
                average_speed += 0
            else:
                average_speed += active.speed
                
            if active.time == None:
                time += 0
            else:
                time += active.time
                
        try:
            average_speed = average_speed / len(actives)
        except:
            average_speed = 0
             
        return {"distance": distance, "average_speed": average_speed, "time": time}, 200
    
@blp.route("/get-day-of-week/<int:user_id>")
class getWeek(MethodView):

    @blp.response(200)
    def get(self, user_id):
        result = {"day_0": 0, "day_1": 0, "day_2": 0, "day_3": 0, "day_4": 0, "day_5": 0, "day_6": 0}
        current_date = datetime.datetime.now()
        start_of_week = current_date - datetime.timedelta(days=current_date.weekday())

        for i in range(7):
            target_date = start_of_week + datetime.timedelta(days=i)
            actives = ActiveModel.query.filter_by(user_id=user_id, date=target_date.strftime('%Y-%m-%d')).all()

            if actives:
                for active in actives:
                        result[f"day_{i}"] = 1

        return result, 200

        
@blp.route("/get-day-week-distance/<int:user_id>")
class getWeekDistance(MethodView):

    @blp.response(200)
    def get(self, user_id):
        result = {"day_0": 0, "day_1": 0, "day_2": 0, "day_3": 0, "day_4": 0, "day_5": 0, "day_6": 0}
        current_date = datetime.datetime.now()
        start_of_week = current_date - datetime.timedelta(days=current_date.weekday())

        for i in range(7):
            target_date = start_of_week + datetime.timedelta(days=i)
            actives = ActiveModel.query.filter_by(user_id=user_id, date=target_date.strftime('%Y-%m-%d')).all()

            if actives:
                for active in actives:
                    if active.distance is not None:
                        result[f"day_{i}"] += active.distance

        return result, 200