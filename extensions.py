import eventlet
eventlet.monkey_patch()
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO

db = SQLAlchemy()
jwt = JWTManager()
socket = SocketIO(async_mode = 'eventlet', logger= True, engineo_logger=True, message_queue='redis://')