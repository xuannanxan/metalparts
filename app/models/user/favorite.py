# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-08-24.
__author__ = 'Allen xu'
from  app.models import db, BaseModel
# 收藏
class Favorite(BaseModel):
    __tablename__ = "favorite"
    favorite_type = db.Column(db.SmallInteger)  # 留言类型，1为产品咨询，2为文章互动,''为其他
    relation_id = db.Column(db.Integer)  # 关联id
    uid = db.Column(db.String(255))  # 收藏用户

    def __repr__(self):
        return '<Favorite %r>' % self.id