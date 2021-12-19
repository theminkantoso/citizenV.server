from src.database import db
from datetime import date


class CitizenDb(db.Model):
    __tablename__ = 'citizen'
    CCCD = db.Column(db.String(12), primary_key=True)
    name = db.Column(db.String(50))
    DOB = db.Column(db.Date)
    sex = db.Column(db.Enum('Nam', 'Nu'))
    maritalStatus = db.Column(db.String(50))
    nation = db.Column(db.String(50))
    religion = db.Column(db.String(50))
    permanentResidence = db.Column(db.String(100))
    temporaryResidence = db.Column(db.String(100))
    educationalLevel = db.Column(db.String(10))
    job = db.Column(db.String(50))
    cityProvinceId = db.Column(db.String(2), db.ForeignKey("cityprovince.cityProvinceId"))
    districtId = db.Column(db.String(4), db.ForeignKey("district.districtId"))
    wardId = db.Column(db.String(6), db.ForeignKey("ward.wardId"))
    groupId = db.Column(db.String(8), db.ForeignKey("residentialgroup.groupId"))

    # full
    def __init__(self, name, DOB, sex, maritalStatus, nation, religion, CCCD, permanentResidence, temporaryResidence,
                 educationalLevel, job, cityProvinceId, districtId, wardId, groupId):
        self.CCCD = CCCD
        self.name = name
        self.DOB = DOB
        self.sex = sex
        self.maritalStatus = maritalStatus
        self.nation = nation
        self.religion = religion
        self.permanentResidence = permanentResidence
        self.temporaryResidence = temporaryResidence
        self.educationalLevel = educationalLevel
        self.job = job
        self.cityProvinceId = cityProvinceId
        self.districtId = districtId
        self.wardId = wardId
        self.groupId = groupId

    def json(self):
        if isinstance(self.DOB, date):
            dob_json = self.DOB.isoformat()
        else:
            dob_json = ''
        return {
            "CCCD": self.CCCD,
            "name": self.name,
            "DOB": dob_json,
            "sex": self.sex,
            "maritalStatus": self.maritalStatus,
            "nation": self.nation,
            "religion": self.religion,
            "permanentResidence": self.permanentResidence,
            "temporaryResidence": self.temporaryResidence,
            "educationalLevel": self.educationalLevel,
            "job": self.job,
            "cityProvinceId": self.cityProvinceId,
            "districtId": self.districtId,
            "wardId": self.wardId,
            "groupId": self.groupId
        }

    @classmethod
    def find_by_id(cls, Id):
        return cls.query.filter_by(CCCD=Id).first()

    @classmethod
    def find_all_citizen(cls):
        return cls.query.all()

    @classmethod
    def find_all_citizen_in_city(cls, city_id):
        return cls.query.filter_by(cityProvinceId=city_id).all()

    @classmethod
    def find_all_citizen_in_dist(cls, dist_id):
        return cls.query.filter_by(districtId=dist_id).all()

    @classmethod
    def find_all_citizen_in_ward(cls, ward_id):
        return cls.query.filter_by(wardId=ward_id).all()

    @classmethod
    def find_all_citizen_in_group(cls, group_id):
        return cls.query.filter_by(groupId=group_id).all()

    @classmethod
    def sum_all_citizen_in_group(cls, group_id):
        query = db.session.query(db.func.count(CitizenDb.CCCD)).filter_by(groupId=group_id)
        return query.scalar()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
