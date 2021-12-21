from datetime import date

from src.database import db
from src.models.accountDb import AccountDb


class GroupDb(db.Model):
    __tablename__ = 'residentialgroup'
    groupId = db.Column(db.String(8), primary_key=True)
    groupName = db.Column(db.String(30))
    wardId = db.Column(db.String(6), db.ForeignKey("ward.wardId"))

    def __init__(self, groupId, groupName, wardId):
        self.groupId = groupId
        self.groupName = groupName
        self.wardId = wardId

    def json(self):
        return {
            "groupId": self.groupId,
            "groupName": self.groupName,
            "wardId": self.wardId
        }

    def json1(self, sum_citizen, endTime):
        if endTime is None:
            endTime = ""
        elif isinstance(endTime, date):
            endTime = endTime.isoformat()
        return {
            "id": self.groupId,
            "name": self.groupName,
            "endTime": endTime,
            "sumCitizen": sum_citizen
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(groupName=name).first()

    @classmethod
    def find_by_id(cls, group_id):
        return cls.query.filter_by(groupId=group_id).first()

    @classmethod
    def find_by_ward_id(cls, ward_id):
        return cls.query.filter_by(wardId=ward_id).all()

    @classmethod
    def find_by_ward_group_name(cls, ward_id, group_name):
        return cls.query.filter_by(wardId=ward_id, groupName=group_name).first()

    @classmethod
    def join_areaId(cls):
        query = db.session.query(GroupDb, AccountDb) \
            .outerjoin(AccountDb, AccountDb.accountId == GroupDb.groupId).all()
        return query

    @classmethod
    def find_join_account_specific(cls, id_acc, id_group):
        return db.session.query(GroupDb.groupId, GroupDb.groupName,\
                                AccountDb.endDate).select_from(GroupDb). \
            join(AccountDb, GroupDb.groupId == AccountDb.accountId).filter(GroupDb.wardId == id_acc). \
            filter(GroupDb.groupId == id_group).first()

    @staticmethod
    def find_join_account(id):
        return db.session.query(GroupDb.groupId, GroupDb.groupName,
                                AccountDb.endDate).select_from(GroupDb). \
            join(AccountDb, GroupDb.groupId == AccountDb.accountId).filter(GroupDb.wardId == id).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
