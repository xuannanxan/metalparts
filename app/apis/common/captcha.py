#!/usr/bin/env python
# coding=utf-8
'''
@Description: 
@Author: Xuannan
@Date: 2019-11-26 09:05:26
@LastEditTime: 2019-11-26 17:29:52
@LastEditors: Xuannan
'''
from flask_restful import Resource
from app.utils.captcha import Captcha

class CaptchaResource(Resource):
    def get(self):
        text, image = Captcha()
        print(text,image)
        return image