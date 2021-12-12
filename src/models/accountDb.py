import datetime
from src.database import db


class AccountDb(db.Model):
    __tablename__ = 'account'
    accountId = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    email = db.Column(db.String)
    roleId = db.Column(db.Integer)
    managerAccount = db.Column(db.String)
    startTime = db.Column(db.Date)
    endTime = db.Column(db.Date)
    isLocked = db.Column(db.Boolean)

    # def __init__(self, AccountId, email, Password, RoleId, managerAccount, startTime, endTime, isLocked):
    #     self.accountId = AccountId
    #     self.email = email
    #     self.password = Password
    #     self.roleId = RoleId
    #     self.managerAccount = managerAccount
    #     self.startTime = startTime
    #     self.endTime = endTime
    #     self.isLocked = isLocked

    def __init__(self, AccountId, Password, email, RoleId, manager_account, isLocked):
        self.accountId = AccountId
        self.password = Password
        self.email = email
        self.roleId = RoleId
        self.managerAccount = manager_account
        self.isLocked = isLocked

    def json(self):
        return {"accountId": self.accountId, "password": self.password, "email": self.email, "roleId": self.roleId,
                "managerAccount": self.managerAccount, "startTime": self.startTime.strftime("%Y-%m-%d"),
                "endTime": self.endTime.strftime("%Y-%m-%d"), "isLocked": self.isLocked}

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
    def find_managed_account_by_id(cls, accId):
        return cls.query.filter_by(managerAccount=accId).all()

    @classmethod
    def lock_managed_account_hierachy(cls, accId):
        search = "{}%".format(accId)
        db.session.query.filter(cls.managerAccount.like(search)).update({"isLocked": 1})
        db.session.commit()

    @classmethod
    def delete_managed_account_hierachy(cls, accId):
        search = "{}%".format(accId)
        db.session.query.filter(cls.managerAccount.like(search)).delete()
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def commit_to_db(self):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


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
