from datetime import date
from src.database import db


class AccountDb(db.Model):
    __tablename__ = 'account'
    accountId = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    email = db.Column(db.String)
    roleId = db.Column(db.Integer)  # ENUM: 0-Admin, 1-A1, 2-A2, 3-A3, 4-B1, 5-B2
    managerAccount = db.Column(db.String)
    startDate = db.Column(db.Date)
    endDate = db.Column(db.Date)
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
        if isinstance(self.startDate, date):
            startDate_json = self.startDate.isoformat()
        else:
            startDate_json = ''
        if isinstance(self.endDate, date):
            endDate_json = self.endDate.isoformat()
        else:
            endDate_json = ''
        return {"accountId": self.accountId, "email": self.email, "roleId": self.roleId,
                "managerAccount": self.managerAccount, "startDate": startDate_json,
                "endDate": endDate_json, "isLocked": self.isLocked}

    @classmethod
    def json1(cls, acc, areaId):
        if acc is None:
            return {
                "areaId": areaId,
                "accountId": "",
                "email": "",
                "roleId": "",
                "managerAccount": "",
                "startDate": "",
                "endDate": "",
                "isLocked": None
            }
        else:
            if isinstance(acc.startDate, date):
                startDate_json = acc.startDate.isoformat()
            else:
                startDate_json = ''
            if isinstance(acc.endDate, date):
                endDate_json = acc.endDate.isoformat()
            else:
                endDate_json = ''
            return {"areaId": areaId, "accountId": acc.accountId, "email": acc.email, "roleId": acc.roleId,
                    "managerAccount": acc.managerAccount, "startDate": startDate_json,
                    "endDate": endDate_json, "isLocked": acc.isLocked}

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
        cls.query.filter(cls.managerAccount.like(search)). \
            update({"isLocked": 1, "startDate": None, "endDate": None}, synchronize_session='fetch')
        db.session.commit()

    @classmethod
    def delete_managed_account_hierachy(cls, accId):
        search = "{}%".format(accId)
        cls.query.filter(cls.managerAccount.like(search)).delete(synchronize_session='fetch')
        db.session.commit()

    @staticmethod
    def get_email_user_manager(id_manager, id_in):
        return db.session.query(AccountDb.email).filter(AccountDb.managerAccount == id_manager). \
            filter(AccountDb.accountId == id_in).first()

    # @classmethod
    # def delete_managed_account_hierachy_2(cls, accId):
    #     search = "{}%".format(accId)
    #     print(cls.query.filter(cls.managerAccount.like(search)).count().group_by(accId))

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
