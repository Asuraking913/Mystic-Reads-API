from extensions import db
from uuid import uuid4
from datetime import datetime

def create_id(): 
    return uuid4().hex

def return_current_date():
    month = ['january', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December' ]
    day = datetime.now().day
    month_index = datetime.now().month
    year = datetime.now().year
    return f"{month[month_index - 1]}, {day}, {year}"

def return_current_time():
    now = datetime.now()
    formatted_time = now.strftime("%I:%M %p")  # %I for 12-hour format, %p for AM/PM
    return formatted_time



class User(db.Model):
    _id = db.Column(db.String(255), unique = True, nullable = False, primary_key = True, default = create_id)
    user_name = db.Column(db.String(255), unique = True, nullable = False)
    user_email = db.Column(db.String(255), unique = True, nullable = False)
    user_pass = db.Column(db.String(255), nullable = False)
    joined = db.Column(db.String(30), nullable = False, default = return_current_date)
    birthday = db.Column(db.String(45))
    gender = db.Column(db.String(20))
    bio = db.Column(db.String(345))
    current_location = db.Column(db.String(255))

    #Post and like relationship
    post = db.relationship('Posts', backref = 'user')
    likes = db.relationship('Likes', backref = 'user')
    comments = db.relationship('Comments', backref = 'user')


    #room/friends and message relationships
    room_user_one = db.relationship('Room', foreign_keys ='Room.user_one_id', back_populates = 'user_one')
    room_user_two = db.relationship('Room', foreign_keys='Room.user_two_id', back_populates = 'user_two')
    message_user_one = db.relationship('Message', backref = 'user')
    friend_user_one = db.relationship('Friend', foreign_keys='Friend.user_one_id',back_populates = 'user_one')
    friend_user_two = db.relationship('Friend', foreign_keys='Friend.user_two_id',back_populates = 'user_two')

    #images
    profile_image = db.Column(db.LargeBinary)
    cover_image = db.Column(db.LargeBinary)

    
    def __init__(self, name, email, gender, pass_w):
        self.user_name = name
        self.user_email = email
        self.user_pass = pass_w
        self.gender = gender

    def __repr___(self):
        return f'This object has a name: {self.user_name} and email: {self.user_email}'
    
class Posts(db.Model):
    _id = db.Column(db.String(255), unique = True, nullable = False, primary_key = True, default = create_id)
    content = db.Column(db.String(10000), nullable = False)
    time_created = db.Column(db.String(30), nullable = False, default = return_current_date)
    user_id = db.Column(db.String(255), db.ForeignKey('user._id'))
    likes = db.relationship('Likes', backref = 'post')
    comments = db.relationship('Comments', backref = 'posts')

    def __init__(self, content, user):
        self.content = content
        self.user = user
    
class Likes(db.Model):
    _id = db.Column(db.String(255), unique = True, nullable = False, primary_key = True, default = create_id)
    user_id = db.Column(db.String(255), db.ForeignKey('user._id'))
    post_id = db.Column(db.String(255), db.ForeignKey('posts._id'))

    def __init__(self, user, post):
        self.user = user
        self.post = post

class Comments(db.Model):
    _id = db.Column(db.String(255), unique = True, nullable = False, primary_key = True, default = create_id)
    content = db.Column(db.String(345), nullable = False)
    user_id = db.Column(db.String(255), db.ForeignKey('user._id'))
    post_id = db.Column(db.String(255), db.ForeignKey('posts._id'))

    def __init__(self, content, user, postId): 
        self.user = user
        self.post_id = postId
        self.content = content

# class Image(db.Model):
#     _id = db.Column(db.String(255), unique = True, nullable = False, primary_key = True, default = create_id)
#     file_name = db.Column(db.String(40), nullable = False)
#     data = db.Column(db.LargeBinary, nullable = False)

#     def __repr__(self):
#         return f"Image {self.file_name}"

class Friend(db.Model):
    _id = db.Column(db.String(255), unique = True, nullable = False, primary_key = True, default = create_id)
    user_one_id = db.Column(db.String(255), db.ForeignKey('user._id'))
    user_two_id = db.Column(db.String(255), db.ForeignKey('user._id'))

    user_one = db.relationship('User', foreign_keys = [user_one_id], back_populates='friend_user_one')
    user_two = db.relationship('User', foreign_keys = [user_two_id], back_populates='friend_user_two')
    room_id = db.relationship('Room', backref = 'friend')

    def __init__(self, user_one, user_two, roomId):
        self.user_one_id = user_one
        self.user_two_id = user_two
        self.room_id = rommId

    def __repr__(self):
        return f"User:{self.user_one_id} and {self.user_two_id} are friends"
    
class Room(db.Model):
    _id = db.Column(db.String(255), unique = True, nullable = False, primary_key = True, default = create_id)
    user_one_id = db.Column(db.String(255), db.ForeignKey('user._id'))
    user_two_id = db.Column(db.String(255), db.ForeignKey('user._id'))
    message = db.relationship('Message', backref='room')
    day = db.Column(db.String(20), nullable = False, default = return_current_date)
    time_created = db.Column(db.String(40), nullable = False, default = return_current_time)
    friend_relation_id = db.Column(db.String(255), db.ForeignKey('friend._id'))

    user_one = db.relationship('User', foreign_keys = [user_one_id], back_populates='room_user_one')
    user_two = db.relationship('User', foreign_keys = [user_two_id], back_populates='room_user_two')

    def __init__(self, user_one, user_two, friend_id):
        self.user_one_id = user_one
        self.user_two_id = user_two
        self.friend_relation_id = friend_id


class Message(db.Model):
    _id = db.Column(db.String(255), unique = True, nullable = False, primary_key = True, default = create_id)
    content = db.Column(db.String(500), unique = True, nullable = False)
    user_id = db.Column(db.String(255), db.ForeignKey('user._id'))
    room_id = db.Column(db.String(255), db.ForeignKey('room._id'))
    day = db.Column(db.String(20), nullable = False, default = return_current_date)
    time_created = db.Column(db.String(40), nullable = False, default = return_current_time)

    def __init__(self, user_id, content, room):
        self.user_id = user_one
        self.content = content
        self.room_id = room

    
