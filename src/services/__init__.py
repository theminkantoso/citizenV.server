from flask_mail import Mail
from flask_jwt_extended import JWTManager
my_mail = Mail()
jwt_manager = JWTManager()


def init_app(app):
    my_mail.init_app(app)
    jwt_manager.init_app(app)