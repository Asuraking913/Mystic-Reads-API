from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import AppConfig
from routes import root_routes
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    
    app = Flask(__name__)

    app.config.from_object(AppConfig)
    db.init_app(app)
    jwt.init_app(app)

    root_routes(app)

    with app.app_context():
        db.create_all()

    return app
