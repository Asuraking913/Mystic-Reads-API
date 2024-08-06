from flask import make_response, jsonify, request
from models import User, Posts, Comments, Likes, Image
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token
import magic
import base64
from flask_jwt_extended import set_access_cookies, set_refresh_cookies, unset_access_cookies, unset_refresh_cookies
import random

def root_routes(app, db):
    hasher = Bcrypt()
    
    
    @app.route("/")
    def home():
        return "<h1>This is the home page</h1>"
    
    # #test
    # @app.route("/upload", methods = ['POST'])
    # def upload_image():
    #     if "file" not in request.files:
    #         print('no Image')
    #         return "no image", 400
        
    #     new_file = request.files['file']
    #     if new_file:
    #         file_name = secure_filename(new_file.filename)
    #         data = new_file.read()
    #         newImage = Image(file_name = file_name, data = data)
    #         db.session.add(newImage)
    #         db.session.commit()
    #     return "Found Image Image"

    # @app.route("/receive/<id>")
    # def receive_file(id):
    #     file = Image.query.filter_by(_id = id).first()
    #     if file:
    #         return send_file(
    #             BytesIO(file.data), download_name=file.file_name, as_attachment=True
    #         )
    #     return "Image Does not exist"

    #app
    
    @app.route("/api/refresh_token")
    @jwt_required(refresh=True)
    def refresh_token(): 
        refreshed_user = get_jwt_identity()

        access_token = create_access_token(identity=refreshed_user)
        refresh_token = create_refresh_token(identity=refreshed_user)

        response = jsonify({
            "access_token" : access_token, 
            "refresh_token" : refresh_token
        })

        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)
        # response.set_cookie('access_token_cookie', access_token, samesite='Strict', httponly=True, secure=True)
        # response.set_cookie('refresh_token_cookie', refresh_token, samesite='Strict', httponly=True, secure=True)


        return response, 200

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
                        'access' : access_token,
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
                set_access_cookies(response, access_token)
                set_refresh_cookies(response, refresh_token)
                # response.set_cookie('access_token_cookie', access_token, samesite='Strict', httponly=True, secure=True)
                # response.set_cookie('refresh_token_cookie', refresh_token, samesite='Strict', httponly=True, secure=True)
                return response, 200
            return {
                "status" : "unsucessfull",
                "message" : "Incorrect Password", 
            }, 400
        
        # return {
        #         "status" : "unsucessfull",
        #         "message" : "Invalid Username/email address", 
        #     }, 400
        auth_user = User.query.filter_by(user_email = username).first()
        if auth_user:
            if hasher.check_password_hash(auth_user.user_pass, userpass):
                access_token = create_access_token(identity=auth_user._id)
                refresh_token = create_refresh_token(identity=auth_user._id)
                response =  make_response(jsonify({
                    "status" : "success",
                    "message" : "Login Sucessfull", 
                    "data" : {
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
                set_access_cookies(response, access_token)
                set_refresh_cookies(response, refresh_token)
                return response, 200
            return {
                "status" : "unsucessfull",
                "message" : "Incorrect Password", 
            }, 400
        

        return {
                "status" : "unsucessfull",
                "message" : "Invalid Username/Email", 
            }, 400
        
    @app.route("/api/logout", methods = ['GET'])
    @jwt_required()
    def logout():
        response = jsonify({
            'status' : 'Sucessfully', 
            'message' : "Logged out successfully"
        })

        unset_access_cookies(response)
        unset_refresh_cookies(response)
        return response

    @app.route("/api/profiles_info", methods = ['POST', 'GET'])
    @jwt_required()
    def get_update_profile():
        if request.method == 'POST':
            required_fields = ['bio', 'location', 'birthday']
            data = request.json
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
                        "joined": auth_user.joined,
                        "gender": auth_user.gender,
                        "birthday": auth_user.birthday,
                        "bio": auth_user.bio,
                        "location": auth_user.current_location
                    }
                }
                return jsonify(response), 201
            
            response = jsonify({
                    "status" : "unsuccessfull", 
                    "message" : "User Does not exist"
                })
            
            return response, 400

        if request.method == 'GET':
            user_id = get_jwt_identity()
            auth_user = User.query.filter_by(_id = user_id).first()
            if auth_user:
                response = {
                    'status': "success",
                    'message': "Fetched User data Sucessfully",
                    "data": {
                        "userId": auth_user._id,
                        "userName": auth_user.user_name,
                        "userEmail": auth_user.user_email,
                        "joined": auth_user.joined,
                        "gender": auth_user.gender,
                        "birthday": auth_user.birthday,
                        "bio": auth_user.bio,
                        "location": auth_user.current_location
                    }
                }
                return jsonify(response), 200

            response = jsonify({
                    "status" : "unsuccessfull", 
                    "message" : "UserName Does not exist"
                })

            return response, 400
        
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
                    "message" : "User Does not exist"
                })
            
            return response, 400
        
        response =  jsonify({
            "status" : "Unsuccessfull", 
            "message" : "User Does not exist"
        })
        return response, 404
    
    #get random posts
    @app.route("/api/fetch_feeds", methods = ['GET'])
    # @jwt_required()
    def fetch_random():
        mime = magic.Magic(mime=True)
        universal_post = Posts.query.all()
        feeds_list = []
        prev_post = []
        for _ in range(0, 10):
            selected_post = random.choice([items for items in universal_post if items != prev_post])
            prev_post = selected_post
            img = {"data" : base64.b64encode(selected_post.user.profile_image).decode('utf-8'), "mime" : mime.from_buffer(selected_post.user.profile_image)}
            new_post = {
                "userId" : selected_post._id, 
                "userName" : selected_post.user.user_name,
                "img" : img,
                "likes" : len(selected_post.likes), 
                "comments" : selected_post.comments,
                'content' : selected_post.content
            }
            feeds_list.append(new_post)

        
        return {
            'status' : 'sucessfull', 
            'message' : 'new feeds fetched sucessfully', 
            "data" : {
                'feeds' : feeds_list
            } 
        }


        
    #current user create post Endopint
    @app.route("/api/user_posts", methods = ['POST', 'GET'])  
    @jwt_required()
    def create_fetch_post():
        if request.method == 'POST':
            data = request.json
            content = data['content']
            user_id = get_jwt_identity()
            current_user = User.query.filter_by(_id = user_id).first()
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
        
        if request.method == 'GET':
            mime = magic.Magic(mime=True)
            user_id = get_jwt_identity()
            current_user = User.query.filter_by(_id = user_id).first()
            if current_user:
                if current_user.profile_image:
                    user_image = {"data" : base64.b64encode(current_user.profile_image).decode('utf-8'), "mime" : mime.from_buffer(current_user.profile_image)}
                    response =  jsonify({
                            'status' : "success", 
                            'message' : "Fetched post successfully", 
                            "data" : {
                                    "userId" : current_user._id, 
                                    "userName" : current_user.user_name,
                                    "userPic" : user_image,
                                    "post" : [
                                        {
                                            "content" : post.content, 
                                            "postId" : post._id, 
                                            "userId" : current_user._id, 
                                            "userName" : current_user.user_name
                                            } for post in current_user.post
                                        ]
                                }
                            })
                    return response, 200
                else:
                    return jsonify({
                            'status' : "success", 
                            'message' : "Fetched post successfully", 
                            "data" : {
                                    "userId" : current_user._id, 
                                    "userName" : current_user.user_name,
                                    "post" : [
                                        {
                                            "content" : post.content, 
                                            "postId" : post._id, 
                                            "userId" : current_user._id, 
                                            "userName" : current_user.user_name
                                            } for post in current_user.post
                                        ]
                                }
                            }), 200
            
            return {
                'status' : 'unsuccessfull', 
                'message' : "Invalid User"
            }


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
    
    def file_ext(filename):
        allowed_extensions = ['jpg', 'png', "jpeg", 'svg']
        # file_ext = filename.filename.rsplit(".", 1)[-1]
        return '.' in filename and filename.rsplit(".", 1)[-1].lower() in allowed_extensions 
    
    
    @app.route("/api/upload_picture", methods = ['POST'])
    @jwt_required()
    def upload_picture():
        user_id = get_jwt_identity()
        auth_user = User.query.filter_by(_id = user_id).first()
        try:
            profile_image = request.files['profile']

            if profile_image:
                if file_ext(profile_image.filename):
                    auth_user.profile_image = profile_image.read()
                    db.session.commit()
                    return jsonify({
                        "status" : "success",
                        "message" : "Profile photo uploaded sucessfully",
                    }), 201

                response = jsonify({
                    "status" : "unsuccessfull",
                    "message" : "Invalid file_extensions"
                })

                return response, 400
            
            response = jsonify({
                "status" : 'Unsuccessfull', 
                "message" : "Could not complete request"
            }), 422
        

        except Exception as e:
            cover_image = request.files['cover']
            if cover_image:
                if file_ext(cover_image.filename):
                    auth_user.cover_image = cover_image.read()
                    db.session.commit()
                    return jsonify({
                        "status" : "success",
                        "message" : "Cover photo uploaded sucessfully",
                    }), 201

                response = jsonify({
                    "status" : "unsuccessfull",
                    "message" : "Invalid file_extensions"
                })

                return response, 400

            return response, 400
        
    @app.route("/api/fetch_picture", methods = ['GET'])
    @jwt_required()
    def retrieve_picture():
        mime = magic.Magic(mime=True)
        userId = get_jwt_identity()
        auth_user = User.query.filter_by(_id = userId).first()
        if auth_user:
            images =  {}
            if auth_user.profile_image:
                images['profile'] = { "data" : base64.b64encode(auth_user.profile_image).decode('utf-8'), "mime" : mime.from_buffer(auth_user.profile_image) }
            if auth_user.cover_image:
                images['cover'] = { 'data' :  base64.b64encode(auth_user.cover_image).decode('utf-8'), "mime" : mime.from_buffer(auth_user.cover_image)}
            
            if images:
                return jsonify(images), 200
            
            return {
                "status" : "Unsucessfull", 
                "message" : "Images Unavailable"
            }, 400
        
        return {
                "status" : "Unsucessfull", 
                "message" : "Invalid user"
            }, 400

    @app.route("/api/remove_image", methods = ['POST'])
    @jwt_required()
    def delete_picture():
        user_id = get_jwt_identity()
        auth_user = User.query.filter_by(_id = user_id).first()
        print(request.json)
        if request.json['photo'] == 'cover':
            auth_user.cover_image = b''
            db.session.commit()
            return {
                "status" : "success", 
                "message" : "Deleted Cover Image"
            }, 201
        
        if request.json['photo'] == 'profile':
            auth_user.profile_image = b''
            db.session.commit()
            return {
                "status" : 'succes', 
                "message" : "Deleted Profile Image"
            }

        return {
            "status" : "Unsucessfull", 
            "message" : "Could not complete operation"
        }, 400
    