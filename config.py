import os
from decouple import config

base_dir = os.path.abspath(os.path.dirname(__file__))


class Config:

    SECRET_KEY = config("SECRET_KEY_FLASK") or 'secret-key'
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(base_dir, 'app.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
