from flask import Flask
from flask_pymongo import PyMongo

from config import Config

mongo = PyMongo()

def create_app():
    
    
    app = Flask(__name__)
  
    app.config.from_object(Config)
  
    # This establishes the actual connection to MongoDB
    mongo.init_app(app)
  
    # auth_bp handles login/logout
    from app.auth import auth_bp
   
    app.register_blueprint(auth_bp)
    from app.routes import main_bp
    
    app.register_blueprint(main_bp)
    
    return app