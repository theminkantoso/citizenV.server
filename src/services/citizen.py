from datetime import date

from flask_jwt_extended import get_jwt

from src.models.citizenDb import CitizenDb
from src.models.accountDb import AccountDb
import re

# regex_validate
regex_group_id = '^(0[1-9]|[1-9][0-9]){4}$'
regex_cccd = '[0-9]{12}'
regex_edu_level = '^([0-9]|([1][012]))[/]([9]|([1][2]))$'
regex_area_id = '^[0-9]*$'


# so sánh chuỗi với chuỗi regex
def validate_regex(input_string, regex):
    pattern = re.compile(regex)
    if pattern.fullmatch(input_string):
        return True
    return False


# Kiểm tra DOB
def check_dob(dob):
    s = dob.split('-')
    if len(s) != 3:  # 3 phần ngày, tháng, năm
        return False
    regex = '^[0-9]*$'  # đầu vào là các chữ số
    if (not validate_regex(s[0], regex)) or (not validate_regex(s[1], regex)) or (not validate_regex(s[2], regex)):
        return False
    # chuyển str về int
    ngay = int(s[2])
    thang = int(s[1])
    nam = int(s[0])
    # kiem tra tinh hop le
    if thang > 12 or thang < 1:
        return False
    if thang == 1 or thang == 3 or thang == 5 or thang == 7 or thang == 8 or thang == 10 or thang == 12:
        if ngay > 31:
            return False
    elif thang == 2:
        if nam % 4 == 0 and nam % 100 != 0:  # nam nhuan
            if ngay > 29:
                return False
        elif ngay > 28:
            return False
    elif ngay > 30:
        return False
    if ngay < 1:
        return False
    # so sanh vơi ngày hiện tại
    today = date.today()
    if nam > today.year or nam < 1910:  # so năm >= 1910 và < năm hiện tại
        return False
    elif nam == today.year and thang > today.month:
        return False
    elif nam == today.year and thang == today.month and ngay > today.day:
        return False
    return True


class CitizenServices:

    # Xem id người dân có tồn tại không
    @staticmethod
    def exist_citizen(id_acc: str, citizen_id: str):
        # validate id_citizen là cccd
        if not validate_regex(citizen_id, regex_cccd):
            return 0  # Invalid id
        citizen = CitizenDb.find_by_id(citizen_id)
        role_acc = AccountDb.find_by_id(id_acc).roleId
        if citizen:  # tìm thấy người dân
            if id_acc == citizen.groupId or id_acc == citizen.wardId or id_acc == citizen.districtId \
                    or id_acc == citizen.cityProvinceId or role_acc == 1:
                return citizen
            return 1  # not authorized
        return None  # citizen not exist

    # Validate CCCD
    @staticmethod
    def cccd(cccd):
        # validate cccd
        if not validate_regex(cccd, regex_cccd):
            return False  # Invalid cccd
        return True

    # Validate request
    @staticmethod
    def validate(data: dict):
        dob = data['DOB']
        sex = data['sex']
        mari_status = data['maritalStatus']
        edu_level = data['educationalLevel']

        # validate DOB
        if not check_dob(dob):
            return 0  # Invalid DOB

        # validate sex:
        list_sex = ['Nam', 'Nu']
        if sex not in list_sex:
            return 1  # Invalid sex

        # validate marital_status
        list_marital_status = ['Đã kết hôn', 'Chưa kết hôn']
        if mari_status not in list_marital_status:
            return 2  # Invalid marital status

        # validate educationalLevel
        if not validate_regex(edu_level, regex_edu_level):
            return 3  # Invalid edu_level

        return 4  # not Invalid

    # Nhập liệu : Bởi B1/B2
    @staticmethod
    def create_citizen(data: dict, id_acc: str, group_id: str):
        role_acc = AccountDb.find_by_id(id_acc).roleId
        if (role_acc == 5 and id_acc != group_id) or (role_acc == 4 and id_acc != group_id[0:6]):
            return 0  # not authorize
        if CitizenDb.find_by_id(data["CCCD"]):
            return 1  # CCCD is exist
        id_city = id_acc[0:2]
        id_district = id_acc[0:4]
        id_ward = id_acc[0:6]

        citizen = CitizenDb(CCCD=data["CCCD"], name=data["name"], DOB=data["DOB"], sex=data["sex"],
                            maritalStatus=data["maritalStatus"], nation=data["nation"], religion=data["religion"],
                            permanentResidence=data["permanentResidence"],
                            temporaryResidence=data["temporaryResidence"],
                            educationalLevel=data["educationalLevel"], job=data["job"], cityProvinceId=id_city,
                            districtId=id_district, wardId=id_ward, groupId=group_id)
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

    # update citizen
    @staticmethod
    def update_citizen(data: dict, citizen: CitizenDb, id_acc: str):
        role_acc = AccountDb.find_by_id(id_acc).roleId
        if (role_acc == 5 and id_acc != citizen.groupId) or (role_acc == 4 and id_acc != citizen.wardId):
            return 0  # not authorize
        try:
            citizen.name = data["name"]
            citizen.DOB = data["DOB"]
            citizen.sex = data["sex"]
            citizen.maritalStatus = data["maritalStatus"]
            citizen.nation = data["nation"]
            citizen.religion = data["religion"]
            citizen.temporaryResidence = data["temporaryResidence"]
            citizen.educationalLevel = data["educationalLevel"]
            citizen.job = data["job"]
            citizen.save_to_db()
        except Exception as e:
            print(e)
            return 1  # err
        return 2  # save

    # Tra cứu tất cả người dân theo id_acc
    @staticmethod
    def all_citizen(id_acc: str):
        role = get_jwt()['role']
        # A1
        if role == 1:
            citizens = CitizenDb.find_all_citizen()
            return citizens
        elif role == 2:  # A2
            citizens = CitizenDb.find_all_citizen_in_city(id_acc)
            return citizens
        elif role == 3:  # A3
            citizens = CitizenDb.find_all_citizen_in_dist(id_acc)
            return citizens
        elif role == 4:  # B1
            citizens = CitizenDb.find_all_citizen_in_ward(id_acc)
            return citizens
        elif role == 5:  # B2
            citizens = CitizenDb.find_all_citizen_in_group(id_acc)
            return citizens

    # Tra cứu theo nóm
    @staticmethod
    def all_citizen_by_list_areas(role: int, areas):
        len_areaId = len(areas[0])
        # Validate : tất cả các id đều là số , chia  hết cho 2 , độ dài tất cả các id đầu vào bằng nhau
        for area in areas:
            if (not validate_regex(area, regex_area_id)) or len(area) % 2 != 0 or len(area) != len_areaId:
                return 1
        # A1 chỉ cho
        if (role == 1 and len_areaId in [2, 4, 6, 8]) \
                or (role == 2 and len_areaId in [4, 6, 8]) \
                or (role == 3 and len_areaId in [6, 8]) \
                or (role == 4 and len_areaId == 8):
            return CitizenDb.find_all_citizen_by_list_area(areas, len_areaId)
        return []

    @staticmethod
    def get_population_entire():
        return CitizenDb.get_population_entire()

    @staticmethod
    def get_population_city(id):
        return CitizenDb.get_population_city(id)

    @staticmethod
    def get_population_district(id):
        return CitizenDb.get_population_district(id)

    @staticmethod
    def get_population_ward(id):
        return CitizenDb.get_population_ward(id)

    @staticmethod
    def get_population_group(id):
        return CitizenDb.get_population_group(id)

    @staticmethod
    def get_stats_sex_entire():
        return CitizenDb.get_stats_sex_entire()

    @staticmethod
    def get_stats_sex_city(id):
        return CitizenDb.get_stats_sex_city(id)

    @staticmethod
    def get_stats_sex_district(id):
        return CitizenDb.get_stats_sex_district(id)

    @staticmethod
    def get_stats_sex_ward(id):
        return CitizenDb.get_stats_sex_ward(id)

    @staticmethod
    def get_stats_sex_group(id):
        return CitizenDb.get_stats_sex_group(id)

    @staticmethod
    def get_stats_edu_entire():
        return CitizenDb.get_stats_edu_entire()

    @staticmethod
    def get_stats_edu_city(id):
        return CitizenDb.get_stats_edu_city(id)

    @staticmethod
    def get_stats_edu_district(id):
        return CitizenDb.get_stats_edu_district(id)

    @staticmethod
    def get_stats_edu_ward(id):
        return CitizenDb.get_stats_edu_ward(id)

    @staticmethod
    def get_stats_edu_group(id):
        return CitizenDb.get_stats_edu_district(id)

    @staticmethod
    def get_marital_status_entire():
        return CitizenDb.get_marital_status_entire()

    @staticmethod
    def get_marital_status_city(id):
        return CitizenDb.get_marital_status_city(id)

    @staticmethod
    def get_marital_status_district(id):
        return CitizenDb.get_marital_status_district(id)

    @staticmethod
    def get_marital_status_ward(id):
        return CitizenDb.get_marital_status_ward(id)

    @staticmethod
    def get_marital_status_group(id):
        return CitizenDb.get_marital_status_group(id)

    @staticmethod
    def get_group_age_entire():
        return CitizenDb.get_group_age_entire()

    @staticmethod
    def get_group_age_city(id):
        return CitizenDb.get_group_age_city(id)

    @staticmethod
    def get_group_age_district(id):
        return CitizenDb.get_group_age_district(id)

    @staticmethod
    def get_group_age_ward(id):
        return CitizenDb.get_group_age_ward(id)

    @staticmethod
    def get_group_age_group(id):
        return CitizenDb.get_group_age_group(id)
