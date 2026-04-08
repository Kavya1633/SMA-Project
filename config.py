import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # App settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')

    # Database
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/sma_db')

    DEBUG = True