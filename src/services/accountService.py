from src.models.accountDb import AccountDb
from src.services.city import CityServices
from src.services.district import DistrictServices
from src.services.ward import WardServices
from src.services.group import GroupServices
import re
import random
import string


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
                or not validate_regex(input_string=id, regex=regex_id) \
                or len(id) == 0:
            return False
        return True

    @staticmethod
    def validate_input_id_email_create(id_create, email_create):
        regex_id = '^[0-9]*$'
        regex_mail = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not validate_regex(id_create, regex_id) or not validate_regex(email_create, regex_mail) \
                or len(id_create) % 2 != 0:
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
    def check_password(password):
        if not password.isalnum():
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
    def prevent_trash_account(id):
        return (CityServices.check_exist(id) or DistrictServices.check_exist(id) or WardServices.check_exist(id)
                or GroupServices.check_exist(id))




