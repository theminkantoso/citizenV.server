from flask_restful import Resource, reqparse
from src.models.accountDb import AccountDb, RevokedTokenModel
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from src.services import my_mail
from flask import jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask_mail import Message
from src.services.accountService import AccountService

class Account(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=str)
    parser.add_argument('password', type=str)

    def get(self):
        pass
        # args = request.args
        # print(args['a'])  # For debugging
        # a = CityDb.find_join_account()
        # k = []
        # for i in range(len(a)):
        #     print(type(CityDb.json2(a[i])))
        #     k.append(CityDb.json2(a[i]))
        # print(k)
        # return {"a": k}, 200
        # print(CityDb.count_total(), CityDb.count_completed())
        # print(WardDb.count_completed('2901'), WardDb.count_total('2901'))
        # print(DistrictDb.count_completed('29'), DistrictDb.count_total('29'))
        # ak = AccountDb.get_email_user_manager('00','0003')
        # print(ak[0])

    def post(self):
        data = Account.parser.parse_args()
        id = data['id']
        password = data['password']

        # validate input
        if not AccountService.validate_input_id_pass(id, password):
            return {'message': "Invalid id or password"}, 400

        user = AccountDb.find_by_id(id)

        if user is None:
            return {'message': "Incorrect id or password"}, 401

        name = AccountService.area_name_of_acc(user)

        if check_password_hash(user.password, password):
            # additional_claim = {"role": user.roleId, "isLocked": user.isLocked}
            additional_claim = {"role": user.roleId, "isLocked": user.isLocked, "name": name}
            access_token = create_access_token(identity=id, additional_claims=additional_claim)

            # update khóa tài khoản
            # do server không phải chạy 24/24 nên khi đăng nhập server sẽ kiểm tra có khóa tài khoản không
            # kiểm tra thời gian hiện tại với thời gian tài khoản được thêm sửa xóa
            # Update lock CRUD permission
            # Since server cannot run continuously, we use alternative solution via check the period of the
            # logged in account when logging in.
            # This means the system does not lock CRUD permission automatically, but check when logging in and lock
            # if necessary.
            today = date.today()
            if user.startDate is not None and user.endDate is not None:
                if user.startDate <= today <= user.endDate:
                    user.isLocked = False
                    user.commit_to_db()
                else:
                    user.isLocked = True
                    # lock children accounts
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

        # validate input
        if not AccountService.validate_input_id_email(id, email):
            return {'message': "Check your id or email"}, 400

        get_user = AccountDb.find_by_email(email, id)
        if get_user is None:
            return {'message': "No account with this email and id"}, 400
        try:
            new_password = AccountService.random_string()
            # send new password to user
            get_user.password = generate_password_hash(new_password, method='sha256')
            msg = Message('New Password Recovery', sender='phucpb.hrt@gmail.com', recipients=[email.lower()])
            msg.body = 'Your new password is {}'.format(new_password)
            my_mail.send(msg)
            get_user.commit_to_db()
        except Exception as e:
            print(e)
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

        # validate input
        if not AccountService.validate_input_pass_newpass(password, new_password):
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



