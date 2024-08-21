import eventlet
eventlet.monkey_patch(socket=True)
from app import create_app
from events import socket

app = create_app()

if __name__ == "__main__":
    app.run()