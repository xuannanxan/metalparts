#!/usr/bin/env python
# coding=utf-8
'''
@Description: 
@Author: Xuannan
@Date: 2019-11-26 09:05:26
@LastEditTime: 2019-11-26 17:34:21
@LastEditors: Xuannan
'''
from flask_restful import Api
from app.apis import api_blueprint
from app.apis.common.captcha import CaptchaResource

common_api = Api(api_blueprint)
common_api.add_resource(CaptchaResource,'/captcha/')
