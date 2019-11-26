#!/usr/bin/env python
# coding=utf-8
'''
@Description: 
@Author: Xuannan
@Date: 2019-11-25 10:40:04
@LastEditTime: 2019-11-26 22:25:08
@LastEditors: Xuannan
'''


import qrcode,base64
from io import BytesIO

def set_qrcode(url):
    """
    根据传入的url 生成 二维码对象
    :param url:
    :return:
    """
    qr = qrcode.QRCode(version=1,  # 二维码大小 1～40
                       error_correction=qrcode.constants.ERROR_CORRECT_L,  # 二维码错误纠正功能
                       box_size=10,  # 二维码 每个格子的像素数
                       border=2)     # 二维码与图片边界的距离

    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image()
    byte_io = BytesIO()
    img.save(byte_io, 'PNG')
    res = byte_io.getvalue()
    byte_io.close()
    return (base64.b64encode(res)).decode()