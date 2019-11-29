#!/usr/bin/env python
# coding=utf-8
'''
@Description: 
@Author: Xuannan
@Date: 2019-11-13 17:29:28
@LastEditTime: 2019-11-29 12:00:05
@LastEditors: Xuannan
'''

from  app.models import db,BaseModel
# 分类
class FieldType(BaseModel):
    __tablename__ = "field_type"
    name = db.Column(db.String(200),nullable=False)
    sort = db.Column(db.Integer, default=0)  # 排序
    

    def __repr__(self):
        return '<FieldType %r>' % self.name