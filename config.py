import os

from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class AppConfig: 

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    JWT_SECRET_KEY = os.getenv("SECRET_KEY")      ##Change this secret key
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=20000)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=20000)
    JWT_TOKEN_LOCATION = ['cookies']  
    JWT_COOKIE_SAMESITE = 'Strict'  
    JWT_CSRF_IN_COOKIES = False
    JWT_COOKIE_SECURE = True    
    JWT_COOKIE_HTTPONLY = True
    JWT_CSRF_IN_COOKIES = False
    JWT_COOKIE_CSRF_PROTECT = False 