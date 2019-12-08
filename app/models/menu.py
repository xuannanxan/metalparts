# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-26.
__author__ = 'Allen xu'
from  app.models import db

# 菜单
class Menu(BaseModel):
    __tablename__ = "menu"
    name = db.Column(db.String(100),nullable=False)
    icon = db.Column(db.String(100))
    url = db.Column(db.String(255))
    pid = db.Column(db.Integer)  # 上级菜单
    sort = db.Column(db.Integer, default=0)  # 排序

    def __repr__(self):
        return '<Menu %r>' % self.name