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
'''
if __name__ == '__main__':
    manager.run()
