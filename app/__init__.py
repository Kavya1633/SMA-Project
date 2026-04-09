from flask import Flask
from flask_pymongo import PyMongo

# Login Manager use to manage user login in and session details
from flask_login import LoginManager

from config import Config

mongo=PyMongo()

login_manager=LoginManager()

def create_app():
    app=Flask(__name__)
    app.config.from_object(Config)
    
    # connect Mongodb to the app
    mongo.init_app(app)
    
    # connect login manager to the app
    login_manager.init_app(app)
    
    login_manager.login_view='auth.login'
    
    login_manager.login_message='Please log in to access this page.'
    
    from app.auth import auth_bp
    app.register_blueprint(auth_bp)
    
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    with app.app_context():
        from app import models
    
    return app
    



