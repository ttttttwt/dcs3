import os 

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy import or_

from db import db
from models import UserModel

from schemas import UserSchema, UserLoginSchema

blp = Blueprint("Users", "users", description="Operations on users")

@blp.route("/register")
class UserRegister(MethodView):
    
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(
            or_(
                UserModel.username == user_data["username"],
                UserModel.email == user_data["email"]
                )
            ).first():
            abort(409, message="A user with that username already exists.")

        user = UserModel(
            username=user_data["username"],
            email=user_data["email"],
            password=user_data["password"],
        )
        db.session.add(user)
        db.session.commit()
        
        return {"message": "User created successfully."}, 201
    
    
@blp.route("/login")
class UserLogin(MethodView):
    
    @blp.arguments(UserLoginSchema)
    def post(self, user_data):
        user = UserModel.query.filter_by(username=user_data["username"]).first()
        
        if user and user.password == user_data["password"]:
            return {"id:": user.id}, 200
        
        abort(401, message="Invalid credentials.")
    

@blp.route("/user/<int:user_id>")
class User(MethodView):
    
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user
    
    
@blp.route("/users")
class Users(MethodView):

    @blp.response(200, UserSchema(many=True))
    def get(self):
        users = UserModel.query.all()
        return users