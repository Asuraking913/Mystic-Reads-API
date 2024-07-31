import os

from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class AppConfig: 

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    JWT_SECRET_KEY = os.getenv("SECRET_KEY")      ##Change this secret key
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=2000)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(seconds=2000)
    JWT_TOKEN_LOCATION = ['cookies']  
    JWT_COOKIE_SAMESITE = 'Lax'  
    JWT_CSRF_IN_COOKIES = False
    JWT_COOKIE_SECURE = True    
    JWT_COOKIE_HTTPONLY = True