#!/usr/bin/env python
# coding=utf-8
'''
@Description: 
@Author: Xuannan
@Date: 2019-11-25 09:14:35
@LastEditTime: 2019-11-28 12:35:12
@LastEditors: Xuannan
'''

from app.models.base import BaseModel,db
from app.models.model_constant import *
from werkzeug.security import check_password_hash,generate_password_hash
from flask_login import UserMixin
# 会员的数据模型
class User(UserMixin,BaseModel):
    __tablename__ = "user"  
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    _password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    phone = db.Column(db.String(100), unique=True)
    info = db.Column(db.Text)
    permission = db.Column(db.Integer, default=NOT_ACTIVE_USER)  # 用户权限
    profile = db.Column(db.String(255))
    address = db.Column(db.String(255))


    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        """
        读取属性
        :return:
        """
        raise Exception('密码无法直接访问')

    @password.setter
    def password(self,raw):
        """
        为password写入属性
        :param raw:明文密码
        :return:加密后的密码
        """
        self._password = generate_password_hash(raw)


    def check_pwd(self, raw):
        """
        密码验证
        :param raw:
        :return:
        """
        return check_password_hash(self._password, raw)
  
    def check_permission(self,permission):
        if (BLACK_USER & self.permission) == BLACK_USER:
            return False
        else:
            return permission & self.permission == permission

