from flask import Flask, request, jsonify, make_response, request
import jwt
from flask_jwt_extended import jwt_required, current_user, get_jwt_identity, get_raw_jwt
from functools import wraps
from ..models.accountDb import AccountDb
# su = 'Thisisasecret!'
#
#
# def token_required(func):
#     # decorator factory which invoks update_wrapper() method and passes decorated function as an argument
#     @wraps(func)
#     def decorated(*args, **kwargs):
#         token = request.args.get('token')
#         if not token:
#             return jsonify({'Alert!': 'Token is missing!'}), 401
#
#         try:
#
#             data = jwt.decode(token, su)
#         # You can use the JWT errors in exception
#         # except jwt.InvalidTokenError:
#         #     return 'Invalid token. Please log in again.'
#         except:
#             return jsonify({'Message': 'Invalid token'}), 403
#         return func(*args, **kwargs)
#     return decorated


@jwt_required()
def get_id_from_jwt_token():
    id = get_jwt_identity()
    return id


def authorized_required(func, roles):
    @wraps(func)
    def decorated(*args, **kwargs):
        try:
            user_id = get_id_from_jwt_token()
            user = AccountDb.find_by_id(user_id)
            ok = False
            for x in roles:
                if user.roleId == x:
                    ok = True
            if not ok:
                raise Exception()
        except:
            return {'message': "You are not authorized to perform this activity"}, 403
        return func(*args, **kwargs)
    return decorated


def crud_permission_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        try:
            user_id = get_id_from_jwt_token()
            user = AccountDb.find_by_id(user_id)
            if user.isLocked:
                raise Exception()
        except:
            return {'message': "You are not authorized to perform this activity"}, 403
        return func(*args, **kwargs)
    return decorated
