from src.database import db
from src.models.accountDb import AccountDb
from src.models.citizenDb import CitizenDb


class CityDb(db.Model):
    __tablename__ = 'cityprovince'
    cityProvinceId = db.Column(db.String(2), primary_key=True)
    cityProvinceName = db.Column(db.String(30))
    completed = db.Column(db.Boolean)

    def __init__(self, cityProvinceId, cityProvinceName, completed):
        self.cityProvinceId = cityProvinceId
        self.cityProvinceName = cityProvinceName
        self.completed = completed

    def json(self):
        return {
            "cityProvinceId": self.cityProvinceId,
            "cityProvinceName": self.cityProvinceName,
            "completed": self.completed
        }

    def json1(self):
        return {
            "Name": self.cityProvinceName,
            "Id": self.cityProvinceId
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(cityProvinceName=name).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(cityProvinceId=id).first()

    @staticmethod
    def find_join_account():
        return db.session.query(CityDb.cityProvinceId, CityDb.cityProvinceName, CityDb.completed, AccountDb.endDate).\
            select_from(CityDb).join(AccountDb, CityDb.cityProvinceId == AccountDb.accountId).all()

    @staticmethod
    def find_join_account_allocated():
        return db.session.query(CityDb.cityProvinceId, CityDb.cityProvinceName, CityDb.completed, AccountDb.endDate). \
            select_from(CityDb).join(AccountDb, CityDb.cityProvinceId == AccountDb.accountId).count()

    @staticmethod
    def find_join_account_specific(id):
        return db.session.query(CityDb.cityProvinceId, CityDb.cityProvinceName, CityDb.completed, AccountDb.endDate). \
            select_from(CityDb).join(AccountDb, CityDb.cityProvinceId == AccountDb.accountId). \
            filter(CityDb.cityProvinceId == id).first()

    @classmethod
    def count_completed(cls):
        return cls.query.filter_by(completed=True).count()

    @classmethod
    def count_total(cls):
        return cls.query.count()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def join_areaId(cls):
        query = db.session.query(CityDb, AccountDb). \
            outerjoin(AccountDb, AccountDb.accountId == CityDb.cityProvinceId).all()
        return query
    @staticmethod
    def find_city_name(id):
        return db.session.query(CityDb.cityProvinceName).filter_by(cityProvinceId=id).first()

    @classmethod
    def check_exist(cls, id):
        return cls.query.filter_by(cityProvinceId=id).count()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
