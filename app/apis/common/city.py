#!/usr/bin/env python
# coding=utf-8
'''
@Description: 
@Author: Xuannan
@Date: 2019-11-28 14:14:13
@LastEditTime: 2019-11-28 17:46:17
@LastEditors: Xuannan
'''
from flask_restful import Resource,reqparse,abort
from app.models.common import City

class CitiesResource(Resource):
    def get(self):
        data = City.query.all()
        print(data)
        return {'msg':'111'}