# config.py
class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://flask_user:ssdpm@localhost/flask_app'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable unnecessary tracking overhead
    SECRET_KEY = 'your_secret_key'  # Set your own secret key for session management

