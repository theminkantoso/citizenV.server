from src.database import db

class DistrictDb(db.Model) :
    __tablename__ = 'district'
    districtId =  db.Column(db.Integer, primary_key=True)
    districtName = db.Column(db.String(30))
    cityProvinceId = db.Column(db.Integer, db.ForeignKey("cityprovince.cityProvinceId"))
    created = db.Column(db.Boolean)

    def __init__(self, districtId, districtName, cityProvinceId, created) :
        self.districtId = districtId
        self.districtName = districtName
        self.cityProvinceId = cityProvinceId
        self.created = created

    def json(self):
        return {"districtId":self.districtId, "districtName": self.districtName,"cityProvinceId":self.cityProvinceId, "created" : self.created}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(districtName=name).first()

    @classmethod
    def find_by_C_D_name(cls, CId, Dname):
        return cls.query.filter_by(cityProvinceId=CId,districtName=Dname).first()

    # @classmethod
    # def find_by_C_Dname(cls, CId, Dname):
    #     return cls.query.filter_by(cityProvinceId=CId, districtName=Dname).all()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(districtId=id).first()

    @classmethod
    def find_by_CityId(cls, id):
        return cls.query.filter_by(cityProvinceId=id)



    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()




