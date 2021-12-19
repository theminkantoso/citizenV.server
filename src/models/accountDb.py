from datetime import date
from src.models.cityProvinceDb import CityDb
from src.models.districtDb import DistrictDb
from src.models.wardDb import WardDb
from src.models.residentialGroupDb import GroupDb
from src.database import db


class AccountDb(db.Model):
    __tablename__ = 'account'
    accountId = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    email = db.Column(db.String)
    roleId = db.Column(db.Integer)  # ENUM: 0-Admin, 1-A1, 2-A2, 3-A3, 4-B1, 5-B2
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
        if isinstance(self.startTime, date):
            startTime_json = self.startTime.isoformat()
        else:
            startTime_json = ''
        if isinstance(self.endTime, date):
            endTime_json = self.endTime.isoformat()
        else:
            endTime_json = ''
        return {"accountId": self.accountId, "email": self.email, "roleId": self.roleId,
                "managerAccount": self.managerAccount, "startTime": startTime_json,
                "endTime": endTime_json, "isLocked": self.isLocked}

    @classmethod
    def json1(cls, acc, areaId):
        if acc is None:
            return {
                "areaId": areaId,
                "accountId": "",
                "email": "",
                "roleId": "",
                "managerAccount": "",
                "startTime": "",
                "endTime": "",
                "isLocked": ""
            }
        else:
            if isinstance(acc.startTime, date):
                startTime_json = acc.startTime.isoformat()
            else:
                startTime_json = ''
            if isinstance(acc.endTime, date):
                endTime_json = acc.endTime.isoformat()
            else:
                endTime_json = ''
            return {"areaId": areaId, "accountId": acc.accountId, "email": acc.email, "roleId": acc.roleId,
                    "managerAccount": acc.managerAccount, "startTime": startTime_json,
                    "endTime": endTime_json, "isLocked": acc.isLocked}

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
        cls.query.filter(cls.AccountId.like(search)).update({"isLocked": 1}, synchronize_session='fetch')
        db.session.commit()

    @classmethod
    def delete_managed_account_hierachy(cls, accId):
        search = "{}%".format(accId)
        cls.query.filter(cls.managerAccount.like(search)).delete(synchronize_session='fetch')
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
