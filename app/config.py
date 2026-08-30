import os


class Config:

    SECRET_KEY = "change-this-to-a-long-random-secret-key"

    SQLALCHEMY_DATABASE_URI = "sqlite:///student.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")

    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2 MB