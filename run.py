from app import create_app
from os import system

flask_app = create_app()

if __name__ == '__main__':
    flask_app.run(debug=True)