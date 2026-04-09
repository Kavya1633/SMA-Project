# This describes the structure of data we store in db

from flask_login import UserMixin

from app import mongo, login_manager

class User(UserMixin):
    # UserMixin features: is_authenticated, is_active, is_anonymous, get_id()
    
    def __init__(self, user_data):
        
        self.id=str(user_data['_id'])
        
        self.username=user_data['username']
        self.email=user_data['email']
        self.password=user_data['password']
        

@login_manager.user_loader

def load_user(user_id):
    from bson.objectid import ObjectId
    
    # find the user details from the db
    user_data=mongo.db.users.find_one({'_id': ObjectId(user_id)})
    
    # if user exit in db return user object
    if user_data:
        return User(user_data)
    
    return None
    
        