#!/usr/bin/env python
# coding=utf-8
'''
@Description: 
@Author: Xuannan
@Date: 2019-11-26 09:05:27
@LastEditTime: 2019-11-28 16:19:35
@LastEditors: Xuannan
'''
import os
from time import time



# 装饰器

def runtime(fun):
    
    def wrapper1(*args,**kwargs):
        begintime = time()
        result = fun(*args,**kwargs)
        endtime = time()
        print(endtime-begintime)
        return result
    return wrapper1

@runtime
def filelist(dir):
    for filename in os.listdir(dir):
        print(filename)

if __name__ == '__main__':
    filelist('./')

