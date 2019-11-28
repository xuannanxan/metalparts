#!/usr/bin/env python
# coding=utf-8
'''
@Description: 
@Author: Xuannan
@Date: 2019-11-28 15:12:17
@LastEditTime: 2019-11-28 17:25:16
@LastEditors: Xuannan
'''
import json,pymysql
from secret import secret
secret = secret()

db = pymysql.Connect(host=secret.get('host'),port=secret.get('port'),user=secret.get('user'),password=secret.get('password'),db=secret.get('db'),charset='utf8')
def load_data():
    with open('./help/code/data/cities.json','r',encoding='utf-8') as city_json_file:
        city_json_str = city_json_file.read()
        city_json = json.loads(city_json_str)
    return city_json

def insert_cities(city_json):
    cities = city_json.get('returnValue')
    keys = cities.keys()
    cursor = db.cursor()
    for k in keys:
        for city in cities[k]:
            id = city.get('id')
            parentId = city.get('parentId')
            regionName = city.get('regionName')
            cityCode = city.get('cityCode')
            pinYin = city.get('pinYin')
            cursor.execute("insert into city(id,pid,city_name,city_code,short_name) values('%s','%s','%s','%s','%s');"%(id,parentId,regionName,cityCode,pinYin))
    db.commit()
if __name__ == '__main__':
    city_json = load_data()
    insert_cities(city_json)