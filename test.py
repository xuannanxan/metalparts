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
    filelist('D:/python/metalparts/app/utils/captcha')

