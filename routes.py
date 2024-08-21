import eventlet
eventlet.monkey_patch()
from flask import make_response, jsonify, request, render_template
from models import User, Posts, Comments, Likes, Friend
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token
import magic
import base64
from flask_jwt_extended import set_access_cookies, set_refresh_cookies, unset_access_cookies, unset_refresh_cookies
import random
from sqlalchemy import or_

def root_routes(app, db):
    hasher = Bcrypt()
    
    
    @app.route("/")
    def home():
        app.logger.info('Tring to complete request')
        return render_template('index.html')

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

    #profile/foreign enpoint 
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
    @jwt_required()
    def fetch_random():
        mime = magic.Magic(mime=True)
        universal_post = Posts.query.all()
        feeds_list = []
        prev_post = []
        if universal_post:
            for _ in range(0, 10) :
                selected_post = random.choice([items for items in universal_post if items != prev_post])
                prev_post = selected_post
                
                #check like status
                like_status = [False]
                for likes in selected_post.likes:
                    if get_jwt_identity() == likes.user_id:
                        like_status.clear()
                        like_status.append(True)
                    else:
                        like_status.clear()
                        like_status.append(False)
    
                new_post = {
                    "userId" : selected_post.user._id, 
                    "userName" : selected_post.user.user_name,
                    "likes" : len(selected_post.likes), 
                    "likeStatus" : like_status, 
                    "comments" : [{"content" : comment.content, "commentId" : comment.user_id, "userName" : comment.user.user_name} for comment in selected_post.comments],
                    'content' : selected_post.content, 
                    'postId' : selected_post._id
                }
                # if new_post not in feeds_list:
                feeds_list.append(new_post)
    
    
    
            return {
                'status' : 'sucessfull', 
                'message' : 'new feeds fetched sucessfully', 
                "data" : {
                    'feeds' : feeds_list
                } 
            }, 200

        else:
            return {
                'status' : 'unsucessfull', 
                'message' : 'No posts Unavailable', 
            }, 200

    @app.route("/api/fetch_comments/<postId>")
    @jwt_required(optional=True)
    def fetch_comments(postId):
        target_post = Posts.query.filter_by(_id = postId).first()
        if target_post:
            if target_post.comments:
                return {
                    'status' : "sucessfull", 
                    "message" : "Comments fetched sucessfully", 
                    'data' : {
                    "comments" : [{"content" : comment.content, "commentId" : comment.user_id, "userName" : comment.user.user_name} for comment in target_post.comments],
                    }
                }, 200

            return {
            'status' : "uncessfull",
            "message" : 'No comments for this posts', 
            'data' : {
                    "comments" : [],
                    }
            }, 200

        return {
        'status' : 'uncessfull',
        'message' : 'Invalid request',
        }, 400



    @app.route("/api/fetch_feeds/images/<userId>")
    # @jwt_required()
    def feeds_images(userId):
        mime = magic.Magic(mime=True)
        target_user = User.query.filter_by(_id = userId).first()
        if target_user:
            if target_user.profile_image:
                img = {"data" : base64.b64encode(target_user.profile_image).decode('utf-8'), "mime" : mime.from_buffer(target_user.profile_image)}
                return {
                    "status" : 'sucess', 
                    "message" : "fetched Imaege sucessfully",
                    "data" : {
                        "img" : img
                    }
                }, 200
            return {
                "status" : 'unsucessfull', 
                "message" : "User has no image",
            }, 200
        return {
            "status" : 'uncessfull',
            "message" : "Invalid User"
        }, 400
    
    #view full post
    @app.route("/api/view_post/<postId>")
    @jwt_required(optional=True)
    def get_post(postId):
        post = Posts.query.filter_by(_id = postId).first()
        like_status = [False]
        if get_jwt_identity():
            for likes in post.likes:
                if get_jwt_identity() == likes.user_id:
                    like_status.clear()
                    like_status.append(True)
                else:
                    like_status.clear()
                    like_status.append(False)
        return {
                "userName" : post.user.user_name,
                "userId" : post.user._id, 
                "content" : post.content,
                "date" : post.time_created, 
                "likes" : len(post.likes),
                "likeStatus" : like_status,
                "comments" : [{"comment" :comment.content, "userId" : comment.user_id, "userName" : comment.user.user_name} for comment in post.comments],
                "commentNo" : len([comment.content for comment in post.comments])
             }, 200

        
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
                                            "userName" : current_user.user_name, 
                                            "likes" : len(Posts.query.filter_by(_id = post._id).first().likes),
                                            "comments" : len(Posts.query.filter_by(_id = post._id).first().comments)
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
                                            "postLikes" : len(Posts.query.filter_by(_id = post._id).first().likes),
                                            "postComments" : len(Posts.query.filter_by(_id = post._id).first().comments)
                                            } 
                                    for post in list_posts]}
                            }, 200
            return {
                        "status" : "unsucessfull",
                        "message" : "Unable to get list of posts", 
                    }, 400

    #likes
    @app.route("/api/<postId>/likes", methods = ['POST'])
    @jwt_required()
    def add_like(postId):
        if request.method == 'POST':
            data = request.json
            current_user = User.query.filter_by(_id = get_jwt_identity()).first()
            target_post = Posts.query.filter_by(_id = postId).first()
            for likes in target_post.likes:
                if likes.user_id == current_user._id:
                    return {
                        'status' : "success", 
                        'message' : "Already  Liked"
                    }, 200
            
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
            'status' : "unsucessfull", 
            'message' : "Invalid"
        }, 400
    
    #comments
    @app.route("/api/<postId>/comment", methods = ['POST'])
    @jwt_required()
    def handle_comment(postId):
        if request.method == 'POST': 
            data = request.json
            current_user = User.query.filter_by(_id = get_jwt_identity()).first()
            target_post = Posts.query.filter_by(_id = postId).first()
            if current_user and target_post:
                new_comment = Comments(content=data['content'], user=current_user, postId=postId)
                db.session.add(new_comment)
                db.session.commit()
                return {
                    "status" : "success",
                    "message" : "Comment uploaded sucessfully",
                    "data" : {
                        "postId" : postId,
                        "postContent" : target_post.content
                    }
                }, 201
            return {
                        "status" : "unsucessfull",
                        "message" : "Invalid User/post credentials", 
                    }, 400


    #fileext
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
        
    #auth user endpoint for pictures
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
            
            return jsonify(images), 200
        
        return {
                "status" : "Unsucessfull", 
                "message" : "Invalid user"
            }, 400

    #foerign user enpoint for pictures
    @app.route("/api/fetch_picture/<user_id>", methods = ['GET'])
    @jwt_required()
    def retrieve_forieign_picture(user_id):
        mime = magic.Magic(mime=True)
        userId = user_id
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

    @app.route("/api/delete_post/<postId>")    
    @jwt_required()
    def delete_post(postId):
        if postId:
            target_post = Posts.query.filter_by(_id = postId).first()
            db.session.delete(target_post)
            db.session.commit()

            return {
            "status" : "sucess", 
            "message" : "Post removed sucessfully"
            }, 200

        return {
            "status" : "uncessfull", 
            "message" : "Unable to complete request"
        }, 400


    @app.route("/api/add_friend", methods = ['POST', 'GET'])
    @jwt_required()
    def add_friend():
        if request.method == 'POST':
            data = request.json
            target_id = data['targetId']
            auth_user = User.query.filter_by(_id = get_jwt_identity()).first()
            target_user = User.query.filter_by(_id = target_id).first()
            friend_list = Friend.query.filter(
                or_(auth_user._id == Friend.user_one_id, auth_user._id == Friend.user_two_id)
                ).all()

            # return "sdfsfd"
    
            for friends in friend_list:
                if friends.user_one_id == auth_user._id and friends.user_two_id == target_user._id or friends.user_one_id == target_user._id and friends.user_two_id == auth_user._id:
                    return {
                            'status' : 'sucessfull',
                            'message' : 'Friend Relationship already established'
                            }, 200

            for relations in auth_user.friend_user_one:
                if relations.user_one_id == target_user._id or relations.user_two_id == target_user._id:
                    return {
                        'status' : 'sucessfull',
                        'message' : 'Friend Relationship already established'
                        }, 200
    
            if auth_user and target_user:
                friend_relation = Friend(auth_user._id, target_user._id)
                auth_user.friend_user_one.append(friend_relation)
                target_user.friend_user_two.append(friend_relation)
                friend_relation.user_one_id = auth_user._id
                friend_relation.user_two_id = target_user._id
                db.session.add(friend_relation)
                db.session.commit()
    
                return {
                    'status' : 'sucessfull',
                    'message' : 'New Friend Created'
                }, 201

        return {
            'status' : 'sucessfull',
            'message' : 'Invalid request'
        }, 400



    @app.route("/api/verify_friend/<userId>")
    @jwt_required()
    def verify_friend(userId):
        auth_user = User.query.filter_by(_id = get_jwt_identity()).first()
        target_user = User.query.filter_by(_id = userId).first()
        friend_list = Friend.query.all()

        for friends in friend_list:
            if friends.user_one_id == auth_user._id and friends.user_two_id == target_user._id or friends.user_one_id == target_user._id and friends.user_two_id == auth_user._id:
                return {
                        'status' : 'sucessfull',
                        'message' : 'Friend Relationship already established',
                            "data" : {
                                'status' : True
                            }
                        }, 200
        return {
            'status'  : 'sucessfull',
            'message' : 'No friend Relationship', 
            "data" : {
                        'status' : False
                }
        }, 200



    @app.route("/api/unfollow_friend/<userId>")
    @jwt_required()
    def unfollow_friend(userId):
        if request.method == 'GET':
            auth_user = User.query.filter_by(_id = get_jwt_identity()).first()
            target_user = User.query.filter_by(_id = userId).first()
            friend_list = Friend.query.filter(
                    or_(userId == Friend.user_one_id or userId == Friend.user_two_id)
                ).all()

            for friends in friend_list:
                if friends.user_one_id == get_jwt_identity() or friends.user_two_id == get_jwt_identity():
                    db.session.delete(friends)
                    db.session.commit()

                    return {
                    'status' : "sucess", 
                    'message' : 'Sucessfully removed friend Relationship', 
                    "data" : {
                        'status' : False
                        }
                    }, 200

            return {
            'status' : 'uncessfull',
            'message' : 'Invalid Request'
            }, 400



    @app.route("/api/friends_list")
    @jwt_required()
    def handle_friends():
        auth_user = User.query.filter_by(_id = get_jwt_identity()).first()

        get_friend_list = Friend.query.filter(
            or_(Friend.user_one_id == get_jwt_identity(), Friend.user_two_id == get_jwt_identity())
            ).all()

        if auth_user:
            friend_list = [
                    {
                     'id' : friends.user_two_id if friends.user_one_id == get_jwt_identity() else friends.user_one_id,
                     'userName' : friends.user_two.user_name if friends.user_one_id == get_jwt_identity() else friends.user_one.user_name,
                     'relation_id' : friends._id,
                    } 
                    for friends in get_friend_list]

            response = {
                'status' : 'sucess', 
                'message' : 'Fetched friends sucessfully', 
                'data' : {
                    'friendList' : friend_list, 
                }
            }

        return response, 200

    @app.route("/api/fetch_messages/<relation_id>")
    @jwt_required()
    def handle_messages(relation_id):
        auth_user = User.query.filter_by(_id = get_jwt_identity()).first()
        friend_relation = Friend.query.filter_by(_id = relation_id).first()
        if len(friend_relation.room) > 0: 
            message = friend_relation.room[0].message
        # print(message)
        # print(friend_relation.room[0].message)
        # message = Message.query.filter(
        #     or_(Message.user_id == get_jwt_identity(), Message.user_id == foreign_user_id)
        #     ).all()

           # for sms in message:
           #  if len(new_message) > 2:
           #      break
           #  new_message.append(sms)



            if not message:
                return {
                'status' : 'uncessfull', 
                'message' : 'No past messages', 
                "data" : {
                    'messageList' : []
                }
                }

            if message:
                message = [
                    {
                    'day' : sms.day, 
                    'time' : sms.time_created,
                    'roomId' : sms.room_id, 
                    'userId' : sms.user_id, 
                    "content" : sms.content,
                    "userName" : User.query.filter_by(_id = sms.user_id).first().user_name
                     }
                    for sms in message 
                ]

                # message.reverse()

                response = {
                    'status' : 'sucess',
                    'message' : 'Fetched message sucessfull',
                    'data' : {
                        'messageList' : message
                    }
                }

                return response, 200

        return {
                    'status' : 'unsucessfull',
                    'message' : 'Fetched message sucessfull',
                    'data' : {
                        'messageList' : []
                    }
                }