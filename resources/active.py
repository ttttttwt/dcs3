import os 

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy import or_

from db import db
from models import ActiveModel
from models import UserModel

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
            date=active_data["date"],
        )
        db.session.add(active)
        db.session.commit()
        
        return {"message": "Active created successfully."}, 201
    
    