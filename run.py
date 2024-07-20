from app import create_app

flask = create_app()

if __name__ == '__main__':
    flask.run(debug=True)