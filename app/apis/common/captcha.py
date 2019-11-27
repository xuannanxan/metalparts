#!/usr/bin/env python
# coding=utf-8
'''
@Description: 
@Author: Xuannan
@Date: 2019-11-26 09:05:26
@LastEditTime: 2019-11-27 22:14:27
@LastEditors: Xuannan
'''
from flask_restful import Resource,reqparse,abort
from app.utils.captcha import Captcha
from flask import make_response,current_app
from app.ext import cache
from app.apis.api_constant import *

parse = reqparse.RequestParser()
parse.add_argument('image_code',type=str,required=True,help='请传入image_code')
class CaptchaResource(Resource):
    def get(self):
        """
        file: yml/captcha.yml
        """
        args = parse.parse_args()
        image_code = args.get('image_code')
        text, image_data = Captcha.gene_graph_captcha()
        try:
            cache.set('image_code_%s'%image_code,text,timeout= 3*60)
            data = {
                    'status':RET.OK,
                    'data':image_data
                }
            return data
        except Exception as e:
            current_app.logger.error(e)
            abort(RET.BadRequest,msg='获取验证码失败')
        