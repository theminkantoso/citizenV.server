from src.database import db

class GroupDb(db.Model) :
    __tablename__ = 'residentialgroup'
    groupId = db.Column(db.Integer, primary_key=True)
    groupName = db.Column(db.String(30))
    wardId = db.Column(db.Integer, db.ForeignKey("ward.wardId"))
    created = db.Column(db.Boolean)

    def __init__(self, groupId, groupName, wardId, created) :
        self.groupId = groupId
        self.groupName = groupName
        self.wardId = wardId
        self.created = created

    def json(self):
        return {"groupId":self.groupId, "groupName": self.groupName, "wardId": self.wardId, "created" : self.created}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(groupName=name).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(groupId=id).first()

    @classmethod
    def find_by_WardId(cls, id):
        return cls.query.filter_by(wardId=id)

    @classmethod
    def find_by_W_Gname(cls, WId, Gname):
        return cls.query.filter_by(wardId=WId,groupName=Gname).first()

    @classmethod
    def find_by_WGname(cls, WId, Gname):
        return cls.query.filter_by(wardId=WId, groupName=Gname).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()




