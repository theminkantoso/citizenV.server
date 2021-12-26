from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps
from ..models.accountDb import AccountDb


@jwt_required()
def get_id_from_jwt_token():
    """
    Get user's id based on the jwt
    :return: user's id
    """
    id = get_jwt_identity()
    return id


def authorized_required(roles):
    """
    Authorization control access based on user role
    :param roles: list roles allowed
    :return: 403 if user's role is not in the permission list, else allow them to proceed
    """
    def decor(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            try:
                user_id = get_id_from_jwt_token()
                user = AccountDb.find_by_id(user_id)
                ok = False
                for x in roles:
                    if user.roleId == x:
                        ok = True
                        break
                if not ok:
                    raise Exception()
            except:
                return {'msg': "You are not authorized to perform this activity"}, 403
            return func(*args, **kwargs)
        return decorated
    return decor


def crud_permission_required(func):
    """
    Only allow user to CUD data in their limit time
    :param func: wrapper function
    :return: 403 if the account is locked, else allow them to proceed
    """
    @wraps(func)
    def decorated(*args, **kwargs):
        try:
            user_id = get_id_from_jwt_token()
            user = AccountDb.find_by_id(user_id)
            if user.isLocked:
                raise Exception()
        except:
            return {'msg': "You are not authorized to edit"}, 403
        return func(*args, **kwargs)
    return decorated
