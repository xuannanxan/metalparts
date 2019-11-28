#!/usr/bin/env python
# coding=utf-8
'''
@Description: 
@Author: Xuannan
@Date: 2019-11-25 09:14:35
@LastEditTime: 2019-11-28 17:45:18
@LastEditors: Xuannan
'''


import uuid
from datetime import datetime
from flask import current_app
from app.ext import db

class BaseModel(db.Model):
    #不需要创建base表
    __abstract__ = True
    #所有模型继承的字段
    id = db.Column(db.String(32),primary_key=True,default=uuid.uuid4().hex)
    create_time = db.Column(db.DateTime, nullable=True,default=datetime.now)
    update_time = db.Column(db.DateTime, nullable=True, default=datetime.now, onupdate=datetime.now)  # 记录的更新时间
    is_del = db.Column(db.String(32), default=0)  # 状态，0为未删除，其他为已删除


    def set_attrs(self,attrs_dict):
        for key,value in attrs_dict.items():
            if hasattr(self,key) and key != "id":
                setattr(self,key,value)
        # setattr(self,'create_time',datetime.now)

    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(e)
            current_app.logger.error(e)
            return False

    def updata(self):
        try:
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(e)
            current_app.logger.error(e)
            return False

    def clean(self):
        '''
        清除数据，物理删除，谨慎操作
        '''
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(e)
            current_app.logger.error(e)
            return False

    def delete(self):
        '''
        逻辑删除
        '''
        try:
            self.is_del = self.id
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(e)
            current_app.logger.error(e)
            return False

