from flask_jwt_extended import JWTManager
jwt_manager = JWTManager()


def init_app(app):
    jwt_manager.init_app(app)