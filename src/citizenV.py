from flask_restful import Api
from flask import Flask

from src.controller.account import Account, Register, Confirmation, Repass, ChangePass, UserLogoutAccess
from src.controller.cityProvince import City,Cities
from src.controller.district import District, Districts
from src.controller.ward import Ward,Wards
from src.controller.residentialGroup import Group,Groups

from src import controller

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/citizen'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_pyfile('core/config.py')

api = Api(app)
controller.init_app(app)

api.add_resource(Account, '/login')
api.add_resource(Register, '/register')
api.add_resource(Confirmation, '/confirm_email/<token>')
api.add_resource(Repass, '/repass')
api.add_resource(ChangePass, '/changepass')
api.add_resource(UserLogoutAccess, '/logout')

# Tỉnh/thành phố
api.add_resource(City, '/city', '/city/<string:name>')
api.add_resource(Cities, '/cities')

# Quận/huyện
api.add_resource(District, '/district', '/district/<string:Cname>/<string:Dname>')
api.add_resource(Districts, '/districts/<string:name>')

# Xã/phường
api.add_resource(Ward, '/ward', '/ward/<string:Dname>/<string:Wname>')
api.add_resource(Wards, '/wards/<string:name>')

# Thôn/bản/tdp
api.add_resource(Group, '/group', '/group/<string:Wname>/<string:Gname>')
api.add_resource(Groups, '/groups/<string:name>')
@controller.jwt_manager.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):

    jti = decrypted_token['jti']

    return controller.account.RevokedTokenModel.is_jti_blacklisted(jti)


if __name__ == '__main__':
    from database import db
    db.init_app(app)
    app.run(debug=True)
