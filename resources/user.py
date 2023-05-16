import os 

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from db import db
from models import UserModel

from schemas import UserSchema, UserLoginSchema, UserUpdateSchema

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
            return {"id": user.id}, 200
        
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
    
@blp.route("/update-user/<int:user_id>")
class UpdateUser(MethodView):

    @blp.response(201, UserSchema)
    @blp.arguments(UserUpdateSchema)
    def put(self, user_data, user_id):
        user = UserModel.query.get_or_404(user_id)
        
         
        user.username = user_data.get("username", user.username)
        user.email = user_data.get("email", user.email)
        user.password = user_data.get("password", user.password)
        
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            if user_data.get("username"):
                abort(409, message="A user with that username already exists.")
            elif user_data.get("email"):
                abort(409, message="A user with that email already exists.")

        except SQLAlchemyError:
            abort(400, message="Bad request.")
        except Exception:
            abort(500)
            
        return user
    
@blp.route("/delete-user/<int:user_id>")
class DeleteUser(MethodView):
        
        @blp.response(204)
        def delete(self, user_id):
            user = UserModel.query.get_or_404(user_id)
            db.session.delete(user)
            db.session.commit()
            
            return {"message": "User delete successfully."}, 204
        

        