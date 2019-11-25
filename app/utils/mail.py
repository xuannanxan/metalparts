#!/usr/bin/env python
# coding=utf-8
'''
@Description: 
@Author: Xuannan
@Date: 2019-11-21 10:12:25
@LastEditTime: 2019-11-25 13:11:19
@LastEditors: Xuannan
'''


from flask_mail import Message
from app.ext import mail
import app.secret as secret
from threading import Thread
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(2)

class MailObj():
        def __init__(self):
            self.subject = 'Thank you mail to us'
            self.sender = secure.MAIL_DEFAULT_SENDER
            self.recipients = [secure.MAIL_ASYNC_RECIPIENTS]
            self.text_body = 'We have received your mail, and we will contact you as soon as possible. '
            self.html_body = ''
# 异步发送邮件
def send_email(mailObj):
    from manage import app
    thr = Thread(target=send_async_email,args=[app,mailObj])
    #使用多线程，在实际开发中，若是不使用异步、多线程等方式，网页会卡住
    thr.start()
    return thr
def send_async_email(app,mailObj):
    #异步发送将开启一个新的线程,执行上下文已经不在app内,必须with语句进入app上下文才可以执行mail对象
    with app.app_context():
        #主要是Message卡，在线程中初始化
        msg = Message(mailObj.subject, sender=mailObj.sender, recipients=mailObj.recipients)
        msg.body = mailObj.text_body
        msg.html = mailObj.html_body
        mail.send(msg)
