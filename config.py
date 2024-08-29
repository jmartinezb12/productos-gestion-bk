import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:123456@db:5432/postgres')
    SQLALCHEMY_TRACK_MODIFICATIONS = False