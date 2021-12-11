from flask_restful import Resource, reqparse
from src.models.accountDb import AccountDb
from flask_jwt_extended import jwt_required, get_jwt_identity


class AccountManagement(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('email', type=str)

    @jwt_required()
    def get(self):
        id_acc = get_jwt_identity()
        managed_accounts = AccountDb.find_managed_account_by_id(id_acc)
        if managed_accounts:
            return {'Accounts': list(map(lambda x: x.json(), managed_accounts))}, 200
        return {}, 200

    # @jwt_required
    # def post(self):


class AccountManagementChange(Resource):
    # parser = reqparse.RequestParser()
    # parser.add_argument('id', type=int)
    # parser.add_argument('password', type=str)

    @jwt_required()
    def get(self, id):
        # id_acc = get_jwt_identity()
        try:
            specific_account = AccountDb.find_by_id(id)
            if specific_account:
                return specific_account.json(), 200
        except:
            return {"message": "Not found"}, 404

    # @jwt_required
    # def post(self):

