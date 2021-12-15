from src.database import db


class WardDb(db.Model):
    __tablename__ = 'ward'
    wardId = db.Column(db.String(6), primary_key=True)
    wardName = db.Column(db.String(30))
    districtId = db.Column(db.String(4), db.ForeignKey("district.districtId"))
    created = db.Column(db.Boolean)

    def __init__(self, wardId, wardName, districtId, created):
        self.wardId = wardId
        self.wardName = wardName
        self.districtId = districtId
        self.created = created

    def json(self):
        return {
            "wardId": self.wardId,
            "wardName": self.wardName,
            "districtId": self.districtId,
            "created": self.created
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

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
