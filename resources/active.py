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
        
        return {"message": "Active created successfully."}, 201
    
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
            distance = distance / len(actives)
        except:
            distance = 0 
        return {"distance": distance, "average_speed": average_speed, "time": time}, 200
    
@blp.route("/get-day-of-week/<int:user_id>")
class getDayOfWeek(MethodView):
    
    @blp.response(200)
    def get(self, user_id,):
        
        temp = [None, None, None, None, None, None, None]
        currunt_date = datetime.datetime.now()
        before = None
        day_of_week = currunt_date.weekday()
        if day_of_week == 0:
            before = currunt_date
            temp[0] = ActiveModel.query.filter_by(user_id=user_id, date=currunt_date.strftime('%Y-%m-%d')).first()
        elif day_of_week == 1:
            before = currunt_date - datetime.timedelta(days=1)
            temp[1] = ActiveModel.query.filter_by(user_id=user_id, date=currunt_date.strftime('%Y-%m-%d')).first()
            temp[0] = ActiveModel.query.filter_by(user_id=user_id, date=before.strftime('%Y-%m-%d')).first()
            
        elif day_of_week == 2:
            before = currunt_date - datetime.timedelta(days=2)
            temp[2] = ActiveModel.query.filter_by(user_id=user_id, date=currunt_date.strftime('%Y-%m-%d')).first()
            temp[1] = ActiveModel.query.filter_by(user_id=user_id, date=before + datetime.timedelta(days=1)).first()
            temp[0] = ActiveModel.query.filter_by(user_id=user_id, date=before.strftime('%Y-%m-%d')).first()
        
        elif day_of_week == 3:
            before = currunt_date - datetime.timedelta(days=3)
            temp[3] = ActiveModel.query.filter_by(user_id=user_id, date=currunt_date.strftime('%Y-%m-%d')).first()
            temp[2] = ActiveModel.query.filter_by(user_id=user_id, date=before + datetime.timedelta(days=1)).first()
            temp[1] = ActiveModel.query.filter_by(user_id=user_id, date=before + datetime.timedelta(days=2)).first()
            temp[0] = ActiveModel.query.filter_by(user_id=user_id, date=before.strftime('%Y-%m-%d')).first()
            
        elif day_of_week == 4:
            before = currunt_date - datetime.timedelta(days=4)
            temp[4] = ActiveModel.query.filter_by(user_id=user_id, date=currunt_date.strftime('%Y-%m-%d')).first()
            temp[3] = ActiveModel.query.filter_by(user_id=user_id, date=before + datetime.timedelta(days=1)).first()
            temp[2] = ActiveModel.query.filter_by(user_id=user_id, date=before + datetime.timedelta(days=2)).first()
            temp[1] = ActiveModel.query.filter_by(user_id=user_id, date=before + datetime.timedelta(days=3)).first()
            temp[0] = ActiveModel.query.filter_by(user_id=user_id, date=before.strftime('%Y-%m-%d')).first()
            
        elif day_of_week == 5:
            before = currunt_date - datetime.timedelta(days=5)
            temp[5] = ActiveModel.query.filter_by(user_id=user_id, date=currunt_date.strftime('%Y-%m-%d')).first()
            temp[4] = ActiveModel.query.filter_by(user_id=user_id, date=before + datetime.timedelta(days=1)).first()
            temp[3] = ActiveModel.query.filter_by(user_id=user_id, date=before + datetime.timedelta(days=2)).first()
            temp[2] = ActiveModel.query.filter_by(user_id=user_id, date=before + datetime.timedelta(days=3)).first()
            temp[1] = ActiveModel.query.filter_by(user_id=user_id, date=before + datetime.timedelta(days=4)).first()
            temp[0] = ActiveModel.query.filter_by(user_id=user_id, date=before.strftime('%Y-%m-%d')).first()
            
        elif day_of_week == 6:
            before = currunt_date - datetime.timedelta(days=6)
        
            temp[6] = ActiveModel.query.filter_by(user_id=user_id, date=currunt_date.strftime('%Y-%m-%d')).first()
            temp[5] = ActiveModel.query.filter_by(user_id=user_id, date=before + datetime.timedelta(days=1)).first()
            temp[4] = ActiveModel.query.filter_by(user_id=user_id, date=before + datetime.timedelta(days=2)).first()
            temp[3] = ActiveModel.query.filter_by(user_id=user_id, date=before + datetime.timedelta(days=3)).first()
            temp[2] = ActiveModel.query.filter_by(user_id=user_id, date=before + datetime.timedelta(days=4)).first()
            temp[1] = ActiveModel.query.filter_by(user_id=user_id, date=before + datetime.timedelta(days=5)).first()
            temp[0] = ActiveModel.query.filter_by(user_id=user_id, date=before.strftime('%Y-%m-%d')).first()
            
            
        result = {}
        for i in range(len(temp)):
            if temp[i] is not None:
                result[f"day_{i}"] = 1
            else:
                result[f"day_{i}"] = 0
                
        
        return result, 200
        
@blp.route("/get-day-of-week-distance/<int:user_id>")
class getDayOfWeekDitance(MethodView):
    
    @blp.response(200)
    def get(self, user_id,):
        
        temp = [None, None, None, None, None, None, None]
        currunt_date = datetime.datetime.now()
        before = None
        day_of_week = currunt_date.weekday()
        if day_of_week == 0:
            before = currunt_date
            temp[0] = ActiveModel.query.filter_by(user_id=user_id, date=currunt_date.strftime('%Y-%m-%d')).all()
        elif day_of_week == 1:
            before = currunt_date - datetime.timedelta(days=1)
            temp[1] = ActiveModel.query.filter_by(user_id=user_id, date=currunt_date.strftime('%Y-%m-%d')).all()
            temp[0] = ActiveModel.query.filter_by(user_id=user_id, date=before.strftime('%Y-%m-%d')).all()
            
        elif day_of_week == 2:
            before = currunt_date - datetime.timedelta(days=2)
            temp[2] = ActiveModel.query.filter_by(user_id=user_id, date=currunt_date.strftime('%Y-%m-%d')).all()
            temp[1] = ActiveModel.query.filter_by(user_id=user_id, date=before + datetime.timedelta(days=1)).all()
            temp[0] = ActiveModel.query.filter_by(user_id=user_id, date=before.strftime('%Y-%m-%d')).all()
        
        elif day_of_week == 3:
            before = currunt_date - datetime.timedelta(days=3)
            temp[3] = ActiveModel.query.filter_by(user_id=user_id, date=currunt_date.strftime('%Y-%m-%d')).all()
            temp[2] = ActiveModel.query.filter_by(user_id=user_id, date=before + datetime.timedelta(days=1)).all()
            temp[1] = ActiveModel.query.filter_by(user_id=user_id, date=before + datetime.timedelta(days=2)).all()
            temp[0] = ActiveModel.query.filter_by(user_id=user_id, date=before.strftime('%Y-%m-%d')).all()
            
        elif day_of_week == 4:
            before = currunt_date - datetime.timedelta(days=4)
            temp[4] = ActiveModel.query.filter_by(user_id=user_id, date=currunt_date.strftime('%Y-%m-%d')).all()
            temp[3] = ActiveModel.query.filter_by(user_id=user_id, date=before + datetime.timedelta(days=1)).all()
            temp[2] = ActiveModel.query.filter_by(user_id=user_id, date=before + datetime.timedelta(days=2)).all()
            temp[1] = ActiveModel.query.filter_by(user_id=user_id, date=before + datetime.timedelta(days=3)).all()
            temp[0] = ActiveModel.query.filter_by(user_id=user_id, date=before.strftime('%Y-%m-%d')).all()
            
        elif day_of_week == 5:
            before = currunt_date - datetime.timedelta(days=5)
            temp[5] = ActiveModel.query.filter_by(user_id=user_id, date=currunt_date.strftime('%Y-%m-%d')).all()
            temp[4] = ActiveModel.query.filter_by(user_id=user_id, date=before + datetime.timedelta(days=1)).all()
            temp[3] = ActiveModel.query.filter_by(user_id=user_id, date=before + datetime.timedelta(days=2)).all()
            temp[2] = ActiveModel.query.filter_by(user_id=user_id, date=before + datetime.timedelta(days=3)).all()
            temp[1] = ActiveModel.query.filter_by(user_id=user_id, date=before + datetime.timedelta(days=4)).all()
            temp[0] = ActiveModel.query.filter_by(user_id=user_id, date=before.strftime('%Y-%m-%d')).all()
            
        elif day_of_week == 6:
            before = currunt_date - datetime.timedelta(days=6)
        
            temp[6] = ActiveModel.query.filter_by(user_id=user_id, date=currunt_date.strftime('%Y-%m-%d')).all()
            temp[5] = ActiveModel.query.filter_by(user_id=user_id, date=before + datetime.timedelta(days=1)).all()
            temp[4] = ActiveModel.query.filter_by(user_id=user_id, date=before + datetime.timedelta(days=2)).all()
            temp[3] = ActiveModel.query.filter_by(user_id=user_id, date=before + datetime.timedelta(days=3)).all()
            temp[2] = ActiveModel.query.filter_by(user_id=user_id, date=before + datetime.timedelta(days=4)).all()
            temp[1] = ActiveModel.query.filter_by(user_id=user_id, date=before + datetime.timedelta(days=5)).all()
            temp[0] = ActiveModel.query.filter_by(user_id=user_id, date=before.strftime('%Y-%m-%d')).all()
            
            
        result = {"day_0": 0, "day_1": 0, "day_2": 0, "day_3": 0, "day_4": 0, "day_5": 0, "day_6": 0}
        for i in range(len(temp)):
            if temp[i] is not None:
                for active in temp[i]: # type: ignore
                    if active.distance is not None:
                        result[f"day_{i}"] += active.distance
                    else:
                        result[f"day_{i}"] += 0
            else:
                result[f"day_{i}"] = 0
                
        
        return result, 200
        