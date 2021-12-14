from src.database import db


class CitizenDb(db.Model):
    __tablename__ = 'citizen'
    citizenId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    DOB = db.Column(db.String(10))
    sex = db.Column(db.String(3))
    maritalStatus = db.Column(db.String(15))
    nation = db.Column(db.String(15))
    religion = db.Column(db.String(50))
    CMND = db.Column(db.String(11))
    permanentResidence = db.Column(db.String(100))
    temporaryResidence = db.Column(db.String(100))
    educationalLevel = db.Column(db.String(10))
    job = db.Column(db.String(50))
    cityProvinceId = db.Column(db.String(2))
    districtId = db.Column(db.String(4))
    wardId = db.Column(db.String(6))
    groupId = db.Column(db.String(8))

    def __init__(self, citizenId, name, DOB, sex, maritalStatus, nation, religion, CMND,
                 permanentResidence, temporaryResidence, educationalLevel, job):
        self.citizenId = citizenId
        self.name = name
        self.DOB = DOB
        self.sex = sex
        self.maritalStatus = maritalStatus
        self.nation = nation
        self.religion = religion
        self.CMND = CMND
        self.permanentResidence = permanentResidence
        self.temporaryResidence = temporaryResidence
        self.educationalLevel = educationalLevel
        self.job = job

    # Trường hợp B1 nhập liệu
    def __init__(self, citizenId, name, DOB, sex, maritalStatus, nation, religion, CMND,
                 permanentResidence, temporaryResidence, educationalLevel, job, groupId):
        self.citizenId = citizenId
        self.name = name
        self.DOB = DOB
        self.sex = sex
        self.maritalStatus = maritalStatus
        self.nation = nation
        self.religion = religion
        self.CMND = CMND
        self.permanentResidence = permanentResidence
        self.temporaryResidence = temporaryResidence
        self.educationalLevel = educationalLevel
        self.job = job
        self.groupId = groupId

    def json(self):
        return {
            "citizenId": self.citizenId,
            "name": self.name,
            "DOB": self.DOB,
            "sex": self.sex,
            "maritalStatus": self.maritalStatus,
            "nation": self.nation,
            "religion": self.religion,
            "CMND": self.CMND,
            "permanentResidence": self.permanentResidence,
            "temporaryResidence": self.temporaryResidence,
            "educationalLevel": self.educationalLevel,
            "job": self.job
        }

    @classmethod
    def find_by_id(cls, Id):
        return cls.query.filter_by(citizenId=Id).first()

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

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
