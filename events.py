from extensions import socket
from models import User


def root_socket(soc, db):
    
    @soc.on('connect')
    def handle_connect():
        print('Client Connected')
        soc.emit('response', 'user Connected')

    @soc.on('friend')
    def handle_friend():
        print('sdf')

