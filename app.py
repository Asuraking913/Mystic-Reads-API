from flask import Flask
from config import AppConfig
from routes import root_routes
from extensions import db, jwt

def create_app():
    
    app = Flask(__name__)

    app.config.from_object(AppConfig)
    db.init_app(app)
    jwt.init_app(app)

    root_routes(app, db)

    with app.app_context():
        db.create_all()

    return app

# if __name__ == "__main__":
#     flask_app = create_app()
#     flask_app.run()
