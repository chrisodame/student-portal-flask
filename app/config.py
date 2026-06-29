import os

class Config:
    SECRET_KEY = "change-this-to-a-long-random-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///student.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False