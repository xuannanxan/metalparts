'''
@Description: 
@Version: 1.0
@Autor: Allen
@Date: 2019-11-13 17:29:28
@LastEditors: Allen
@LastEditTime: 2019-11-25 10:56:33
'''

__author__ = 'Allen xu'
from  app.models import db,BaseModel


# 角色
class Role(BaseModel):
    __tablename__ = "role"
    name = db.Column(db.String(100), unique=True,nullable=False)
    auths = db.Column(db.String(512))
  

    def __repr__(self):
        return '<Role %r>' % self.name

# 权限
class Auth(BaseModel):
    __tablename__ = "auth"
    name = db.Column(db.String(100),nullable=False)
    url = db.Column(db.String(255))
    menu_id = db.Column(db.Integer)  # 所属菜单

    def __repr__(self):
        return '<Auth %r>' % self.name