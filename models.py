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
    post = db.relationship('Posts', backref = 'user')
    likes = db.relationship('Likes', backref = 'user')
    comments = db.relationship('Comments', backref = 'user')
    # friends = db.relationship('FriendList', backref = 'user')
    profile_image = db.Column(db.LargeBinary)
    cover_image = db.Column(db.LargeBinary)

# class FriendList(db.Model):
#     _id = db.Column(db.String(255), unique = True, nullable = False, primary_key = True, default = create_id)
#     user_id = db.Column(db.String(255), db.ForeignKey('user._id'))
#     friend_id = db.Column(db.String(255), db.ForeignKey('user._id'))
    
    
 
    def __init__(self, name, email, gender, pass_w):
        self.user_name = name
        self.user_email = email
        self.user_pass = pass_w
        self.gender = gender

    def __repr___(self):
        return f'This object has a name: {self.user_name} and email: {self.user_email}'
    
class Posts(db.Model):
    _id = db.Column(db.String(255), unique = True, nullable = False, primary_key = True, default = create_id)
    content = db.Column(db.String(455), nullable = False)
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

    def __init__(self, content, user, post): 
        self.user = user
        self.post = post
        self.content = content

class Image(db.Model):
    _id = db.Column(db.String(255), unique = True, nullable = False, primary_key = True, default = create_id)
    file_name = db.Column(db.String(40), nullable = False)
    data = db.Column(db.LargeBinary, nullable = False)

    def __repr__(self):
        return f"Image {self.file_name}"
    
class Room(db.Model):
    _id = db.Column(db.String(255), unique = True, nullable = False, primary_key = True, default = create_id)
    user_one_id = db.Column(db.String(255), db.ForeignKey('user._id'))
    user_two_id = db.Column(db.String(255), db.ForeignKey('user._id'))
    message = db.relationship('Messages', backref='room')

class Messages(db.Model):
    _id = db.Column(db.String(255), unique = True, nullable = False, primary_key = True, default = create_id)
    content = db.Column(db.String(500), unique = True, nullable = False)
    user_one_id = db.Column(db.String(255), db.ForeignKey('user._id'))
    user_two_id = db.Column(db.String(255), db.ForeignKey('user._id'))
    room_id = db.Column(db.String(255), db.ForeignKey('room._id'))

    def __init__(self, content, room):
        self.content = content
        self.room = room

    
