from extensions import socket

@socket.on('connect')
def handle_connect():
    print('Client Connected')
    return 'User Connected'
