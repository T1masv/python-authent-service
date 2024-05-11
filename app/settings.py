import os

class Config:
    HOST = os.environ.get('DB_HOST', 'mongodb://localhost:27017/mydatabase')
    USERNAME = os.environ.get('DB_USERNAME', 'admin')
    PASSWORD = os.environ.get('DB_PASSWORD', '<PASSWORD>')
    PORT = os.environ.get('DB_PORT', '27017')
    DB_NAME = os.environ.get('DB_NAME', 'mydatabase')



class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False