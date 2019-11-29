#!/usr/bin/env python
# coding=utf-8
'''
@Description: 
@Author: Xuannan
@Date: 2019-11-13 17:29:28
@LastEditTime: 2019-11-29 11:58:49
@LastEditors: Xuannan
'''


from  app.models import db,BaseModel
# 分类
class Category(BaseModel):
    __tablename__ = "category"
    type_id = db.Column(db.String(32), nullable=False)  # 分类类型
    name = db.Column(db.String(200),nullable=False)
    keywords = db.Column(db.String(255))
    info = db.Column(db.Text)
    icon = db.Column(db.String(100))
    cover = db.Column(db.String(255))
    pid = db.Column(db.Integer, default=0)  # 上级分类,0为最上级
    sort = db.Column(db.Integer, default=0)  # 排序
   

    def __repr__(self):
        return '<Category %r>' % self.name

# 分类的类型
class CategoryType(BaseModel):
    __tablename__ = "category_type"
    name = db.Column(db.String(200),nullable=False)
    sort = db.Column(db.Integer, default=0)  # 排序
   

    def __repr__(self):
        return '<CategoryType %r>' % self.name