# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-26.
__author__ = 'Allen xu'
from  app.models import db,BaseModel

# 管理员登录日志
class Adminlog(BaseModel):
    __tablename__ = "adminlog"
    admin_id = db.Column(db.Integer)
    ip = db.Column(db.String(100))
    info = db.Column(db.String(255))

    def __repr__(self):
        return '<Adminlog %r>' % self.id


# 管理员操作日志
class Operationlog(BaseModel):
    __tablename__ = "operationlog"
    admin_id = db.Column(db.Integer)
    ip = db.Column(db.String(100))
    info = db.Column(db.String(255))  # 操作原因

    def __repr__(self):
        return '<Operationlog %r>' % self.id

# 会员登录日志
class Userlog(BaseModel):
    __tablename__ = "userlog"
    user_id = db.Column(db.Integer)
    ip = db.Column(db.String(100))
    info = db.Column(db.String(255))
    
    def __repr__(self):
        return '<Userlog %r>' % self.id
