from flask import request, make_response, jsonify
from models import User
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
        userpass = hasher.generate_password_hash(userpass)

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


        
