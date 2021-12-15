from src.database import db


class GroupDb(db.Model):
    __tablename__ = 'residentialgroup'
    groupId = db.Column(db.String(8), primary_key=True)
    groupName = db.Column(db.String(30))
    wardId = db.Column(db.String(6), db.ForeignKey("ward.wardId"))
    created = db.Column(db.Boolean)

    def __init__(self, groupId, groupName, wardId, created):
        self.groupId = groupId
        self.groupName = groupName
        self.wardId = wardId
        self.created = created

    def json(self):
        return {
            "groupId": self.groupId,
            "groupName": self.groupName,
            "wardId": self.wardId,
            "created": self.created
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(groupName=name).first()

    @classmethod
    def find_by_id(cls, group_id):
        return cls.query.filter_by(groupId=group_id).first()

    @classmethod
    def find_by_ward_id(cls, ward_id):
        return cls.query.filter_by(wardId=ward_id).all()

    @classmethod
    def find_by_ward_group_name(cls, ward_id, group_name):
        return cls.query.filter_by(wardId=ward_id, groupName=group_name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
