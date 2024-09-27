import os


class Config:
    MONGO_URI = os.getenv('MONGO_URI')
    DEBUG=os.getenv("DEBUG") == 'True'
    APP_URL=os.getenv('APP_URL')
