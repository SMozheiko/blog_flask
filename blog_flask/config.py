"""Application config module"""
from pathlib import Path


PATH = Path(__file__).resolve().parent


class Config:
    """Application config class"""
    SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    STATIC = f'{PATH}/static/profile_pictures'
