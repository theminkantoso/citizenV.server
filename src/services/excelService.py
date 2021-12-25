from src.services.citizen import CitizenServices
from datetime import date


class ExcelServices():
    @staticmethod
    def to_dict(row):
        if row is None:
            return None

        rtn_dict = dict()
        keys = row.__table__.columns.keys()
        for key in keys:
            if key == 'cityProvinceId' or key == 'districtId' or key == 'wardId' or key == 'groupId':
                continue
            elif isinstance(getattr(row, key), date):
                rtn_dict['Ngay sinh'] = getattr(row, key).strftime("%d/%m/%Y")
            elif key == 'name':
                rtn_dict['Ho va ten'] = getattr(row, key)
            elif key == 'sex':
                rtn_dict['Gioi tinh'] = getattr(row, key)
            elif key == 'maritalStatus':
                rtn_dict['Hon nhan'] = getattr(row, key)
            elif key == 'nation':
                rtn_dict['Dan toc'] = getattr(row, key)
            elif key == 'religion':
                rtn_dict['Ton giao'] = getattr(row, key)
            elif key == 'permanentResidence':
                rtn_dict['Thuong tru'] = getattr(row, key)
            elif key == 'temporaryResidence':
                rtn_dict['Tam tru'] = getattr(row, key)
            elif key == 'educationalLevel':
                rtn_dict['Hoc van'] = getattr(row, key)
            elif key == 'job':
                rtn_dict['Nghe nghiep'] = getattr(row, key)
            else:
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
