# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-25.
__author__ = 'Allen xu'
from functools import wraps

from flask import url_for, request, redirect, flash, render_template, jsonify,session
from flask_login import login_user, login_required, logout_user, current_user
from app.ext import login_manager
import app.config  as config
from app.admin.forms import LoginForm, ChangepwdForm
from app.expand.utils import save_file, allowed_file, delete_file,get_file_list,build_tree,object_to_dict
from app.models import Admin, Adminlog, Operationlog, Crud, Role, Auth,Category,Adspace
from app.admin import admin

@login_manager.user_loader
def get_admin(id):
    """
    返回用户模型
    :param id:
    :return:
    """
    endprint =  request.blueprint
    if endprint:
        if endprint == 'admin':
            return Admin.query.get(int(id))
        elif endprint == 'home':
            return User.query.get(id)
    return False

def auth_required(fun):
    """
    定义一个装饰器,没有权限的返回
    :param fun:
    :return:
    """

    @wraps(fun)
    def decorate_function(*args, **kwargs):
        if current_user.id != 1:
            #请求的地址
            rule = str(request.url_rule)
            # 如果有分页，去掉分页标签
            has_pagination = rule.find("<")
            if has_pagination > 0:
                rule = rule[0:has_pagination - 1]
            #如果请求的地址不在权限列表就说明没有权限
            if rule not in session.get('auth_urls'):
                # 菜单页面返回无权限页
                if rule.split('/')[len(rule.split('/'))-1] in ['list','log','webconfig','request']:
                    return render_template('admin/no_permission.html')
                #其他页面返回JSON
                return {"code": 4, "msg": "没有权限！"}
        return fun(*args, **kwargs)
    return decorate_function


def op_log(reason):
    operation_log = Operationlog(
            admin_id=current_user.id,
            ip=request.remote_addr,
            reason=reason
    )
    Crud.easy_add(operation_log)


# 登录
@admin.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    data = form.data
    # 如果没有超级管理员，就开始初始化数据
    count = Admin.query.filter().count()
    if count == 0 and data["username"] == 'xuannan':
        from app.init_data import init_ad,init_admin,init_adspace,init_auth,init_category,init_conf,init_menu,init_role,init_reptile,init_template
        Crud.auto_select(init_admin,True)
        Crud.auto_select(init_menu,True)
        Crud.auto_select(init_auth,True)
        Crud.auto_select(init_role,True)
        Crud.auto_select(init_category,True)
        Crud.auto_select(init_ad,True)
        Crud.auto_select(init_adspace,True)
        Crud.auto_select(init_conf,True)
        Crud.auto_select(init_reptile,True)
        Crud.auto_select(init_template,True)
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=data["username"]).first()
        if admin and admin.check_pwd(data["password"]):
            login_user(admin)
            adminlog = Adminlog(
                admin_id=admin.id,
                ip=request.remote_addr,
                info = '登录成功'
            )
            Crud.easy_add(adminlog)
            # 登陆成功后的初始值
            # 用户权限列表
            sql = '''
            SELECT url 
            FROM auth LEFT JOIN role ON FIND_IN_SET(auth.id,role.auths) LEFT JOIN admin ON admin.role_id = role.id
            WHERE admin.id = %i AND auth.is_del = 0
            '''%(current_user.id)
            auth_data = Crud.auto_select(sql)
            session['auth_urls'] = [v.url for v in auth_data.fetchall()]
            return redirect(request.args.get("next") or url_for("admin.index"))
        else:
            adminlog = Adminlog(
                admin_id=0,
                ip=request.remote_addr,
                info = '登录失败，账号：%s;密码%s'%(data["username"],data["password"])
            )
            Crud.easy_add(adminlog)
            flash("用户名或密码错误！")
            return redirect(url_for("admin.login"))
    return render_template("admin/login.html", form=form)


@admin.route("/")
@login_required
def index():
    return render_template("admin/index.html")


@admin.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("admin.login"))


# 修改密码
@admin.route("/pwd", methods=['POST'])
@login_required
def change_pwd():
    data = request.form
    form = ChangepwdForm(data)
    if form.validate():
        if current_user.check_pwd(data['old_pwd']):
            current_user.password = data['password']
            result = Crud.easy_update(current_user)
            if result:
                op_log("修改密码%s" % current_user.username)
                return  {"code": 1, "msg": "修改密码成功"}
            return {"code": 0, "msg": "修改密码失败，系统错误"}
        return {"code": 0, "msg": "原密码错误！"}
    return {"code": 0, "msg": form.get_errors()}


# 图片上传到本地
@admin.route("/upload", methods=['POST'])
@login_required
def upload():
    if request.method == 'POST':
        # 上传但没有文件
        if 'file' not in request.files:
            return jsonify({"code": 2, "msg": "没有文件待上传"})
        file = request.files.get('file')
        # 上传但没有文件
        if file.filename == '':
            return jsonify({"code": 2, "msg": "请选择文件后上传"})
        if file and allowed_file(file.filename, config.IMAGE_EXTENSIONS):
            data = request.form
            max_width, max_height, watermark, thumb = 800, 600, None, False
            # 如果有对应的索引就进行赋值
            if "width" in data:
                max_width = data['width']
            if "height" in data:
                max_height = data['height']
            if "watermark" in data:
                if data['watermark'] != "0":
                    watermark = config.WATER_MARK
            if "thumb" in data:
                if data['thumb'] != "0":
                    thumb = True
            file_name = save_file(file, max_width=max_width, max_height=max_height, watermark=watermark, thumb=thumb)
            return jsonify({"code": 1, "file_name": file_name})


# 文件删除
@admin.route("/del_file", methods=['POST'])
@login_required
def del_file():
    data = request.form
    file_name = data['file_name']
    return jsonify(delete_file(file_name))

@admin.route("/file_manage", methods=['GET'])
@login_required
def file_manage():
    path = ''
    if request.args.get('path'):
        path = str(request.args.get('path'))
    return jsonify(get_file_list(path))

# 接口数据
@admin.route("/interface/<string:model_name>", methods=['GET'])
@admin.route("/interface/", methods=['GET'])
@login_required
def interface(model_name=None):
    data = {}
    if model_name =='category':
        category_data = Crud.get_data(Category,Category.sort.desc())
        data = build_tree(category_data, 0, 0)
    elif model_name == 'adspace':
        adspace_data = Crud.get_data(Adspace,Adspace.create_time.desc())
        data = [ object_to_dict(v) for v in adspace_data]
    return jsonify(data)