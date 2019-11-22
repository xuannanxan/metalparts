# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-16.
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_mail import Mail
from flask_cache import Cache
from app.apis import api_blueprint


# 创建对象
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()
csrf = CSRFProtect()
#缓存
cache = Cache(with_jinja2_ext=False)
csrf.exempt(api_blueprint)


# 初始化拓展包
def init_ext(app):
    db.init_app(app)
    migrate.init_app(app,db)
    login_manager.init_app(app)
    login_manager.login_view = 'admin.login'
    login_manager.login_message = '请先登录！！！'
    cache.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)

