from flask import request, make_response, jsonify
from models import User, Posts, Comments, Likes
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token


def root_routes(app, db):
    hasher = Bcrypt()
    
    @app.route("/")
    def home():
        return "<h1>This is the home page</h1>"
    
    @app.route("/api/refresh_token")
    @jwt_required(refresh=True)
    def refresh_token(): 
        refreshed_user = get_jwt_identity()

        access_token = create_access_token(identity=refreshed_user)
        refresh_token = create_refresh_token(identity=refreshed_user)

        return jsonify({
            "access_token" : access_token, 
            "refresh_token" : refresh_token
        })

    @app.route("/api/auth/register", methods = ['POST'])
    def register_user():
        data = request.json

        username = data['userName']
        useremail = data['userEmail']
        userpass = data['userPass']
        gender = data['gender']
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
                    "message" : "User Email Already Exists", 
                }, 400
            

        new_user = User(username, useremail, gender, userpass)
        db.session.add(new_user)
        db.session.commit()
        user = User.query.filter_by(user_email = useremail).first()

        response =  make_response(jsonify({
            "status" : "success",
            "message" : "Registration Sucessfull", 
            "data" : {
                "userId" : user._id, 
                "userName" : user.user_name, 
                "userEmail" : user.user_email, 
                "gender" : user.gender, 
                "joined" : user.joined 
            }
        }))

        return response, 201
    
    @app.route("/api/auth/login", methods = ['POST'])
    def login_user():
        data = request.json
        userpass = data['userPass']
        try:
            username = data['userName']
            auth_user = User.query.filter_by(user_name = username).first()
            if auth_user:
                if hasher.check_password_hash(auth_user.user_pass, userpass):
                    access_token = create_access_token(identity=auth_user._id)
                    refresh_token = create_refresh_token(identity=auth_user._id)
                    response =  make_response(jsonify({
                        "status" : "success",
                        "message" : "Login Sucessfull", 
                        "data" : { 
                            "access_token" : access_token,
                            "refresh_token" : refresh_token,
                            "userId" : auth_user._id, 
                            "userName" : auth_user.user_name, 
                            "userEmail" : auth_user.user_email, 
                            "gender" : auth_user.gender, 
                            "joined" : auth_user.joined,
                            "birthday" : auth_user.birthday,
                            "bio" : auth_user.bio,
                            "location" : auth_user.current_location
                        }
                    }))
                    # response.set_cookie('access_token', access_token, samesite='Strict', secure=True, httponly=True)

                    return response, 200

                return {
                    "status" : "unsucessfull",
                    "message" : "Incorrect Password", 
                }, 400
            

            return {
                    "status" : "unsucessfull",
                    "message" : "Invalid Username/email address", 
                }, 400

        except Exception as e:
            useremail = data['userEmail']
            auth_user = User.query.filter_by(user_email = useremail).first()
            if auth_user:
                if hasher.check_password_hash(auth_user.user_pass, userpass):
                    access_token = create_access_token(identity=auth_user._id)
                    refresh_token = create_refresh_token(identity=auth_user._id)
                    response =  make_response(jsonify({
                        "status" : "success",
                        "message" : "Login Sucessfull", 
                        "data" : {
                            "access_token" : access_token,
                            "refresh_token" : refresh_token,
                            "userId" : auth_user._id, 
                            "userName" : auth_user.user_name, 
                            "gender" : auth_user.gender, 
                            "userEmail" : auth_user.user_email,
                            "gender" : auth_user.gender,
                            "birthday" : auth_user.birthday,
                            "bio" : auth_user.bio,
                            "location" : auth_user.current_location
                        }
                    }))
                    # response.set_cookie('access_token', access_token, samesite='Strict', secure=True, httponly=True)

                    return response, 200

                return {
                    "status" : "unsucessfull",
                    "message" : "Invalid Username or password2", 
                }, 400
            

            return {
                    "status" : "unsucessfull",
                    "message" : "Email does Not exist", 
                }, 400
    
    @app.route("/api/profiles_info", methods = ['POST'])
    @jwt_required()
    def update_profile():
        required_fields = ['bio', 'location', 'birthday']
        data = request.json
        
        if request.method == 'POST':
            for fields in required_fields:
                if fields not in data:
                    return {
                        "status" : "unsuccessfull", 
                        "message" : f"Missing field {fields}"
                    }
            user_id = get_jwt_identity()
            auth_user = User.query.filter_by(_id = user_id).first()
            if auth_user:
                auth_user.bio 
                auth_user.bio = data['bio']
                auth_user.birthday = data['birthday']
                auth_user.current_location = data['location']
                db.session.commit()

                response = {
                    'status': "success",
                    'message': "User Profile Updated",
                    "data": {
                        "userId": auth_user._id,
                        "userName": auth_user.user_name,
                        "userEmail": auth_user.user_email,
                        "member": auth_user.joined,
                        "gender": auth_user.gender,
                        "birthday": auth_user.birthday,
                        "bio": auth_user.bio,
                        "location": auth_user.current_location
                    }
                }
                return jsonify(response), 201
            
            response = jsonify({
                    "status" : "unsuccessfull", 
                    "message" : "UserName Does not exist"
                })
            
            return response, 400
            
        response =  jsonify({
            "status" : "Unsuccessfull", 
            "message" : "User Does not exist"
        })
        return response, 404
        
    @app.route("/api/profiles_info/<userId>")
    @jwt_required()
    def get_user_info(userId):
        if request.method == 'GET':
            foreign_user = User.query.filter_by(_id = userId).first()
            if foreign_user:
                response = jsonify({
                    'status': "success",
                    'message': "User details",
                    "data": {
                        "userId": foreign_user._id,
                        "userName": foreign_user.user_name,
                        "userEmail": foreign_user.user_email,
                        "member": foreign_user.joined,
                        "gender": foreign_user.gender,
                        "birthday": foreign_user.birthday,
                        "bio": foreign_user.bio,
                        "location": foreign_user.current_location
                    }
                })
                
                return response, 200
            

            response = jsonify({
                    "status" : "unsuccessfull", 
                    "message" : "UserName Does not exist"
                })
            
            return response, 400
        
        response =  jsonify({
            "status" : "Unsuccessfull", 
            "message" : "User Does not exist"
        })
        return response, 404
            

        
    #current user create post Endopint
    @app.route("/api/user_posts", methods = ['POST'])  
    @jwt_required()
    def create_post(user_id):
        if request.method == 'POST':
            data = request.json
            content = data['content']
            user_id1 = get_jwt_identity()
            current_user = User.query.filter_by(_id = user_id1).first()
            if current_user:
                new_post = Posts(content, current_user)
                db.session.add(new_post)
                db.session.commit()

                return {
                        'status' : "success", 
                        'message' : "Created new post", 
                        "data" : {
                                "userId" : current_user._id, 
                                "userName" : current_user.user_name,
                            },
                            'post' : {
                                'content' : new_post.content, 
                                'time' : new_post.time_created,
                                "postId" : new_post._id,
                            }
                        }, 201  
            return {
                        "status" : "unsucessfull",
                        "message" : "Invalid user", 
                    }, 400


    #foreign user enpoint
    @app.route("/api/user_posts/<user_id>")
    def get_user_posts(user_id):
        if request.method == 'GET': 
            current_user = User.query.filter_by(_id = user_id).first()
            if current_user:
                list_posts = current_user.post

                return {
                        'status' : "success", 
                        'message' : "List of user posts", 
                        "data" : {
                                "userId" : current_user._id, 
                                "userName" : current_user.user_name,
                                "postList" : [
                                        {
                                            "content" : Posts.query.filter_by(_id = post._id).first().content, 
                                            "postId" : Posts.query.filter_by(_id = post._id).first()._id, 
                                            "postLikes" : Posts.query.filter_by(_id = post._id).first().likes,
                                            "postComments" : Posts.query.filter_by(_id = post._id).first().comments
                                            } 
                                    for post in list_posts]}
                            }, 200
            return {
                        "status" : "unsucessfull",
                        "message" : "Unable to get list of posts", 
                    }, 400
    
    @app.route("/api/<postId>/likes", methods = ['POST'])
    @jwt_required()
    def add_like(postId):
        if request.method == 'POST':
            data = request.json
            current_user = User.query.filter_by(_id = get_jwt_identity()).first()
            target_post = Posts.query.filter_by(_id = postId).first()
            if current_user and target_post:
                new_like = Likes(current_user, target_post)
                db.session.add(new_like)
                db.session.commit()
                
                return {
                    "status" : "success",
                    "message" : "Post was liked sucessfully",
                    "data" : {
                        "postId" : postId,
                        "postContent" : target_post.content
                    }
                }, 201
            return {
                        "status" : "unsucessfull",
                        "message" : "Invalid User/post credentials", 
                    }, 400
        
        return {
            'status' : "uncessfull", 
            'message' : "Invalid"
        }, 400
