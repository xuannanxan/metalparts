#!/usr/bin/env python
# coding=utf-8
'''
@Description: 
@Author: Xuannan
@Date: 2019-11-21 10:12:25
@LastEditTime: 2019-11-28 14:59:38
@LastEditors: Xuannan
'''
import os
from flask_script import Manager
from flask_migrate import MigrateCommand
from app import create_app

env = os.environ.get('FLASK_ENV','dev')
# 生成app
app = create_app(env)
manager = Manager(app=app)
manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manager.run()
