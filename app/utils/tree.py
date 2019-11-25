#!/usr/bin/env python
# coding=utf-8
'''
@Description: 
@Author: Xuannan
@Date: 2019-11-25 10:30:34
@LastEditTime: 2019-11-25 13:09:56
@LastEditors: Xuannan
'''

from app.utils import object_to_dict

def build_tree(data, pid, level=0):
    """
    生成树
    :param data:    数据
    :param p_id:    上级分类
    :param level:   当前级别
    :return:
    """
    tree = []
    for v in data:
        row = object_to_dict(v)
        if row:
            if row['pid'] == pid:
                row['level'] = level
                child = build_tree(data, row['id'], level+1)
                row['children'] = []
                if child:
                    row['children'] += child
                tree.append(row)
    return tree