import os

from flask_restful import Resource, reqparse
from src.models.accountDb import AccountDb, RevokedTokenModel
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from src.services import my_mail
from flask import jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask_mail import Message
from src.services.accountService import AccountService
# from src.models.cityProvinceDb import CityDb
# from src.models.districtDb import DistrictDb
# from src.models.wardDb import WardDb
# from src.models.residentialGroupDb import GroupDb

# from src.models.citizenDb import CitizenDb


class Account(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=str)
    parser.add_argument('password', type=str)

    def get(self):
        # print(CitizenDb.get_population_cities([10, 11, 12]))
        pass

    def post(self):
        data = Account.parser.parse_args()
        id = data['id']
        password = data['password']

        # validate input
        if not AccountService.validate_input_id_pass(id, password):
            return {'msg': "Invalid id or password"}, 400

        user = AccountDb.find_by_id(id)

        if user is None:
            return {'msg': "Incorrect id or password"}, 401

        name = AccountService.area_name_of_acc(user)

        if check_password_hash(user.password, password):
            additional_claim = {"role": user.roleId, "isLocked": user.isLocked, "name": name}
            access_token = create_access_token(identity=id, additional_claims=additional_claim)

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

        return {"msg": "Incorrect username or password"}, 401

    def delete(self):
        return {'msg': 'Not allowed'}, 404

    def put(self):
        return {'msg': 'Not allowed'}, 404


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
            return {'msg': "Check your id or email"}, 400

        get_user = AccountDb.find_by_email(email, id)
        if get_user is None:
            return {'msg': "No account with this email and id"}, 400
        try:
            new_password = AccountService.random_string()
            # send new password to user
            get_user.password = generate_password_hash(new_password, method='sha256')
            msg = Message('New Password Recovery', sender=os.environ.get('MAIL'), recipients=[email.lower()])
            msg.body = 'Your new password is {}'.format(new_password)
            my_mail.send(msg)
            get_user.commit_to_db()
        except Exception as e:
            print(e)
            return {'msg': "Unable to send confirmation mail"}, 400
        return {'msg': "New password sent to your mailbox!"}, 200


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
            return {'msg': "Wrong input format"}, 400

        id = get_jwt_identity()
        get_user = AccountDb.find_by_id(id)
        if check_password_hash(get_user.password, password):
            get_user.password = generate_password_hash(new_password, method='sha256')
            get_user.save_to_db()
            return {'msg': "New password saved succeed!"}, 200
        return {'msg': "Wrong password"}, 400


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

            return {'msg': 'Access token has been revoked'}, 200

        except:
            return {'msg': 'Something went wrong'}, 500



