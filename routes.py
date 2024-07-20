def root_routes(app):
    
    @app.route("/")
    def home():
        return "<h1>This is the home page</h1>"