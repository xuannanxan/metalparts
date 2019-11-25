#!/usr/bin/env python
# coding=utf-8
'''
@Description: 
@Author: Xuannan
@Date: 2019-11-25 09:57:46
@LastEditTime: 2019-11-25 13:11:30
@LastEditors: Xuannan
'''

import json
from collections import defaultdict

def object_to_dict(obj):
    """
    对象转字典
    :param model:
    :return:
    """
    data = obj.__dict__
    if "_sa_instance_state" in data:
        del data["_sa_instance_state"]
    if "password" in data:
        del data["password"]
    if "_password" in data:
        del data["_password"]
    return data

def object_to_json(obj):
    data = object_to_dict(obj)
    data = json.dumps(data, default=str, ensure_ascii=False)
    data = json.loads(data)
    return data

def error_to_string(err):
    """
    错误列表转字符串
    :param err:
    :return:
    """
    errors = ''
    for v in err:
        for m in v:
            errors += m
        errors += '\n'
    return errors


def rows_by_date(data,name):
    '''
    按字段对数据进行分类
    '''
    rows_date = defaultdict(list)
    for row in data:
        rows_date[row[name]].append(row)    
    return rows_date

