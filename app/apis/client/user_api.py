from flask_restful import Resource,reqparse,fields,marshal,abort
from app.models.client import User
from app.apis.api_constant import *
from app.apis.client.model_utils import get_user
import uuid
from flask_cache import Cache

parse_base = reqparse.RequestParser()
parse_base.add_argument('password',type=str,required=True,help='请输入密码')
parse_base.add_argument('action',type=str,required=True,help='请确认请求参数')

parse_register = parse_base.copy()
parse_register.add_argument('username',type=str,required=True,help='请输入用户名')
parse_register.add_argument('email',type=str,required=True,help='请输入邮箱地址')
parse_register.add_argument('phone',type=str,required=True,help='请输入手机号码')

parse_login = parse_base.copy()
parse_login.add_argument('username',type=str,required=True,help='请输入用户名/邮箱/手机')


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
        args = parse_base.parse_args()
        password = args.get('password')
        action = args.get('action').lower()
        # 注册
        if action == USER_ACTION_REGISTER:
            args_register = parse_register.parse_args()
            username = args_register.get('username').lower()
            email = args_register.get('email')
            phone = args_register.get('phone')
            if get_user(username):
                abort(400,msg='用户名已注册')
            if get_user(phone):
                abort(400,msg='手机号码已注册')
            if get_user(email):
                abort(400,msg='邮箱已注册')
            user = User()
            user.username = username
            user.password = password
            user.email = email
            user.phone = phone
            if user.add():
                data = {
                    'status':HTTP_CREATE_OK,
                    'msg':'新增成功',
                    'data':user
                }
                return marshal(data,sing_user_fields)
            abort(400,msg='新增失败')
        # 登录
        elif action == USER_ACTION_LOGIN:
            args_login = parse_login.parse_args()
            username = args_login.get('username').lower()
            user = get_user(username) 
            if not user:
                abort(400,msg='用户名或密码错误')
            if (not user.check_pwd(password)) or user.is_del != '0':
                abort(401,msg='用户名或密码错误')
            token = uuid.uuid4().hex
            Cache.set(token,user.id,timeout=60*60*7)
            data = {
                'status':HTTP_OK,
                'msg':'登录成功',
                'token':token
            }
        else:
            abort(400,msg='参数错误，请检查后重试')
        
        