import eventlet
eventlet.monkey_patch()
from app import create_app
from os import system
from events import socket, root_socket
from extensions import db
from flask import request

app = create_app()

root_socket(socket, db)

# @socket.on('message')
# def handle_friend():
#     print('new message')
#     socket.emit('response123', 'hey there')

if __name__ == '__main__':
    # app.run(debug=True)
    socket.run(app, port=5001, debug=True),
    