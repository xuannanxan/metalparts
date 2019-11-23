# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-02.
import os
from redis import Redis
from app.secret import secret
# 自定义变量
# 文件上传的位置
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static/uploads')
# 水印
WATER_MARK = os.path.join(BASE_DIR, 'static/admin/img/watermark.png')
# 通用配置
class config:
    DEBUG = False
    TESTING = False
    #允许的文件格式
    FILE_EXTENSIONS = set(['txt', 'pdf','rar', 'zip','doc', 'docx','xls', 'xlsx', 'ppt', 'pptx','db','png', 'jpg', 'jpeg', 'gif'])
    IMAGE_EXTENSIONS = set([ 'png', 'jpg', 'jpeg', 'gif'])
    #图片大小
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024

    # 设置redis的ip,port,有效时间
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = "6379"
    REDIS_DB= 0
    REDIS_PASSWORD = ''


    #设置CACHE
    CACHE_TYPE = 'redis'
    CACHE_REDIS_HOST = REDIS_HOST
    CACHE_REDIS_PORT = REDIS_PORT
    CACHE_REDIS_PASSWORD = REDIS_PASSWORD
    CACHE_DEFAULT_TIMEOUT = 300

    # 设置session
    SESSION_TYPE = 'redis'
    SESSION_REDIS=  Redis(host=REDIS_HOST, port=REDIS_PORT, password= REDIS_PASSWORD,db = REDIS_DB)
    SESSION_PERMANENT = True  # 如果设置为True，则关闭浏览器session就失效
    SESSION_USE_SIGNER = True # 是否对发送到浏览器上 session:cookie值进行加密
    # 数据库配置
    # 数据库公用配置
    # 无警告
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 自动提交
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True    

    # 发邮件 配置
    MAIL_USE_SSL = True
    MAIL_SUPPRESS_SEND = False
    MAIL_PORT = 465
    MAIL_USE_TLS = False   
    MAIL_PROT = 465,
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEBUG = False
    

class Dev(config):
    DEBUG = True
    MAIL_DEBUG = True
    # 密码信息
    secret = secret('dev')
    ENGINE = 'mysql'  # 要用的什么数据库
    DRIVER = 'pymysql'  # 连接数据库驱动
    USERNAME = secret.get('DB_USERNAME')  # 用户名
    PASSWORD = secret.get('DB_PASSWORD')   # 密码
    HOST = secret.get('DB_HOST')   # 服务器
    PORT = '3306'  # 端口
    DATABASE = secret.get('DB_DATABASE')  # 数据库名
    SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(ENGINE, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)
    MAIL_SERVER = secret.get('MAIL_SERVER') 
    MAIL_USERNAME = secret.get('MAIL_USERNAME')
    MAIL_DEFAULT_SENDER =secret.get('MAIL_USERNAME')
    MAIL_ASYNC_RECIPIENTS = secret.get('MAIL_ASYNCNAME') 
    MAIL_PASSWORD = secret.get('MAIL_PASSWORD') 
    SECRET_KEY=secret.get('SECRET_KEY') 
    

class Produce(config):
    # 密码信息
    secret = secret('produce')
    ENGINE = 'mysql'  # 要用的什么数据库
    DRIVER = 'pymysql'  # 连接数据库驱动
    USERNAME = secret.get('DB_USERNAME')  # 用户名
    PASSWORD = secret.get('DB_PASSWORD')   # 密码
    HOST = secret.get('DB_HOST')   # 服务器
    PORT = '3306'  # 端口
    DATABASE = secret.get('DB_DATABASE')  # 数据库名
    SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(ENGINE, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)
    MAIL_SERVER = secret.get('MAIL_SERVER') 
    MAIL_USERNAME = secret.get('MAIL_USERNAME')
    MAIL_DEFAULT_SENDER =secret.get('MAIL_USERNAME')
    MAIL_ASYNC_RECIPIENTS = secret.get('MAIL_ASYNCNAME') 
    MAIL_PASSWORD = secret.get('MAIL_PASSWORD') 
    SECRET_KEY=secret.get('SECRET_KEY') 

envs = {
    'dev' :Dev,
    'produce':Produce,
    'default':Dev
}