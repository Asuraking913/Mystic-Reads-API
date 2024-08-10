from app import create_app
from os import system
from events import socket

app = create_app()

if __name__ == '__main__':
    # app.run(debug=True)
    socket.run(app, debug=True)
    