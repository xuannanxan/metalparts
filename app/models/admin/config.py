#!/usr/bin/env python
# coding=utf-8
'''
@Description: 
@Author: Xuannan
@Date: 2019-11-13 17:29:28
@LastEditTime: 2019-11-29 11:59:50
@LastEditors: Xuannan
'''
# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-26.
__author__ = 'Allen xu'
from  app.models import db, BaseModel


# 配置项
class Conf(BaseModel):
    __tablename__ = "conf"
    name = db.Column(db.String(100), nullable=False)
    ename = db.Column(db.String(100), nullable=False)
    type_id = db.Column(db.String(32), nullable=False) # 配置类型，如系统配置，站点配置
    field_id = db.Column(db.String(32), nullable=False)  # 字段类型，如文本，数字,文本域，下拉单选，下拉多选，图片，富文本
    placeholder = db.Column(db.String(100))
    optional_values = db.Column(db.Text) #可选值
    default_value = db.Column(db.Text)
    sort = db.Column(db.Integer, default=0)  # 排序

    def __repr__(self):
        return '<Conf %r>' % self.name

# 配置类型，如系统配置，站点配置
class ConfigType(BaseModel):
    __tablename__ = "config_type"
    name = db.Column(db.String(200),nullable=False)
    sort = db.Column(db.Integer, default=0)  # 排序
   

    def __repr__(self):
        return '<ConfigType %r>' % self.name