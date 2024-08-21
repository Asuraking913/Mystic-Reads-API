import eventlet
eventlet.monkey_patch(socket=True)
from app import create_app
from events import socket, root_socket
from extensions import db

app = create_app()

root_socket(socket, db)


if __name__ == '__main__':
    app.run(debug=True)
    # socket.run(app, debug=False),
    # socket.run(app, port = 5000, debug=True)

    