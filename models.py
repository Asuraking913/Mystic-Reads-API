from extensions import db
from uuid import uuid4

def create_id(): 
    return uuid4().hex

class User(db.Model):
    _id = db.Column(db.String(255), unique = True, nullable = False, primary_key = True, default = create_id)
    user_name = db.Column(db.String(255), unique = True, nullable = False)
    user_email = db.Column(db.String(255), unique = True, nullable = False)
    user_pass = db.Column(db.String(255), nullable = False)
 
    def __init__(self, name, email, pass_w):
        self.user_name = name
        self.user_email = email
        self.user_pass = pass_w

    def __repr___(self):
        return f'This object has a name: {self.user_name} and email: {self.user_email}'