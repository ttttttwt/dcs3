import os

from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv # load environment variables from .env file

from resource.user import blp as UserBlueprint
from resource.active import blp as ActiveBlueprint
from resource.location import blp as LocationBlueprint

from db import db
import models # let's db know about all the models


def create_app():
    app = Flask(__name__)
    load_dotenv()
    
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "RunMate REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/api"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        
    api = Api(app)
    api.register_blueprint(UserBlueprint) # register the blueprint to the api
    api.register_blueprint(ActiveBlueprint) # register the blueprint to the api
    api.register_blueprint(LocationBlueprint) # register the blueprint to the api
    
        
    @app.route("/")
    def home_page():
        return "Hello World"
    
    
    return app
    
    


# app.run(debug=True)

