from datetime import date

from src.models.citizenDb import CitizenDb
from src.models.accountDb import AccountDb
from src.models.cityProvinceDb import CityDb
from src.models.districtDb import DistrictDb
from src.models.wardDb import WardDb
from src.models.residentialGroupDb import GroupDb
import re

# regex_validate
regex_group_id = '^(0[1-9]|[1-9][0-9]){4}$'
regex_cccd = '[0-9]{12}'
regex_edu_level = '^([0-9]|([1][012]))[/]([9]|([1][2]))$'


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
    regex = '^[0-9]*$' # đầu vào là các chữ số
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
        city_name = CityDb.find_by_id(id_city).cityProvinceName
        dist_name = DistrictDb.find_by_id(id_district).districtName
        ward_name = WardDb.find_by_id(id_ward).wardName
        group_name = GroupDb.find_by_id(group_id).groupName

        permanent_residence = group_name + ',' + ward_name + ',' + dist_name + ',' + city_name

        citizen = CitizenDb(CCCD=data["CCCD"], name=data["name"], DOB=data["DOB"], sex=data["sex"],
                            maritalStatus=data["maritalStatus"], nation=data["nation"], religion=data["religion"],
                            permanentResidence=permanent_residence, temporaryResidence=data["temporaryResidence"],
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
    def all_citizen_by_acc(id_acc: str):
        # A1
        if AccountDb.find_by_id(id_acc).roleId == '1':
            citizens = CitizenDb.find_all_citizen()
            return citizens
        elif len(id_acc) == 2:  # A2
            citizens = CitizenDb.find_all_citizen_in_city(id_acc)
            return citizens
        elif len(id_acc) == 4:  # A3
            citizens = CitizenDb.find_all_citizen_in_dist(id_acc)
            return citizens
        elif len(id_acc) == 6:  # B1
            citizens = CitizenDb.find_all_citizen_in_ward(id_acc)
            return citizens
        elif len(id_acc) == 8:  # B2
            citizens = CitizenDb.find_all_citizen_in_group(id_acc)
            return citizens
