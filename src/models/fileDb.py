from src.database import db


class FileDb(db.Model):
    __tablename__ = 'file'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    data = db.Column(db.BLOB)

    def __init__(self, name, data):
        self.name = name
        self.data = data

    @staticmethod
    def file():
        return db.session.query(FileDb.data).filter_by(id=1).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
