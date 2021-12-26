from datetime import timedelta
import os

SQLALCHEMY_DATABASE_URI = 'mysql://root:''@localhost/citizenv'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_POOL_SIZE = 1000   # Để tạm là 300 -> setTimeOutError sqlachemy
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USERNAME = os.environ.get('MAIL')
MAIL_PASSWORD = os.environ.get('PASS')
MAIL_USE_TLS = True
MAIL_USE_SSL = False
#USE_CREDENTIALS = True
JWT_SECRET_KEY = "JWT" # khóa riêng của server
PROPAGATE_EXCEPTIONS = True
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
