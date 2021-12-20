from src.database import db
from datetime import date


class CitizenDb(db.Model):
    __tablename__ = 'citizen'
    CCCD = db.Column(db.String(12), primary_key=True)
    name = db.Column(db.String(50))
    DOB = db.Column(db.Date)
    sex = db.Column(db.String(3))
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

    @classmethod
    def get_population_entire(cls):
        return cls.query.count()

    @classmethod
    def get_population_city(cls, id):
        return cls.query.filter_by(cityProvinceId=id).count()

    @classmethod
    def get_population_district(cls, id):
        return cls.query.filter_by(districtId=id).count()

    @classmethod
    def get_population_ward(cls, id):
        return cls.query.filter_by(wardId=id).count()

    @classmethod
    def get_population_group(cls, id):
        return cls.query.filter_by(groupId=id).count()

    @staticmethod
    def get_stats_sex_entire():
        # return db.session.query(CitizenDb.sex, db.func.count()).group_by(CitizenDb.sex).filter_by(nation='Kinh').all()
        return db.session.query(CitizenDb.sex, db.func.count()).group_by(CitizenDb.sex).all()

    @staticmethod
    def get_stats_sex_city(id):
        return db.session.query(CitizenDb.sex, db.func.count()).group_by(CitizenDb.sex).\
            filter_by(cityProvinceId=id).all()

    @staticmethod
    def get_stats_sex_district(id):
        return db.session.query(CitizenDb.sex, db.func.count()).group_by(CitizenDb.sex). \
            filter_by(districtId=id).all()

    @staticmethod
    def get_stats_sex_ward(id):
        return db.session.query(CitizenDb.sex, db.func.count()).group_by(CitizenDb.sex). \
            filter_by(wardId=id).all()

    @staticmethod
    def get_stats_sex_group(id):
        return db.session.query(CitizenDb.sex, db.func.count()).group_by(CitizenDb.sex). \
            filter_by(groupId=id).all()

    @staticmethod
    def get_stats_edu_entire():
        return db.session.query(CitizenDb.educationalLevel, db.func.count()).group_by(CitizenDb.educationalLevel).all()

    @staticmethod
    def get_stats_edu_city(id):
        return db.session.query(CitizenDb.educationalLevel, db.func.count()).group_by(CitizenDb.educationalLevel).\
            filter_by(cityProvinceId=id).all()

    @staticmethod
    def get_stats_edu_district(id):
        return db.session.query(CitizenDb.educationalLevel, db.func.count()).group_by(CitizenDb.educationalLevel). \
            filter_by(districtId=id).all()

    @staticmethod
    def get_stats_edu_ward(id):
        return db.session.query(CitizenDb.educationalLevel, db.func.count()).group_by(CitizenDb.educationalLevel). \
            filter_by(wardId=id).all()

    @staticmethod
    def get_stats_edu_group(id):
        return db.session.query(CitizenDb.educationalLevel, db.func.count()).group_by(CitizenDb.educationalLevel). \
            filter_by(groupId=id).all()

    @staticmethod
    def get_marital_status_entire():
        return db.session.query(CitizenDb.maritalStatus, db.func.count()).group_by(CitizenDb.maritalStatus).all()

    @staticmethod
    def get_marital_status_city(id):
        return db.session.query(CitizenDb.maritalStatus, db.func.count()).group_by(CitizenDb.maritalStatus). \
            filter_by(cityProvinceId=id).all()

    @staticmethod
    def get_marital_status_district(id):
        return db.session.query(CitizenDb.maritalStatus, db.func.count()).group_by(CitizenDb.maritalStatus). \
            filter_by(districtId=id).all()

    @staticmethod
    def get_marital_status_ward(id):
        return db.session.query(CitizenDb.maritalStatus, db.func.count()).group_by(CitizenDb.maritalStatus). \
            filter_by(wardId=id).all()

    @staticmethod
    def get_marital_status_group(id):
        return db.session.query(CitizenDb.maritalStatus, db.func.count()).group_by(CitizenDb.maritalStatus). \
            filter_by(groupId=id).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
