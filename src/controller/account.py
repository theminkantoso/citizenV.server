from flask_restful import Resource, reqparse
from src.models.accountDb import AccountDb, RevokedTokenModel
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from src.controller import my_mail
from flask import url_for, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask_mail import Message
from src.models.cityProvinceDb import CityDb
from src.models.districtDb import DistrictDb
from src.models.wardDb import WardDb
from src.models.residentialGroupDb import GroupDb

import json
import re
import random
import string


def random_string():
    """
    Generate a random password
    :return: a random string with 6 letters and 6 numbers
    """
    str1 = ''.join((random.choice(string.ascii_letters) for x in range(6)))
    str1 += ''.join((random.choice(string.digits) for x in range(6)))

    sam_list = list(str1)
    random.shuffle(sam_list)
    final_string = ''.join(sam_list)
    return final_string


def validate_regex(input_string, regex):
    """
    Validate input string based on a given regex
    :param input_string: string needs to check
    :param regex: regex pattern
    :return: True if satisfied
    """
    pattern = re.compile(regex)
    if pattern.fullmatch(input_string):
        return True
    return False


class Account(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=str)
    parser.add_argument('password', type=str)

    def get(self):
        pass
        # args = request.args
        # print(args['a'])  # For debugging

    def post(self):
        data = Account.parser.parse_args()
        id = data['id']
        password = data['password']

        # validate
        regex_id = '^[0-9]*$'
        if not validate_regex(id, regex_id) or not password.isalnum() or len(id) % 2 != 0:
            return {'message': "Invalid id or password"}, 400

        user = AccountDb.find_by_id(id)

        if user is None:
            return {'message': "Incorrect id or password"}, 401

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
            name = city + '-' + dist
        elif user.roleId == 4:
            ward = WardDb.find_by_id(user.accountId).wardName
            dist = DistrictDb.find_by_id(user.accountId[0:4]).districtName
            city = CityDb.find_by_id(user.accountId[0:2]).cityProvinceName
            name = city + '-' + dist + '-' + ward

        elif user.roleId == 5:
            group = GroupDb.find_by_id(user.accountId).groupName
            ward = WardDb.find_by_id(user.accountId[0:6]).wardName
            dist = DistrictDb.find_by_id(user.accountId[0:4]).districtName
            city = CityDb.find_by_id(user.accountId[0:2]).cityProvinceName
            name = city + '-' + dist + '-' + ward + '-' + group
        if check_password_hash(user.password, password):
            additional_claim = {"role": user.roleId, "isLocked": user.isLocked, "name": name}
            access_token = create_access_token(identity=id, additional_claims=additional_claim)

            # update khóa tài khoản
            # do server không phải chạy 24/24 nên khi đăng nhập server sẽ kiểm tra có khóa tài khoản không
            # kiểm tra thời gian hiện tại với thời gian tài khoản được thêm sửa xóa
            today = date.today()
            if user.startTime is not None and user.endTime is not None:
                if user.startTime <= today <= user.endTime:
                    user.isLocked = False
                    user.commit_to_db()
                else:
                    user.isLocked = True
                    # khóa tài khoản con
                    try:
                        AccountDb.lock_managed_account_hierachy(id)
                    except Exception as e:
                        print(e)

            # return jwt to FE
            try:
                return jsonify(access_token=access_token.decode('utf-8'))
            except:
                return jsonify(access_token=access_token)

        return {"message": "Incorrect username or password"}, 401

    def delete(self):
        return {'message': 'Not allowed'}, 404

    def put(self):
        return {'message': 'Not allowed'}, 404


# class Register(Resource):
#     parser = reqparse.RequestParser()
#     parser.add_argument('email', type=str)
#     parser.add_argument('password', type=str)
#
#
#     def get(self):
#         pass
#
#     def post(self):
#         data = Register.parser.parse_args()
#         email = data['email']
#         password = data['password']
#         user = AccountDb(AccountId=email, Password=generate_password_hash(password, method='sha256'), RoleId=0,
#                          isLocked=0)
#         user.save_to_db()
#         return {'message': "Login success"}, 200
#
#     def delete(self):
#         return {'message': 'Not allowed'}, 404
#
#     def put(self):
#         return {'message': 'Not allowed'}, 404


class Repass(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=str)
    parser.add_argument('email', type=str)

    def post(self):
        data = Repass.parser.parse_args()
        id = data['id']
        email = data['email']

        # validate
        regex_id = '^[0-9]*$'
        regex_mail = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not validate_regex(input_string=email.lower(), regex=regex_mail) \
                or not validate_regex(input_string=id, regex=regex_id) \
                or len(id) % 2 != 0:
            return {'message': "Check your id or email"}, 400

        get_user = AccountDb.find_by_email(email, id)
        if get_user is None:
            return {'message': "No account with this email and id"}, 400
        try:
            new_password = random_string()
            # gửi mail mật khẩu mới cho người dùng
            get_user.password = generate_password_hash(new_password, method='sha256')
            msg = Message('New Password Recovery', sender='phucpb.hrt@gmail.com', recipients=[email.lower()])
            msg.body = 'Your new password is {}'.format(new_password)
            my_mail.send(msg)
            get_user.commit_to_db()
        except:
            return {'message': "Unable to send confirmation mail"}, 400
        return {'message': "New password sent to your mailbox!"}, 200


class ChangePass(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('password', type=str)
    parser.add_argument('newpassword', type=str)

    @jwt_required()
    def post(self):
        data = ChangePass.parser.parse_args()
        password = data['password']
        new_password = data['newpassword']

        # validate
        if not password.isalnum() or not new_password.isalnum() or len(new_password) == 0:
            return {'message': "Wrong input format"}, 400

        id = get_jwt_identity()
        get_user = AccountDb.find_by_id(id)
        if check_password_hash(get_user.password, password):
            get_user.password = generate_password_hash(new_password, method='sha256')
            get_user.save_to_db()
            return {'message': "New password saved succeed!"}, 200
        return {'message': "Wrong password"}, 400


class UserLogoutAccess(Resource):
    """
    User Logout Api
    """

    @jwt_required()
    def post(self):

        jti = get_jwt()['jti']
        try:
            # Revoking access token
            revoked_token = RevokedTokenModel(jti=jti)

            revoked_token.add()

            return {'message': 'Access token has been revoked'}, 200

        except:
            return {'message': 'Something went wrong'}, 500



