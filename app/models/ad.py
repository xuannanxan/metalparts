# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-26.
__author__ = 'Allen xu'
from  app.models import db,BaseModel

# 广告
class Ad(BaseModel):
    __tablename__ = "ad"
    title = db.Column(db.String(100),nullable=False)
    info = db.Column(db.Text)
    url = db.Column(db.String(255))
    img = db.Column(db.String(255))
    sort = db.Column(db.Integer, default=0)  # 排序
    space_id = db.Column(db.Integer)  # 关联广告位

    def __repr__(self):
        return '<Ad %r>' % self.title


# 广告位
class AdSpace(BaseModel):
    __tablename__ = "ad_space"
    name = db.Column(db.String(100),nullable=False)
    sort = db.Column(db.Integer, default=0)  # 排序

    def __repr__(self):
        return '<AdSpace %r>' % self.name