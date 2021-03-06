from src.database import db
from src.models.accountDb import AccountDb


class WardDb(db.Model):
    __tablename__ = 'ward'
    wardId = db.Column(db.String(6), primary_key=True)
    wardName = db.Column(db.String(30))
    districtId = db.Column(db.String(4), db.ForeignKey("district.districtId"))
    completed = db.Column(db.Boolean)

    def __init__(self, wardId, wardName, districtId, completed):
        self.wardId = wardId
        self.wardName = wardName
        self.districtId = districtId
        self.completed = completed

    def json(self):
        return {
            "wardId": self.wardId,
            "wardName": self.wardName,
            "districtId": self.districtId,
            "completed": self.completed
        }

    def json1(self):
        return {
            "Name": self.wardName,
            "Id": self.wardId
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(wardName=name).first()

    @classmethod
    def find_by_id(cls, Id):
        return cls.query.filter_by(wardId=Id).first()

    @classmethod
    def find_by_district_id(cls, Id):
        return cls.query.filter_by(districtId=Id).all()

    @classmethod
    def find_by_dist_ward_name(cls, dist_id, ward_name):
        return cls.query.filter_by(districtId=dist_id, wardName=ward_name).first()

    @staticmethod
    def find_join_account(id):
        return db.session.query(WardDb.wardId, WardDb.wardName, WardDb.completed,
                                AccountDb.endDate).select_from(WardDb).\
            join(AccountDb, WardDb.wardId == AccountDb.accountId).filter(WardDb.districtId == id).all()

    @staticmethod
    def find_join_account_allocated(id):
        return db.session.query(WardDb.wardId, WardDb.wardName, WardDb.completed,
                                AccountDb.endDate).select_from(WardDb). \
            join(AccountDb, WardDb.wardId == AccountDb.accountId).filter(WardDb.districtId == id).count()

    @staticmethod
    def find_join_account_specific(id_acc, id_request):
        return db.session.query(WardDb.wardId, WardDb.wardName, WardDb.completed,
                                AccountDb.endDate).select_from(WardDb).\
            join(AccountDb, WardDb.wardId == AccountDb.accountId).filter(WardDb.districtId == id_acc).\
            filter(WardDb.wardId == id_request).first()

    @classmethod
    def count_completed(cls, id_district):
        return cls.query.filter_by(districtId=id_district).filter_by(completed=True).count()

    @classmethod
    def count_total(cls, id_district):
        return cls.query.filter_by(districtId=id_district).count()

    @classmethod
    def join_areaId(cls):
        query = db.session.query(WardDb, AccountDb) \
            .outerjoin(AccountDb, AccountDb.accountId == WardDb.wardId).all()
        return query
    @staticmethod
    def find_ward_name(id):
        return db.session.query(WardDb.wardName).filter_by(wardId=id).first()

    @classmethod
    def check_exist(cls, id):
        return cls.query.filter_by(wardId=id).count()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
