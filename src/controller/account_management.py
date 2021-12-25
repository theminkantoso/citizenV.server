from flask_restful import Resource, reqparse
from src.models.accountDb import AccountDb
from src.services.accountService import AccountService
from src.core.auth import crud_permission_required, authorized_required
from werkzeug.security import generate_password_hash
from datetime import datetime, date
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
        acc = get_jwt()
        managed_accounts = AccountDb.find_managed_account_by_id(id_acc)  # Tất cả người dùng dưới quyền quản lý
        if managed_accounts:
            accounts = AccountService.join_area_account(acc, managed_accounts, id_acc)
            return {"Accounts": accounts}, 200
        return {}, 200

    @jwt_required()
    @authorized_required(roles=[0, 1, 2, 3, 4])
    @crud_permission_required
    def post(self):
        data = AccountManagement.parser.parse_args()
        id_acc = get_jwt_identity()
        role_acc = get_jwt()
        id_create = data['id']
        email_create = data['email']

        # validate input
        if not AccountService.validate_input_id_email_create(id_create, email_create):
            return {'message': "Invalid input format"}, 400

        # prevent creating a trash account where id does not match any location
        if not AccountService.prevent_trash_account(id_create):
            return {'message': "This is a trash account"}, 400

        # check tk phải có id đúng format <tkcha> + <2 ký tự>
        id_create_len = len(id_create)
        if not AccountService.check_format_id_plus_2(id_acc, id_create, id_create_len) and role_acc['role'] != 0:
            return {'message': "Wrong format <id> plus two digit"}, 400

        # prevent duplicate account
        if not AccountService.find_duplicate(id_create):
            return {'message': "Account already existed"}, 400

        try:
            password = AccountService.random_string()

            # send email to user, including id and default password
            msg = Message('Your account information', sender='phucpb.hrt@gmail.com', recipients=[email_create.lower()])
            msg.body = 'Your id is {f_id} and your password is {f_pass}'.format(f_id=id_create, f_pass=password)
            my_mail.send(msg)
            new_account = AccountDb(AccountId=id_create, Password=generate_password_hash(password, method='sha256'),
                                    email=email_create, RoleId=int(role_acc['role']) + 1, manager_account=id_acc,
                                    isLocked=1)
            new_account.save_to_db()
            return {'message': "New account sent to user's mailbox!"}, 200
        except Exception as e:
            print(e)
            return {'messsage': 'Something wrong happened'}, 500


class AccountManagementChange(Resource):
    parser = reqparse.RequestParser()
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
        email_modify = data['email']
        is_locked_modify = data['isLocked']
        start_date_modify = data['StartDate']
        end_date_modify = data['EndDate']

        # validate input
        data_ok = True

        # ensure (!startDate AND !endDate) OR (startDate AND endDate)
        if ((start_date_modify is not None and end_date_modify is None) or
                (start_date_modify is None and end_date_modify is not None)):
            data_ok = AccountService.validate_email(email_modify)

        # ensure (!startDate AND !endDate) OR (startDate AND endDate)
        if ((start_date_modify is not None and end_date_modify is None) or
                (start_date_modify is None and end_date_modify is not None)):
            data_ok = False

        if not data_ok:
            return {'message': "invalid input"}, 400

        if start_date_modify is not None and end_date_modify is not None:
            try:
                start_date_modify = datetime.strptime(data['StartDate'], '%Y-%m-%d').date()
                end_date_modify = datetime.strptime(data['EndDate'], '%Y-%m-%d').date()
            except:
                return {'message': "invalid input"}, 400
            data_ok = AccountService.validate_period(start_date_modify, end_date_modify)

        # ensure CRUD period satisfy with parent's account CRUD period
        parent_user = AccountDb.find_by_id(id_acc)
        if parent_user is None:
            return {'message': "something went wrong"}, 500

        # ensure CRUD period of child account is valid with this account (parent account)
        # child.startDate > parent.startDate AND child.endDate < parent.endDate
        if parent_user.startDate is not None and parent_user.endDate is not None:
            if parent_user.startDate > start_date_modify or parent_user.endDate < end_date_modify:
                data_ok = False

        if not data_ok:
            return {'message': "Check your CRUD period again"}, 400

        # prevent one user access other resources
        current_user = AccountDb.find_by_id(id_modify)
        if current_user is None:
            return {'message': "invalid input"}, 400
        elif current_user.managerAccount != id_acc and len(id_acc) != 1:
            return {"message": "not authorized"}, 403
        if email_modify is not None:
            current_user.email = email_modify
        if start_date_modify is not None:
            current_user.startDate = start_date_modify
            current_user.endDate = end_date_modify
            today = date.today()
            if current_user.startDate <= today <= current_user.endDate:
                current_user.isLocked = False
        if is_locked_modify is not None:
            if is_locked_modify:
                current_user.isLocked = is_locked_modify
                current_user.startDate = None
                current_user.endDate = None
                try:
                    AccountDb.lock_managed_account_hierachy(id_modify)
                except Exception as e:
                    print(e)
                    return {"message": "something wrong"}, 500
            if current_user.startDate is None and current_user.isLocked and not is_locked_modify:
                return {"message": "you must update startDate and endDate to unLock"}, 400
        try:
            current_user.commit_to_db()  # need to recheck
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
