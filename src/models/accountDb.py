from src.database import db
from werkzeug.security import generate_password_hash, check_password_hash

class AccountDb(db.Model):
    __tablename__ = 'accounttest'
    AccountId = db.Column(db.Integer, primary_key=True, autoincrement= True)
    # displayName = db.Column(db.String(50))
    email = db.Column(db.String(100))
    Password = db.Column(db.String)
    RoleId = db.Column(db.Integer)
    isActivated = db.Column(db.Boolean(), nullable=False, server_default='0')
    confirmedAt = db.Column(db.DateTime)
    GoogleId = db.Column(db.String(50))
    CreateAt = db.Column(db.DateTime)
    UpdateAt = db.Column(db.TIMESTAMP)

    def __init__(self, AccountId, email, Password, RoleId,
                 isActivated, confirmedAt,
                GoogleId, CreateAt, UpdateAt,
                ):
        self.AccountId = AccountId
        self.email = email
        self.Password = Password
        self.RoleId = RoleId
        self.isActivated = isActivated
        self.confirmedAt = confirmedAt
        self.GoogleId = GoogleId
        self.CreateAt = CreateAt
        self.UpdateAt = UpdateAt

    def __init__(self, email, Password, createdAt):

        self.email = email
        self.Password = Password
        self.CreateAt = createdAt


    @classmethod
    def find_account(cls, mail, passWord):
        return cls.query.filter_by(email=mail, Password=passWord).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def check_password(cls, password, email):
        user = cls.query.filter_by(email=email).first()
        return check_password_hash(user.Password, password)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def commit_to_db(self):
        db.session.commit()
    #
    # def delete_from_db(self):
    #     db.session.delete(self)
    #     db.session.commit()


class RevokedTokenModel(db.Model):
    """
    Revoked Token Model Class
    """

    __tablename__ = 'revoked_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    jti = db.Column(db.String(120))

    """
    Save Token in DB
    """

    def add(self):
        db.session.add(self)

        db.session.commit()

    """
    Checking that token is blacklisted
    """

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()

        return bool(query)
