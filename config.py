class Config:
    SECRET_KEY = "your_secret_key"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:administrator@localhost/db_skingenie"
    SQLALCHEMY_TRACK_MODIFICATIONS = False