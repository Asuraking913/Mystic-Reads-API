from flask import Flask
from config import AppConfig
from routes import root_routes
from extensions import db, jwt
from flask_cors import CORS
from events import socket, root_socket

def create_app():
    
    app = Flask(__name__)

    app.config.from_object(AppConfig)
    db.init_app(app)
    jwt.init_app(app)
    socket.init_app(app, cors_allowed_origins = 'http://localhost:5173')
    # cors = CORS(app, resources={r"/*": {"origins": "*"}})
    CORS(app, resources={r'/*': {"origins" : 'http://localhost:5173'}})
    root_routes(app, db)
    root_socket(socket, db)

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run()
