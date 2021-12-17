from datetime import timedelta

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USERNAME = "bbsgb"
MAIL_PASSWORD = "sfbgb"
MAIL_USE_TLS = True
MAIL_USE_SSL = False
#USE_CREDENTIALS = True
JWT_SECRET_KEY = "JWT"  # khóa riêng của server
PROPAGATE_EXCEPTIONS = True
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']