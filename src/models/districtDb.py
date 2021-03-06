from src.database import db
from src.models.accountDb import AccountDb


class DistrictDb(db.Model):
    __tablename__ = 'district'
    districtId = db.Column(db.String(4), primary_key=True)
    districtName = db.Column(db.String(30))
    cityProvinceId = db.Column(db.String(2), db.ForeignKey("cityprovince.cityProvinceId"))
    completed = db.Column(db.Boolean)

    def __init__(self, districtId, districtName, cityProvinceId, completed):
        self.districtId = districtId
        self.districtName = districtName
        self.cityProvinceId = cityProvinceId
        self.completed = completed

    def json(self):
        return {
            "districtId": self.districtId,
            "districtName": self.districtName,
            "cityProvinceId": self.cityProvinceId,
            "completed": self.completed
        }

    def json1(self):
        return {
            "Name": self.districtName,
            "Id": self.districtId
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(districtName=name).first()

    @classmethod
    def find_by_city_dist_name(cls, city_id, dist_name):
        return cls.query.filter_by(cityProvinceId=city_id, districtName=dist_name).first()

    @classmethod
    def find_by_id(cls, Id):
        return cls.query.filter_by(districtId=Id).first()

    @classmethod
    def find_by_city_id(cls, Id):
        return cls.query.filter_by(cityProvinceId=Id).all()

    @classmethod
    def find_by_id_like(cls, Id):
        search = "{}%".format(Id)
        return cls.query.filter(cls.districtId.like(search)).all()

    @staticmethod
    def find_join_account(id):
        return db.session.query(DistrictDb.districtId, DistrictDb.districtName, DistrictDb.completed,
                                AccountDb.endDate).select_from(DistrictDb).\
            join(AccountDb, DistrictDb.districtId == AccountDb.accountId).filter(DistrictDb.cityProvinceId == id).all()

    @staticmethod
    def find_join_account_allocated(id):
        return db.session.query(DistrictDb.districtId, DistrictDb.districtName, DistrictDb.completed,
                                AccountDb.endDate).select_from(DistrictDb). \
            join(AccountDb, DistrictDb.districtId == AccountDb.accountId).filter(DistrictDb.cityProvinceId == id).\
            count()

    @staticmethod
    def find_join_account_specific(id_acc, id_dis):
        return db.session.query(DistrictDb.districtId, DistrictDb.districtName, DistrictDb.completed,
                                AccountDb.endDate).select_from(DistrictDb).\
            join(AccountDb, DistrictDb.districtId == AccountDb.accountId).filter(DistrictDb.cityProvinceId == id_acc).\
            filter(DistrictDb.districtId == id_dis).first()

    @classmethod
    def count_completed(cls, id_province):
        return cls.query.filter_by(cityProvinceId=id_province).filter_by(completed=True).count()

    @classmethod
    def count_total(cls, id_province):
        return cls.query.filter_by(cityProvinceId=id_province).count()

    @classmethod
    def join_areaId(cls):
        query = db.session.query(DistrictDb, AccountDb). \
            outerjoin(AccountDb, AccountDb.accountId == DistrictDb.districtId).all()
        return query
    @staticmethod
    def find_district_name(id):
        return db.session.query(DistrictDb.districtName).filter_by(districtId=id).first()

    @classmethod
    def check_exist(cls, id):
        return cls.query.filter_by(districtId=id).count()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
