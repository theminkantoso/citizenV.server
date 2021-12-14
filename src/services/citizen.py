from src.models.citizenDb import CitizenDb
import re

# regex
regex_cmnd = '[0-9]{12}'
regex_DOB = '\s+(?:0[1-9]|[12][0-9]|3[01]):(?:0[1-9]|1[012]):(?:19\d{2}|20[01][0-9]|2020)'


# so sánh chuỗi với chuỗi regex
def validate_regex(input_string, regex):
    pattern = re.compile(regex)
    if pattern.fullmatch(input_string):
        return True
    return False


class CitizenServices():

    # Xem id người dân có tồn tại không
    @staticmethod
    def exist_citizen(Id: int, id_acc: str):
        # validate id_citizen
        regex_id = '^([1-9][0-9]*)$'
        str_id = str(Id)
        if not validate_regex(str_id, regex_id):
            return 0  # Invalid id
        citizen = CitizenDb.find_by_id(Id)
        if citizen:
            if id_acc == citizen.groupId or id_acc == citizen.wardId or id_acc == citizen.districtId \
                    or id_acc == citizen.cityProvinceId or id_acc == '00':
                return citizen
            return 1
        return None

    # Nhập liệu : Bởi B1/B2
    @staticmethod
    def create_citizen(data: dict, id_acc: str):
        # kiểm tra Account
        # role = ['B1', 'B2']
        # acc = AccountDb.find_by_id(id_acc)
        # if acc.roleId not in role:
        #     return 0  # not authorized
        # if acc.isLocked:
        #     return 1  # is locked

        id_city = id_acc[0:2]
        id_district = id_acc[0:4]
        id_ward = id_acc[0:6]
        id_group = id_acc
        # sex = data['sex']
        # list_sex = ['Nam', 'Nữ']
        # list_marital_status = ['Đã kết hôn', 'Chưa kết hôn']
        # if sex not in list_sex:

        citizen = CitizenDb(**data)
        citizen.cityProvinceId = id_city
        citizen.districtId = id_district
        citizen.wardId = id_ward
        citizen.groupId = id_group
        try:
            citizen.save_to_db()
        except:
            return 2  # don't save
        return 3  # saved

    # Xoá 1 citizen ra khỏi dữ liệu
    @staticmethod
    def delete_citizen(citizen: CitizenDb):
        try:
            citizen.delete_from_db()
        except:
            return 1  # error
        return 2  # deleted

    # Tra cứu tất cả người dân theo id_acc
    @staticmethod
    def all_citizen_by_acc(id_acc: str):
        if id_acc == '00':
            citizens = CitizenDb.find_all_citizen()
            return citizens
        elif len(id_acc) == 2:
            citizens = CitizenDb.find_all_citizen_in_city(id_acc)
            return citizens
        elif len(id_acc) == 4:
            citizens = CitizenDb.find_all_citizen_in_dist(id_acc)
            return citizens
        elif len(id_acc) == 6:
            citizens = CitizenDb.find_all_citizen_in_ward(id_acc)
            return citizens
        elif len(id_acc) == 8:
            citizens = CitizenDb.find_all_citizen_in_group(id_acc)
            return citizens
