import os
from decouple import config

base_dir = os.path.abspath(os.path.dirname(__file__))


class Config:

    SECRET_KEY = config("SECRET_KEY_FLASK") or 'secret-key'
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(base_dir, 'app.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = config('MAIL_SERVER')
    MAIL_PORT = int(config('MAIL_PORT') or 25)
    MAIL_USE_TLS = config('MAIL_USE_TLS', default=None) is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']
