from extensions import socket
from models import User
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flask_socketio import emit, join_room, leave_room, rooms
from flask import request


def root_socket(soc, db):

    
    # @soc.on('connect')
    # def handle_connect():
    #     user_id = request.sid
    #     room_name = (user_id)
    #     join_room(room_name)
    #     soc.emit('response', 'user added to new room')
    #     print('Client Connected')
    #     print(request.sid)
    #     print(rooms(), flush = True)


    # @soc.on('message')
    # def handle_friend(data):
    #     room = rooms()
    #     if request.sid not in rooms():
    #         print('Invalid user', flush = True )
    #     else:
    #         print('valid user', flush = True )
    #         print(len(rooms()))
    #         print(data, flush = True)
    #         emit('new_message', {"message" : data}, broadcast = rooms()[0])

    @soc.on('create_room')
    def handle_join(data):
        user_id = data['userId']
        target_user = data['targerId']
    pass
