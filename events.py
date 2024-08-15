from extensions import socket
from models import User, Friend, Room, Message
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flask_socketio import emit, join_room, leave_room, rooms
from flask import request


def root_socket(soc, db):

    
    @soc.on('connect')
    def handle_connect():
        print('Client Connected', flush = True)
        # print(request.sid)
        # print(rooms(), flush = True)

    @soc.on('join_rooms')
    def handle_join(data):
        user_id = data['userId']
        print(user_id, 'userId')
        list_rooms = Room.query.all()
        print(list_rooms, 'list_rooms')
        if list_rooms:
            for room in list_rooms:
                if user_id == room.user_one_id or user_id == room.user_two_id:
                    join_room(room._id)
                    print(rooms(), 'rooms()', flush = True)
                    print(data,'data', flush = True)

    @soc.on('init_room')
    def handle_new_room(data):
        user_id = data['userId']
        target_user = data['targetId']
        relation_id = data['relationId']

        friend_relation = Friend.query.filter_by(_id = relation_id).first()

        list_rooms = Room.query.all()
        if list_rooms:
            for rooms in list_rooms:
                if rooms.friend_relation_id == relation_id:
                    join_room(rooms._id)
                    emit('create_room_response', data, room=rooms._id)
                    return

        new_room = Room(user_id, target_user, relation_id)
        db.session.add(new_room)
        db.session.commit()
        join_room(new_room._id)
        data = {
            'status' : "sucess", 
            'message' : 'Sucessfully created chat room'
        }
        emit('create_room_response', data, room = user_id)

    @soc.on('send_message')
    def handleMessage(data):
        user_id = data['userId']
        target_user = data['targetId']
        relation_id = data['relationId']
        message = data['sms']
        print(user_id)
        print(target_user)
        print(relation_id)
        print(message)
        
        friend_relation = Friend.query.filter_by(_id = relation_id).first()
        user_room = friend_relation.room[0]._id
        if friend_relation.user_one_id == user_id and friend_relation.user_two_id == target_user or friend_relation.user_one_id == target_user and friend_relation.user_two_id == user_id:
            data = {
                'status' : "success", 
                'message' : "New Message"
            }

            new_message = Message(user_id, message, relation_id)
            db.session.add(new_message)
            db.session.commit()
            emit('receive_message', data, room=user_room)