import re


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


class AccountServices:
    @staticmethod
    def validate_input_login(id, password):
        regex_id = '^[0-9]*$'
        if not validate_regex(id, regex_id) or not password.isalnum() or len(id) % 2 != 0:
            return False
        return True


