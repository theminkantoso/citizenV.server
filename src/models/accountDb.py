from src.database import db
from werkzeug.security import generate_password_hash, check_password_hash


class AccountDb(db.Model):
    __tablename__ = 'account'
    accountId = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String)
    email = db.Column(db.String)
    roleId = db.Column(db.Integer)
    managerAccount = db.Column(db.Integer, db.ForeignKey('account.accountId'))
    startTime = db.Column(db.Date)
    endTime = db.Column(db.Date)
    isLocked = db.Column(db.Integer)

    def __init__(self, AccountId, email, Password, RoleId, managerAccount, startTime, endTime, isLocked):
        self.accountId = AccountId
        self.email = email
        self.password = Password
        self.roleId = RoleId
        self.managerAccount = managerAccount
        self.startTime = startTime
        self.endTime = endTime
        self.isLocked = isLocked

    def __init__(self, email, Password, createdAt):

        self.email = email
        self.password = Password
        self.CreateAt = createdAt


    @classmethod
    def find_account(cls, accId, passWord):
        return cls.query.filter_by(accountId=accId, password=passWord).first()

    @classmethod
    def find_by_email(cls, email, accId):
        return cls.query.filter_by(email=email, accountId=accId).first()

    @classmethod
    def find_by_id(cls, accId):
        return cls.query.filter_by(accountId=accId).first()

    @classmethod
    def check_password(cls, password, accId):
        user = cls.query.filter_by(accoundId=accId).first()
        return check_password_hash(user.password, password)

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
