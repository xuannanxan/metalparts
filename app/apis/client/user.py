from flask_restful import Resource,reqparse,fields,marshal,abort,inputs
from app.models.client import User
from app.apis.api_constant import *
from app.apis.client.common import get_user,login_required,logout
import uuid
from app.ext import cache
from flask import g
from app.utils import object_to_json

parse_base = reqparse.RequestParser()
parse_base.add_argument('password',type=str,required=True,help='请输入密码')
parse_base.add_argument('action',type=str,required=True,help='请确认请求参数')
# 注册
parse_register = parse_base.copy()
parse_register.add_argument('username',type=str,required=True,help='请输入用户名')
parse_register.add_argument('email',type=str,required=True,help='请输入邮箱地址')
parse_register.add_argument('phone',type=inputs.regex(r'1[35789]\d{9}'),help='手机号码错误')
# 登录
parse_login = parse_base.copy()
parse_login.add_argument('username',type=str,required=True,help='请输入用户名/邮箱/手机')
# 修改密码
parse_change_pwd = parse_base.copy()
parse_change_pwd.add_argument('new_password',type=str,required=True,help='请输入新密码')

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
        """
        file: yml/register.yml
        """
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
                    'msg':'注册成功',
                    'data':user
                }
                return marshal(data,sing_user_fields)
            abort(400,msg='注册失败')
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
            cache.set(token,user.id,timeout=60*60*7)
            data = {
                'status':HTTP_OK,
                'msg':'登录成功',
                'token':token
            }
            return data
        else:
            abort(400,msg='参数错误，请检查后重试')

    @login_required
    def get(self):
        '''
        获取用户信息
        '''
        return object_to_json(g.user) 

    @login_required   
    def put(self):
        '''
        修改用户信息
        '''
        # 修改密码
        if action == USER_ACTION_CHANGE_PWD:
            args = parse_change_pwd.parse_args()
            password = args.get('password')
            new_password = args.get('new_password')
            action = args.get('action').lower()
            user = g.user
            if (not user.check_pwd(password)) or user.is_del != '0':
                abort(401,msg='用户名或密码错误')
            user.password = new_password
            if user.updata():
                logout()
                return  {
                    'status':HTTP_OK,
                    'msg':'修改成功',
                    }
            abort(400,msg='修改密码失败')
        # 修改用户信息
        elif action == USER_ACTION_CHANGE_INFO:
            
            pass


        
        