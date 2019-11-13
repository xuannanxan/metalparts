# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-26.
__author__ = 'Allen xu'
from flask import  request,jsonify,render_template
from flask_login import login_required

from app.admin.forms import ConfForm
from app.admin.views.base import op_log,auth_required
from app.expand.utils import object_to_dict
from app.models import Conf,Crud
from .. import admin


# 添加配置项
@admin.route("/conf/add", methods=["POST"])
@login_required
@auth_required
def conf_add():
    data = request.form
    form = ConfForm(data)
    if form.validate():
        result = Crud.add(Conf,data,"ename")
        if result:
            op_log("添加配置项-%s" % data["ename"])
            return {"code":1, "msg": '添加成功'}
        return {"code":0, "msg": '添加失败，系统错误或调用名已存在'}
    return {"code": 0, "msg": form.get_errors()}



# 配置项列表
@admin.route("/conf/list/<int:page>", methods=['GET'])
@admin.route("/conf/list", methods=['GET'])
@login_required
@auth_required
def conf_list(page=None):
    page_data = Crud.get_data_paginate(Conf, Conf.sort.desc(), page, 10)
    return render_template("admin/conf/conf_list.html", page_data=page_data)


# 修改配置项
@admin.route("/conf/edit", methods=['GET', 'PUT'])
@login_required
@auth_required
def conf_edit():
    if request.method == 'GET':
        getdata = request.args
        data = Crud.get_data_by_id(Conf, getdata['id'])
        conf_data = object_to_dict(data)
        return jsonify({"code": 1, "data":conf_data})
    elif request.method == "PUT":
        data = request.form
        form = ConfForm(data)
        if form.validate():
            result = Crud.update(Conf,data,"ename")
            if result:
                op_log("修改配置项#%s" %  data["id"])
                return {"code":1, "msg": '修改成功'}
            return {"code":0, "msg": '修改失败，系统错误或调用名已存在'}
        return {"code": 0, "msg": form.get_errors()}


# 删除配置项
@admin.route("/conf/del", methods=['DELETE'])
@login_required
@auth_required
def conf_del():
    deldata = request.form
    data = Conf.query.filter_by(id=deldata['id']).first_or_404()
    result = Crud.delete(data)
    if result:
        op_log("删除配置项-%s" % data.name)
        return {"code":1, "msg": '删除成功'}
    return {"code":0, "msg": '删除失败，系统错误'}


# 配置项
@admin.route("/conf/webconfig", methods=['GET','POST'])
@login_required
@auth_required
def webconfig():
    data = Crud.get_data(Conf, Conf.sort.desc())
    if request.method == 'GET':
        return render_template("admin/conf/webconfig.html")
    elif request.method == 'POST':
        form_data = request.form
        for v in data:
            v.default_value = form_data[v.ename]
        result = Crud.easy_update(data)
        if result:
            op_log("修改配置")
            return {"code":1, "msg": '保存成功'}
        return {"code":0, "msg": '保存失败，系统错误'}
