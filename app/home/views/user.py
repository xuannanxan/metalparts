# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-26.
__author__ = 'Allen xu'
from flask import  request,jsonify,render_template
from flask_login import login_required
from app.expand.utils import object_to_dict
from app.home.forms import RegisterForm
from app.models import User,Crud
from flask_login import login_user, login_required, logout_user, current_user
from app.ext import login_manager
from app.home import home

# 添加管理员
@home.route("/register", methods=["POST"])
def register():
    data = request.form
    if data["password"] != data["rpassword"]:
        return {"code": 0, "msg": '两次输入的密码不一致'} 
    form = RegisterForm(data)
    if form.validate():
        result = Crud.add(User,data,"email")
        if result:
            #op_log("用户注册-%s" % data["email"])
            return {"code": 1, "msg": "注册成功，您的登录邮箱为-%s" % data["email"]}    
        return {"code": 0, "msg": '注册失败，用户已存在'}    
    return {"code": 0, "msg": form.get_errors()}