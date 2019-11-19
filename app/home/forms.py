# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-01.

from flask_wtf import FlaskForm
from wtforms import  StringField,PasswordField
from wtforms.validators import DataRequired,Email,Length

from app.expand.utils import error_to_string


# 邮箱表单，只用于验证
class MessageForm(FlaskForm):
    email = StringField(
            validators=[
                DataRequired("Please input your Email."),
                Email("Please input the correct Email.")
            ]
    )
    def get_errors(self):
        return error_to_string(self.errors.values())

# 修改密码表单，只用于验证
class UserChangePwdForm(FlaskForm):
    old_pwd = PasswordField(
            validators=[
                DataRequired("请输入原密码！"),
                Length(4, 20, "原密码长度错误！")]
    )
    password = PasswordField(
            validators=[
                DataRequired("请输入新密码！"),
                Length(4, 20, "新密码长度错误！")]
    )
    r_pwd = PasswordField(
            validators=[
               DataRequired("请重复新密码！"),
                Length(4, 20, "重复新密码长度错误！")]
    )

    def get_errors(self):
        return error_to_string(self.errors.values())

# 用户注册的表单，只用于验证
class RegisterForm(FlaskForm):
    email = StringField(
            validators=[
                DataRequired("请输入邮箱地址！"),
                Email( "邮箱格式错误！")]
    )
    password = PasswordField(
            validators=[
                DataRequired("密码不能为空！"),
                Length(4, 20, "密码长度错误！")]
    )


    def get_errors(self):
        return error_to_string(self.errors.values())