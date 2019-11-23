from app.models.client import User
from flask import request,g
from flask_restful import abort
from app.ext import cache

def get_user(ident):
    '''
    通过ID，用户名，邮箱，手机号码识别用户
    '''
    if not ident:
        return None
    user = User.query.get(ident)
    if user:
        return user
    user = User.query.filter(User.username == ident).first()
    if user:
        return user
    user = User.query.filter(User.phone == ident).first()
    if user:
        return user
    user = User.query.filter(User.email == ident).first()
    if user:
        return user
    return None

def _verify():
    token = request.args.get('token')
    if not token:
        abort(401,msg='请登录')
    user_id = cache.get(token)
    if not user_id:
        abort(401,msg='请重新登录')
    user = get_user(user_id)
    if not user:
        abort(401,msg='请重新登录')
    g.user = user
    g.auth = token    

def login_required(fun):
    '''
    登录的装饰器，需要登录才能进行访问
    '''
    def wrapper(*args,**kwargs):
        _verify()
        return fun(*args,**kwargs)
    return wrapper

def permission_required(permission):
    def permission_required_wrapper(fun):
        def wrapper(*args,**kwargs):
            _verify()
            if not g.user.check_permission(permission):
                abort(403,msg='权限不足')
            return fun(*args,**kwargs)
        return wrapper
    return permission_required_wrapper
    pass