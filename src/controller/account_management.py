from flask_restful import Resource, reqparse
from src.models.accountDb import AccountDb
# from src.models.cityProvinceDb import CityDb
# from src.models.districtDb import DistrictDb
# from src.models.wardDb import WardDb
# from src.models.residentialGroupDb import GroupDb
from src.services.accountService import AccountService
from src.core.auth import crud_permission_required, authorized_required
from werkzeug.security import generate_password_hash
from datetime import datetime
from src.services import my_mail
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask_mail import Message

import re
import random
import string


def random_string():
    """
    Generate a random password
    :return: a random string
    """
    str1 = ''.join((random.choice(string.ascii_letters) for x in range(6)))
    str1 += ''.join((random.choice(string.digits) for x in range(6)))

    sam_list = list(str1)
    random.shuffle(sam_list)
    final_string = ''.join(sam_list)
    return final_string


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


class AccountManagement(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=str)
    parser.add_argument('email', type=str)

    @jwt_required()
    @authorized_required(roles=[0, 1, 2, 3, 4])
    def get(self):
        id_acc = get_jwt_identity()
        acc = AccountDb.find_by_id(id_acc)
        managed_accounts = AccountDb.find_managed_account_by_id(id_acc)  # Tất cả người dùng dưới quyền quản lý
        if managed_accounts:
            k = []
            if acc.roleId == 0:  # Tất cả người dùng A1
                return {'Accounts': list(map(lambda x: x.json(), managed_accounts))}, 200
            # Cho A1, A2, A3, B1
            acc_join = AccountDb.join_areaId(acc.roleId)   # join để lấy id của các vùng
            for i in range(len(acc_join)):
                areaId = ""
                if acc.roleId == 1:
                    areaId = acc_join[i][0].cityProvinceId  # Id của các thành phố
                elif acc.roleId == 2:
                    areaId = acc_join[i][0].districtId  # Id của các quận/huyện
                elif acc.roleId == 3:
                    areaId = acc_join[i][0].wardId  # Id của các xã/phường
                elif acc.roleId == 4:
                    areaId = acc_join[i][0].groupId  # Id của các thôn/bản/tdp
                k.append(AccountDb.json1(acc_join[i][1], areaId))
            return {"areas": k}, 200
        return {}, 200
        # id_acc = get_jwt_identity()
        # acc = get_jwt()
        # managed_accounts = AccountDb.find_managed_account_by_id(id_acc)  # Tất cả người dùng dưới quyền quản lý
        # if managed_accounts:
        #     k = []
        #     if acc["role"] == 0:  # Tất cả người dùng A1
        #         return {'Accounts': list(map(lambda x: x.json(), managed_accounts))}, 200
        #     # Cho A1, A2, A3, B1
        #     acc_join = AccountDb.join_areaId(acc["role"])   # join để lấy id của các vùng
        #     for i in range(len(acc_join)):
        #         areaId = ""
        #         if acc["role"] == 1:
        #             areaId = acc_join[i][0].cityProvinceId  # Id của các thành phố
        #         elif acc["role"] == 2:
        #             areaId = acc_join[i][0].districtId  # Id của các quận/huyện
        #         elif acc["role"] == 3:
        #             areaId = acc_join[i][0].wardId  # Id của các xã/phường
        #         elif acc["role"] == 4:
        #             areaId = acc_join[i][0].groupId  # Id của các thôn/bản/tdp
        #         len_areaId = len(areaId)
        #         if areaId[0:len_areaId-2] == id_acc:
        #             k.append(AccountDb.json1(acc_join[i][1], areaId))
        #     return {"areas": k}, 200
        # managed_accounts = AccountDb.find_managed_account_by_id(id_acc)
        # if managed_accounts:
        #     return {'Accounts': list(map(lambda x: x.json(), managed_accounts))}, 200
        # return {}, 200

    @jwt_required()
    @authorized_required(roles=[0, 1, 2, 3, 4])
    @crud_permission_required
    def post(self):
        data = AccountManagement.parser.parse_args()
        id_acc = get_jwt_identity()
        role_acc = get_jwt()
        id_create = data['id']
        email_create = data['email']

        # validate
        regex_id = '^[0-9]*$'
        regex_mail = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not validate_regex(id_create, regex_id) or not validate_regex(email_create, regex_mail):
            return {'message': "Invalid input format"}, 400

        # check chống tạo tk rác, tài khoản không tương ứng với một mã tỉnh thành quận huyện nào đó
        id_create_len = len(id_create)
        # NEED TO REMOVE THESE COMMENT LATER
        # if id_create_len == 2:
        #     duplicate_check = CityDb.find_by_id(id=id_create)
        # elif id_create_len == 4:
        #     duplicate_check = DistrictDb.find_by_id(id=id_create)
        # elif id_create_len == 6:
        #     duplicate_check = WardDb.find_by_id(id=id_create)
        # elif id_create_len == 8:
        #     duplicate_check = GroupDb.find_by_id(id=id_create)
        #
        # if duplicate_check is None:
        #     return {'message': "This is a trash account"}, 400

        # check tk phải có id đúng format <tkcha> + <2 ký tự>
        if id_acc != id_create[0:id_create_len - 2]:
            return {'message': "Wrong format <id> plus two digit"}, 400

        # chống tạo tài khoản trùng
        exist_check = AccountDb.find_by_id(accId=id_create)
        if exist_check:
            return {'message': "Account already existed"}, 400

        try:
            password = random_string()
            msg = Message('Your account information', sender='phucpb.hrt@gmail.com', recipients=[email_create.lower()])
            msg.body = 'Your id is {f_id} and your password is {f_pass}'.format(f_id=id_create, f_pass=password)
            my_mail.send(msg)
            new_account = AccountDb(AccountId=id_create, Password=generate_password_hash(password, method='sha256'),
                                    email=email_create, RoleId=int(role_acc['role']) + 1, manager_account=id_acc,
                                    isLocked=0)
            new_account.save_to_db()
            return {'message': "New account sent to user's mailbox!"}, 200
        except Exception as e:
            print(e)
            return {'messsage': 'Something wrong happened'}, 500


class AccountManagementChange(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('password', type=str)
    parser.add_argument('email', type=str)
    parser.add_argument('StartDate')
    parser.add_argument('EndDate')
    parser.add_argument('isLocked', type=bool)

    @jwt_required()
    @authorized_required(roles=[0, 1, 2, 3, 4])
    def get(self, id):
        id_acc = get_jwt_identity()
        try:
            specific_account = AccountDb.find_by_id(id)
            if specific_account:
                if specific_account.managerAccount != id_acc:
                    return {"message": "not authorized"}, 403
                return specific_account.json(), 200
        except:
            return {"message": "Not found"}, 404

    @jwt_required()
    @authorized_required(roles=[0, 1, 2, 3, 4])
    @crud_permission_required
    def put(self, id):
        data = AccountManagementChange.parser.parse_args()
        id_acc = get_jwt_identity()
        id_modify = id
        password_modify = data['password']
        email_modify = data['email']
        is_locked_modify = data['isLocked']
        try:
            start_date_modify = datetime.strptime(data['StartDate'], '%Y-%m-%d').date()
            # start_date_modify = data['StartDate']
            end_date_modify = datetime.strptime(data['EndDate'], '%Y-%m-%d').date()
            # end_date_modify = data['EndDate']
        except:
            return {'message': "invalid input"}, 400

        # validate
        data_ok = True
        if password_modify is not None:
            data_ok = AccountService.check_password(password_modify)

        if email_modify is not None:
            data_ok = AccountService.validate_email(email_modify)

        # ensure (!startDate AND !endDate) OR (startDate AND endDate)
        if ((start_date_modify is not None and end_date_modify is None) or
                (start_date_modify is None and end_date_modify is not None)):
            data_ok = False
        elif start_date_modify is not None and end_date_modify is not None:
            if start_date_modify > end_date_modify:
                data_ok = False

        # hợp lệ thời gian khai báo với tài khoản cha
        parent_user = AccountDb.find_by_id(id_acc)
        if parent_user is None:
            return {'message': "something went wrong"}, 500

        # ensure CRUD period of child account is valid with this account (parent account)
        # child.startDate > parent.startDate AND child.endDate < parent.endDate
        if parent_user.startDate is not None and parent_user.endDate is not None:
            if parent_user.startDate > start_date_modify or parent_user.endDate < end_date_modify:
                data_ok = False

        if not data_ok:
            return {'message': "invalid input"}, 400

        current_user = AccountDb.find_by_id(id_modify)
        if current_user is None:
            return {'message': "invalid input"}, 400
        elif current_user.managerAccount != id_acc:
            return {"message": "not authorized"}, 403

        if password_modify is not None:
            current_user.password = generate_password_hash(password_modify, method='sha256')
        if email_modify is not None:
            current_user.email = email_modify
        if start_date_modify is not None:
            current_user.startDate = start_date_modify
            current_user.endDate = end_date_modify
        if is_locked_modify is not None:
            current_user.isLocked = is_locked_modify
            current_user.startDate = None
            current_user.endDate = None
            if is_locked_modify:
                try:
                    AccountDb.lock_managed_account_hierachy(id_modify)
                except Exception as e:
                    print(e)
                    return {"message": "something wrong"}, 500

        try:
            current_user.commit_to_db() # need to recheck
            return {"message": "done"}, 200
        except:
            return {"message": "something wrong"}, 500

    @jwt_required()
    @authorized_required(roles=[0, 1, 2, 3, 4])
    @crud_permission_required
    def delete(self, id):
        id_acc = get_jwt_identity()
        id_delete = id
        current_user = AccountDb.find_by_id(id_delete)

        if current_user is None:
            return {'message': "invalid input"}, 400
        elif current_user.managerAccount != id_acc:
            return {"message": "not authorized"}, 403

        try:
            try:
                AccountDb.delete_managed_account_hierachy(id_delete)
            except Exception as e:
                print(e)
                return {"message": "something wrong"}, 500
            current_user.delete_from_db()  # need to recheck
            return {"message": "done"}, 200
        except Exception as e:
            print(e)
            return {"message": "something wrong"}, 500
