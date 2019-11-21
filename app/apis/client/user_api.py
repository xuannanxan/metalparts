from flask_restful import Resource,reqparse,fields,marshal,abort
from app.models.client import User
from app.apis.api_constant import *

parse = reqparse.RequestParser()
parse.add_argument('username',type=str,required=True,help='请输入用户名')
parse.add_argument('password',type=str,required=True,help='请输入密码')
parse.add_argument('email',type=str,required=True,help='请输入邮箱地址')
parse.add_argument('phone',type=str,required=True,help='请输入手机号码')

user_fields = {
    'username':fields.String,
    'email':fields.String,
    'phone':fields.String
}

sing_user_fields = {
    'status':fields.Integer,
    'msg':fields.String,
    'data':fields.Nested(user_fields)
}

class UsersResource(Resource):
    def post(self):
        args = parse.parse_args()
        username = args.get('username')
        password = args.get('password')
        email = args.get('email')
        phone = args.get('phone')
        user = User()
        user.set_attrs(args)
        if user.add():
            data = {
                'status':HTTP_CREATE_OK,
                'msg':'新增成功',
                'data':user
            }
            return marshal(data,sing_user_fields)
        abort(400,msg='新增失败')
        