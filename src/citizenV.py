from flask_restful import Api
from flask import Flask
from flask_cors import CORS

from src.controller.account import Account, Repass, ChangePass, UserLogoutAccess
from src.controller.cityProvince import City, Cities, all_Cities
from src.controller.district import District, Districts, all_Districts_in_area
from src.controller.ward import Ward, Wards, WardCompleted, all_Wards_in_area
from src.controller.residentialGroup import Group, Groups, all_groups_in_area
from src.controller.account_management import AccountManagement, AccountManagementChange
from src.controller.citizen import Citizen, add_Citizen, all_Citizen, all_Citizen_Area, citizen_by_group_areas
from src.controller.progress import Progress, ProgressSpecific
from src.controller.statistics import Statistics, StatisticsSpecific
from src.controller.file import File
from src.controller.excel import TestExcel


from src import services, controller

app = Flask(__name__)
CORS(app)
app.config.from_pyfile('core/config.py')

api = Api(app)
services.init_app(app)
controller.init_app(app)

api.add_resource(Account, '/login')
api.add_resource(Repass, '/repass')
api.add_resource(ChangePass, '/changepass')
api.add_resource(UserLogoutAccess, '/logout')

# Tỉnh/thành phố
api.add_resource(City, '/city', '/city/<string:city_id>')
api.add_resource(Cities, '/cities')
api.add_resource(all_Cities, '/cities/<string:acc_id>')

# Quận/huyện
api.add_resource(District, '/district', '/district/<string:dist_id>')
api.add_resource(Districts, '/districts')
api.add_resource(all_Districts_in_area, '/districts/<string:city_id>')

# Xã/phường
api.add_resource(Ward, '/ward', '/ward/<string:ward_id>')
api.add_resource(Wards, '/wards')
api.add_resource(all_Wards_in_area, '/wards/<string:dist_id>')
api.add_resource(WardCompleted, '/wardCompleted')


# Thôn/bản/tdp
api.add_resource(Group, '/group', '/group/<string:group_id>')
api.add_resource(Groups, '/groups')
api.add_resource(all_groups_in_area,  '/groups/<string:ward_id>')

# Màn hình quản lý tài khoản
api.add_resource(AccountManagement, '/accounts')
api.add_resource(AccountManagementChange, '/accounts/<string:id>')

# Người dân
api.add_resource(Citizen, '/citizen', '/citizen/<string:citizen_id>')
api.add_resource(add_Citizen, '/citizen/<string:group_id>')
api.add_resource(all_Citizen, '/citizens')
api.add_resource(citizen_by_group_areas, '/citizens_areas/<string:spArea_id>')
api.add_resource(all_Citizen_Area, '/citizens/<string:area_id>')

# Progress
api.add_resource(Progress, '/progress')
api.add_resource(ProgressSpecific, '/progress/<string:id>')

# Statistics
api.add_resource(Statistics, '/statistics')
api.add_resource(StatisticsSpecific, '/statistics/<string:id>')

# file
api.add_resource(File, '/file')

api.add_resource(TestExcel, '/excel')


@controller.jwt_manager.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = db.session.query(controller.account.RevokedTokenModel.id).filter_by(jti=jti).scalar()
    return token is not None


if __name__ == '__main__':
    from database import db

    db.init_app(app)
    app.run(debug=True)
