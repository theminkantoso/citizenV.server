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
from flask import url_for, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask_mail import Message


class AccountManagement(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=str)
    parser.add_argument('email', type=str)

    @jwt_required()
    @authorized_required(roles=[0, 1, 2, 3, 4])
    def get(self):
        # id_acc = get_jwt_identity()
        # acc = AccountDb.find_by_id(id_acc)
        # managed_accounts = AccountDb.find_managed_account_by_id(id_acc)  # Tất cả người dùng dưới quyền quản lý
        # if managed_accounts:
        #     k = []
        #     if acc.roleId == 0:  # Tất cả người dùng A1
        #         return {'Accounts': list(map(lambda x: x.json(), managed_accounts))}, 200
        #     # Cho A1, A2, A3, B1
        #     acc_join = AccountDb.join_areaId(acc.roleId)   # join để lấy id của các vùng
        #     for i in range(len(acc_join)):
        #         areaId = ""
        #         if acc.roleId == 1:
        #             areaId = acc_join[i][0].cityProvinceId  # Id của các thành phố
        #         elif acc.roleId == 2:
        #             areaId = acc_join[i][0].districtId  # Id của các quận/huyện
        #         elif acc.roleId == 3:
        #             areaId = acc_join[i][0].wardId  # Id của các xã/phường
        #         elif acc.roleId == 4:
        #             areaId = acc_join[i][0].groupId  # Id của các thôn/bản/tdp
        #         k.append(AccountDb.json1(acc_join[i][1], areaId))
        #     return {"areas": k}, 200
        # return {}, 200
        id_acc = get_jwt_identity()
        managed_accounts = AccountDb.find_managed_account_by_id(id_acc)
        if managed_accounts:
            return {'Accounts': list(map(lambda x: x.json(), managed_accounts))}, 200
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
        if not AccountService.check_format_id_plus_2(id_acc, id_create, id_create_len):
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
        start_date_modify = data['StartDate']
        end_date_modify = data['EndDate']
        # if data['StartDate'] and data['EndDate']:
        #     try:
        #         start_date_modify = datetime.strptime(data['StartDate'], '%Y-%m-%d').date()
        #         # start_date_modify = data['StartDate']
        #         end_date_modify = datetime.strptime(data['EndDate'], '%Y-%m-%d').date()
        #         # end_date_modify = data['EndDate']
        #     except:
        #         return {'message': "invalid input"}, 400

        # validate input
        data_ok = True
        if password_modify is not None:
            data_ok = AccountService.check_password(password_modify)

        if email_modify is not None:
            data_ok = AccountService.validate_email(email_modify)

        # ensure (!startDate AND !endDate) OR (startDate AND endDate)
        if ((start_date_modify is not None and end_date_modify is None) or
                (start_date_modify is None and end_date_modify is not None)):
            data_ok = False

        if not data_ok:
            return {'message': "invalid input"}, 400

        if start_date_modify is not None and end_date_modify is not None:
            data_ok = AccountService.validate_period(start_date_modify, end_date_modify)

        # ensure CRUD period satisfy with parent's account CRUD period
        parent_user = AccountDb.find_by_id(id_acc)
        if parent_user is None:
            return {'message': "something went wrong"}, 500

        # ensure CRUD period of child account is valid with this account (parent account)
        # child.startDate > parent.startDate AND child.endDate < parent.endDate
        if parent_user.startDate is not None and parent_user.endDate is not None:
            try:
                start_date_modify = datetime.strptime(data['StartDate'], '%Y-%m-%d').date()
                # start_date_modify = data['StartDate']
                end_date_modify = datetime.strptime(data['EndDate'], '%Y-%m-%d').date()
                # end_date_modify = data['EndDate']
            except:
                return {'message': "invalid input"}, 400
            if parent_user.startDate > start_date_modify or parent_user.endDate < end_date_modify:
                data_ok = False

        if not data_ok:
            return {'message': "Check your CRUD period again"}, 400

        # prevent one user access other resources
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
