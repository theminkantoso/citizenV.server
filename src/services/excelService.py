from src.services.citizen import CitizenServices


class ExcelServices():
    @staticmethod
    def to_dict(row):
        if row is None:
            return None

        rtn_dict = dict()
        keys = row.__table__.columns.keys()
        for key in keys:
            rtn_dict[key] = getattr(row, key)
        return rtn_dict

    @staticmethod
    def get_citizen(id, role):
        if role == 3:
            return CitizenServices.all_citizen_district(id)
        elif role == 4:
            return CitizenServices.all_citizen_ward(id)
        else:
            return None
