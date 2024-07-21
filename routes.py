from flask import request, make_response, jsonify
from models import User, Posts, Comments, Likes
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


def root_routes(app, db):
    hasher = Bcrypt()
    
    @app.route("/")
    def home():
        return "<h1>This is the home page</h1>"

    @app.route("/api/auth/register", methods = ['POST'])
    def register_user():
        data = request.json

        username = data['userName']
        useremail = data['userEmail']
        userpass = data['userPass']
        userpass = hasher.generate_password_hash(userpass).decode('utf-8')

        universal_users = User.query.all()
        for users in universal_users:
            if users.user_name == username:
                return {
                    "status" : "unsucessfull",
                    "message" : "User Name Already Exists", 
                }, 400
            if users.user_email == useremail:
                return {
                    "status" : "unsucessfull",
                    "message" : "User Name Already Exists", 
                }, 400
            

        new_user = User(username, useremail, userpass)
        db.session.add(new_user)
        db.session.commit()
        user = User.query.filter_by(user_email = useremail).first()
        access_token = create_access_token(identity= user._id)

        response =  make_response(jsonify({
            "status" : "success",
            "message" : "Registration Sucessfull", 
            "user" : {
                "userId" : user._id, 
                "userName" : user.user_name, 
                "userEmail" : user.user_email, 
                "joined" : user.joined 
            }
        }))

        response.set_cookie('access_token', access_token, httponly=True, samesite="Strict", secure=True)
        return response, 201
    
    @app.route("/api/auth/login", methods = ['POST'])
    def login_user():
        data = request.json
        userpass = data['userPass']
        print(data)
        try:
            username = data['userName']
            auth_user = User.query.filter_by(user_name = username).first()
            if auth_user:
                if hasher.check_password_hash(auth_user.user_pass, userpass):
                    access_token = create_access_token(identity=auth_user._id)
                    response =  make_response(jsonify({
                        "status" : "success",
                        "message" : "Login Sucessfull", 
                        "user" : {
                            "access_token" : access_token, 
                            "userId" : auth_user._id, 
                            "userName" : auth_user.user_name, 
                            "userEmail" : auth_user.user_email, 
                            "joined" : auth_user.joined 
                        }
                    }))
                    response.set_cookie('access_token', access_token, samesite='Strict', secure=True, httponly=True)

                    return response

                return {
                    "status" : "unsucessfull",
                    "message" : "Incorrect Password", 
                }, 400
            

            return {
                    "status" : "unsucessfull",
                    "message" : "Username does Not exist", 
                }, 400

        except Exception as e:
            useremail = data['userEmail']
            auth_user = User.query.filter_by(user_email = useremail).first()
            if auth_user:
                if hasher.check_password_hash(auth_user.user_pass, userpass):
                    response =  make_response(jsonify({
                        "status" : "success",
                        "message" : "Login Sucessfull", 
                        "user" : {
                            "userId" : auth_user._id, 
                            "userName" : auth_user.user_name, 
                            "userEmail" : auth_user.user_email
                        }
                    }))
                    access_token = create_access_token(identity=auth_user._id)
                    response.set_cookie('access_token', access_token, samesite='Strict', secure=True, httponly=True)

                    return response, 200

                return {
                    "status" : "unsucessfull",
                    "message" : "Incorrect Password", 
                }, 400
            

            return {
                    "status" : "unsucessfull",
                    "message" : "Email does Not exist", 
                }, 400
    
    @app.route("/api/profiles_info", methods = ['POST', 'GET'])
    @jwt_required()
    def update_profile():
        if request.method == 'GET':
            user_id = get_jwt_identity()
            if user_id:
                current_user = User.query.filter_by(_id = user_id).first()
                if current_user:
                    response = {
                        'status' : "success", 
                        'message' : "User Profiles", 
                        "user" : {
                            "userId" : current_user._id, 
                            "userName" : current_user.user_name, 
                            "userEmail" : current_user.user_email,
                            "member" : current_user.joined,
                            "gender" : current_user.gender,
                            "birthday" : current_user.birthday,
                            "bio" : current_user.bio,
                        }
                    }
                    return response, 200
                
        if request.method == 'POST':
            data = request.json
            user_id = get_jwt_identity()
            if user_id:
                current_user = User.query.filter_by(_id = user_id).first()
                if current_user:
                    current_user.bio = data['bio']
                    current_user.birthday = data['birthday']
                    current_user.gender = data['gender']
                    db.session.commit()
                    return  {
                        'status' : "success", 
                        'message' : "User Profiles", 
                        "user" : {
                            "userId" : current_user._id, 
                            "userName" : current_user.user_name, 
                            "userEmail" : current_user.user_email,
                            "member" : current_user.joined,
                            "gender" : current_user.gender,
                            "birthday" : current_user.birthday,
                            "bio" : current_user.bio,
                        }
                    }, 201
            return {
                    "status" : "unsucessfull",
                    "message" : "Email does Not exist", 
                }, 400
        
    @app.route("/api/new_post/<user_id>", methods = ['POST', 'GET'])  
    @jwt_required()
    def create_post(user_id):
        if request.method == 'POST':
            data = request.json
            content = data['content']
            # user_id = get_jwt_identity()
            current_user = User.query.filter_by(_id = user_id).first()
            new_post = Posts(content, current_user)
            db.session.add(new_post)
            db.session.commit()

            return {
                    'status' : "success", 
                    'message' : "Created new post", 
                    'user' : {
                        "userId" : current_user._id, 
                        "userName" : current_user.user_name,
                    },
                    'post' : {
                        'content' : new_post.content, 
                        'time' : new_post.time_created,
                        "postId" : new_post._id,
                    }
            }, 201
        
        if request.method == 'GET': 

            current_user = User.query.filter_by(_id = user_id).first()
            list_posts = current_user.post

            return {
                    'status' : "success", 
                    'message' : "List of user posts", 
                    'user' : {
                        "userId" : current_user._id, 
                        "userName" : current_user.user_name,
                    },
                    "postList" : [
                        {
                        "content" : Posts.query.filter_by(_id = post._id).first().content, 
                        "postId" : Posts.query.filter_by(_id = post._id).first()._id, 
                        "postLikes" : Posts.query.filter_by(_id = post._id).first().likes,
                        "postComments" : Posts.query.filter_by(_id = post._id).first().comments
                        } 
                        for post in list_posts]
            }, 200
