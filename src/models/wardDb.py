from src.database import db

class WardDb(db.Model) :
    __tablename__ = 'ward'
    wardId = db.Column(db.Integer, primary_key=True)
    wardName = db.Column(db.String(30))
    districtId = db.Column(db.Integer, db.ForeignKey("district.districtId"))
    created = db.Column(db.Boolean)

    def __init__(self, wardId, wardName, districtId, created) :
        self.wardId = wardId
        self.wardName = wardName
        self.districtId = districtId
        self.created = created

    def json(self):
        return {"wardId": self.wardId, "wardName" : self.wardName,"districtId":self.districtId, "created" : self.created}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(wardName=name).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(wardId=id).first()

    @classmethod
    def find_by_DistrictId(cls, id):
        return cls.query.filter_by(districtId=id)

    @classmethod
    def find_by_D_Wname(cls, DId, Wname):
        return cls.query.filter_by(districtId=DId,wardName=Wname).first()

    @classmethod
    def find_by_DWname(cls, DId, Wname):
        return cls.query.filter_by(districtId=DId, wardName=Wname).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()




