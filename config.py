# from app import load_env
import os
from dotenv import load_dotenv

load_dotenv()

class AppConfig: 

    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')