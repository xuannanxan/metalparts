#!/usr/bin/env python
# coding=utf-8
'''
@Description: 
@Author: Xuannan
@Date: 2019-11-21 10:12:25
@LastEditTime: 2019-11-25 15:34:33
@LastEditors: Xuannan
'''
# -*- coding: utf-8 -*-
# Created by xuannan on 2019-01-01.
import os
from flask_script import Manager
from flask_migrate import MigrateCommand
from app import create_app

env = os.environ.get('FLASK_ENV','dev')
# 生成app
app = create_app(env)
manager = Manager(app=app)
manager.add_command('db',MigrateCommand)
'''
数据迁移
    初始化    
    python manager.py db init  仅第一次使用
    迁移      
    python manager.py db migrate
    更新      
    python manager.py db upgrade
启动服务
    python manager.py runserver
接口文档
    http://localhost:5000/apidocs/
'''
if __name__ == '__main__':
    manager.run()
