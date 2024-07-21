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
    post = db.relationship('Posts', backref = 'user')
    likes = db.relationship('Likes', backref = 'user')
    comments = db.relationship('Comments', backref = 'user')
    
 
    def __init__(self, name, email, pass_w):
        self.user_name = name
        self.user_email = email
        self.user_pass = pass_w

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
    user_id = db.Column(db.String(255), db.ForeignKey('user._id'))
    post_id = db.Column(db.String(255), db.ForeignKey('posts._id'))