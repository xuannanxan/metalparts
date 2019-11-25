# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-26.
__author__ = 'Allen xu'
from app.models import db,BaseModel
from app.expand.utils import diyId
# 企业的数据模型
class Company(BaseModel):
    __tablename__ = "company"
    email = db.Column(db.String(100), unique=True)
    aid = db.Column(db.String(255))  # 管理员用户
    name = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    info = db.Column(db.Text)
    status = db.Column(db.SmallInteger, default=1)  # 企业状态，第一位 1为已激活 0为禁用
    profile = db.Column(db.String(255))
    address = db.Column(db.String(255))


    def __repr__(self):
        return '<Company %r>' % self.name
    

