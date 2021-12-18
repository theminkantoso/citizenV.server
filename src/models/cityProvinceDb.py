from src.database import db
from src.models.citizenDb import CitizenDb
from src.models.accountDb import AccountDb


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

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(cityProvinceName=name).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(cityProvinceId=id).first()

    @staticmethod
    def find_join_account():
        return db.session.query(CityDb.cityProvinceId, CityDb.cityProvinceName, CityDb.completed, AccountDb.endTime).\
            join(AccountDb).filter(CityDb.cityProvinceId == AccountDb.accountId).all()
        # return db.session.query(CityDb.cityProvinceName, CitizenDb.name).join(CitizenDb).\
        #     filter(CityDb.cityProvinceId == CitizenDb.cityProvinceId).filter(CityDb.cityProvinceId == 29).all()

    @staticmethod
    def find_join_account_specific(id):
        return db.session.query(CityDb.cityProvinceId, CityDb.cityProvinceName, CityDb.completed, AccountDb.endTime). \
            join(AccountDb).filter(CityDb.cityProvinceId == AccountDb.accountId).\
            filter(CityDb.cityProvinceId == id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
