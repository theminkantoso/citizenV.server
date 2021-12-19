from src.database import db


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

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
