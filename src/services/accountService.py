from src.models.accountDb import AccountDb
from src.services.city import CityServices
from src.services.district import DistrictServices
from src.services.ward import WardServices
from src.services.group import GroupServices
import re
import random
import string

from src.models.cityProvinceDb import CityDb
from src.models.districtDb import DistrictDb
from src.models.wardDb import WardDb
from src.models.residentialGroupDb import GroupDb


def validate_regex(input_string, regex):
    """
    Validate input string with a given regular expression
    :param input_string: the string that needed to be checked
    :param regex: regex pattern
    :return: True if satisfy and vice versa
    """
    pattern = re.compile(regex)
    if pattern.fullmatch(input_string):
        return True
    return False


class AccountService:
    @staticmethod
    def validate_input_id_pass(id, password):
        regex_id = '^[0-9]*$'
        if not validate_regex(id, regex_id) or not password.isalnum() or len(id) == 0:
            return False
        return True

    @staticmethod
    def validate_input_id(id):
        regex_id = '^[0-9]*$'
        if not validate_regex(id, regex_id):
            return False
        return True

    @staticmethod
    def validate_input_id_email(id, email):
        regex_id = '^[0-9]*$'
        regex_mail = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not validate_regex(input_string=email.lower(), regex=regex_mail) \
                or not validate_regex(input_string=id, regex=regex_id):
            return False
        return True

    @staticmethod
    def validate_input_id_email_create(id_create, email_create):
        regex_id = '^[0-9]*$'
        regex_mail = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not validate_regex(id_create, regex_id) or not validate_regex(email_create, regex_mail):
            return False
        return True

    @staticmethod
    def validate_input_pass_newpass(password, new_password):
        if not password.isalnum() or not new_password.isalnum() or len(new_password) == 0:
            return False
        return True

    @staticmethod
    def check_format_id_plus_2(id_acc, id_create, id_create_length):
        if len(id_create) <= len(id_acc):
            return False
        if id_acc != id_create[0:id_create_length - 2]:
            return False
        return True

    @staticmethod
    def find_duplicate(id):
        exist_check = AccountDb.find_by_id(accId=id)
        if exist_check:
            return False
        return True


    @staticmethod
    def validate_email(email):
        regex_mail = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not validate_regex(email, regex_mail):
            return False
        return True

    @staticmethod
    def validate_period(startDate, endDate):
        """
        ensure startDate <= endDate
        :param startDate: start CRUD date
        :param endDate: end CRUD date
        :return: True if startDate is earlier than endDate
        """
        if startDate > endDate:
            return False
        return True

    @staticmethod
    def random_string():
        """
        Generate a random password
        :return: a random string
        :return:
        """
        str1 = ''.join((random.choice(string.ascii_letters) for x in range(6)))
        str1 += ''.join((random.choice(string.digits) for x in range(6)))

        sam_list = list(str1)
        random.shuffle(sam_list)
        final_string = ''.join(sam_list)
        return final_string

    @staticmethod
    def get_email_from_manager(id_manager, id_in):
        return AccountDb.get_email_user_manager(id_manager, id_in)

    @staticmethod
    def join_area_account(acc, managed_accounts, id_acc):
        accounts = []
        if acc["role"] == 0:  # Tất cả người dùng A1
            return {'Accounts': list(map(lambda x: x.json(), managed_accounts))}, 200
        # Cho A1, A2, A3, B1
        elif acc["role"] == 1:
            acc_join = CityDb.join_areaId()  # join để lấy id của các vùng
            for i in range(len(acc_join)):
                areaId = acc_join[i][0].cityProvinceId  # Id của các thành phố
                accounts.append(AccountDb.json1(acc_join[i][1], areaId))
        elif acc["role"] == 2:
            acc_join = DistrictDb.join_areaId()
            for i in range(len(acc_join)):
                areaId = acc_join[i][0].districtId  # Id của các quận/huyện
                len_areaId = len(areaId)
                if areaId[0:len_areaId - 2] == id_acc:
                    accounts.append(AccountDb.json1(acc_join[i][1], areaId))
        elif acc["role"] == 3:
            acc_join = WardDb.join_areaId()
            for i in range(len(acc_join)):
                areaId = acc_join[i][0].wardId  # Id của các xã/phường
                len_areaId = len(areaId)
                if areaId[0:len_areaId - 2] == id_acc:
                    accounts.append(AccountDb.json1(acc_join[i][1], areaId))
        elif acc["role"] == 4:
            acc_join = GroupDb.join_areaId()
            for i in range(len(acc_join)):
                areaId = acc_join[i][0].groupId  # Id của các thôn/bản/tdp
                len_areaId = len(areaId)
                if areaId[0:len_areaId - 2] == id_acc:
                    accounts.append(AccountDb.json1(acc_join[i][1], areaId))
        return accounts

    @classmethod
    def area_name_of_acc(cls, user):
        name = ""
        if user.roleId == 0:
            name = "Admin"
        elif user.roleId == 1:
            name = "A1"
        elif user.roleId == 2:
            name = CityDb.find_by_id(user.accountId).cityProvinceName
        elif user.roleId == 3:
            dist = DistrictDb.find_by_id(user.accountId).districtName
            city = CityDb.find_by_id(user.accountId[0:2]).cityProvinceName
            name = dist + ',' + city
        elif user.roleId == 4:
            ward = WardDb.find_by_id(user.accountId).wardName
            dist = DistrictDb.find_by_id(user.accountId[0:4]).districtName
            city = CityDb.find_by_id(user.accountId[0:2]).cityProvinceName
            name = ward + ',' + dist + ',' + city

        elif user.roleId == 5:
            group = GroupDb.find_by_id(user.accountId).groupName
            ward = WardDb.find_by_id(user.accountId[0:6]).wardName
            dist = DistrictDb.find_by_id(user.accountId[0:4]).districtName
            city = CityDb.find_by_id(user.accountId[0:2]).cityProvinceName
            name = group + ',' + ward + ',' + dist + ',' + city
        return name
    def prevent_trash_account(id):
        return (CityServices.check_exist(id) or DistrictServices.check_exist(id) or WardServices.check_exist(id)
                or GroupServices.check_exist(id))




