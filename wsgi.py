from app import create_app
from events import socket

app = create_app()

if __name__ == "__main__":
    app.run()