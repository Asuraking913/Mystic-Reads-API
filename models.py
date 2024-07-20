from app import db
from uuid import uuid4

def create_id(): 
    return uuid4().hex

class User(db.Model):
    id = db.Column(db.String(255), unique = True, nullable = False, primary_key = True, default = create_id)
    user_name = db.Column(db.String(255), unique = True, nullable = False)
    user_email = db.Column(db.String(255), unique = True, nullable = False)
    user_pass = db.Column(db.String(255), nullable = False)
 