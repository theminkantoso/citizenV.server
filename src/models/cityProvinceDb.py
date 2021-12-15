from src.database import db


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
            "created": self.completed
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(cityProvinceName=name).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(cityProvinceId=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
