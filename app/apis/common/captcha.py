#!/usr/bin/env python
# coding=utf-8
'''
@Description: 
@Author: Xuannan
@Date: 2019-11-26 09:05:26
@LastEditTime: 2019-11-26 22:26:20
@LastEditors: Xuannan
'''
from flask_restful import Resource
from app.utils.captcha import Captcha
from flask import make_response

class CaptchaResource(Resource):
    def get(self):
        text, image_data = Captcha.gene_graph_captcha()
        print(text,image_data)
        return image_data