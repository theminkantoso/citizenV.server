from flask_mail import Mail
my_mail = Mail()


def init_app(app):
    my_mail.init_app(app)