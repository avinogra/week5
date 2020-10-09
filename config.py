import os

class Config:
    DEBUG = True
    SECRET_KEY= "secret_key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_SECRET_KEY= "secretkey"



