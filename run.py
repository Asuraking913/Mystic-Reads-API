from app import create_app
from os import system
from events import socket

flask_app = create_app()

if __name__ == '__main__':
    # flask_app.run(debug=True)
    socket.run(flask_app, debug=True)