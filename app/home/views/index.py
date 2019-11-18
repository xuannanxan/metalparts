# -*- coding: utf-8 -*- 
# Created by xuannan on 2019-01-01.
#从当前模块__init__导入蓝图对象
from flask import render_template,g,request,session
from app.expand.utils import object_to_dict,Pagination
from app.models import Crud,Product,Category,Template,Ad,Article,TagRelation
from . import home,seoData,cache,getWebTemplate,getCategory,getTemplates,getTag,getQrcode,CLICKS_COUNT


@home.route("/", methods=['GET'])
@home.route("/<int:nav_id>", methods=['GET'])
@home.route("/<int:nav_id>/<int:cate_id>", methods=['GET'])
@home.route("/<int:nav_id>/<int:cate_id>/<int:content_id>", methods=['GET'])
#@cache.memoize(60)
def index(nav_id=None,cate_id=None,content_id=None):
    # 页码
    url = request.url
    rule = str(request.path)
    page,artpage,seo_data,templates, category_data,all_templates= 1,1,{},[],getCategory(),getTemplates()
    nav_data,cate_data,content_data = {'id':nav_id},{'id':cate_id},{'id':content_id}
    if request.args.get('page'):
        page = int(request.args.get('page'))
    if nav_id:
        nav_data = [v for v in category_data if v.id == nav_id][0]
        seo_data = seoData(nav_data.keywords,nav_data.info,nav_data.name) 
        templates_data = [v for v in all_templates if v.nav_id==nav_id]
    else:
        templates_data = [v for v in all_templates if v.nav_id==0]
    if cate_id:
        cate_data = [v for v in category_data if v.id == cate_id][0]
        seo_data = seoData(cate_data.keywords,cate_data.info,cate_data.name) 
    if content_id:
        # 详情页
        tableName = getTableName(int(cate_data.type))
        relation_cate,relation_data = {},[]   
        if tableName:
            content_data = getSubData(tableName,content_id)
            #点击量
            click = 0
            #如果有缓存的点击量，更新点击量
            if rule in CLICKS_COUNT:
                click = int(content_data.click) + int(CLICKS_COUNT[rule])
                # 如果记录了缓存的更新，就把数据重置
                CLICKS_COUNT[rule] = 0
            else:
                click = int(content_data.click)+1
            Crud.auto_select('UPDATE {} SET click = {} WHERE id = {} '.format(tableName,click,content_id))
            if not content_data.id:
                return render_template('admin/404.html')
            seo_data = seoData(content_data.keywords,content_data.description,content_data.title) 
            if content_data.relation_id:
                relation_cate = [v for v in category_data if v.id == content_data.relation_id][0]
            # 当前产品tag对应的产品
            str_tag_content=''
            if content_data.tags:
                tag_content = Crud.search_data(TagRelation,TagRelation.tag_id.in_((content_data.tags).split(',')),'tag_id')
                #关联数据查询语句
                if tag_content:
                    str_tag_content = 'OR {0}.id in ({1})' .format(tableName,','.join([str(x) for x in [v.relation_id for v in tag_content if v.tag_type==cate_data.type]]))
            relation_data = selectSubData(tableName,'{tableName}.relation_id={0} {1} AND {tableName}.id<>{2}'.format(noneToZero(content_data.relation_id),str_tag_content,content_data.id,tableName=tableName),1,8)
            temp_data = {
                "temp": {"template":getContentTemplate(int(cate_data.type))},
                "data": {
                    "cate_data":cate_data,
                    "content_data":content_data,
                    "tags":getTag(),
                    "relation_cate":relation_cate,
                    "relation_data":relation_data
                }
            }
            templates.append(temp_data)
    else:
        for v in templates_data:
            temp_data,data = {},{}
            '''
            temp_data{
                temp:模板设置内容
                data：{当前栏目数据
                    sub_category：子栏目数据 
                    sub_data：子栏目数据 
                    tag:所有标签数据
                }
            }

            '''
            temp_data['temp'] = object_to_dict(v)
            sub_category,cates = [],[]
            for val in category_data:   
                if v.data_id :
                    if val.id == v.data_id:
                        # 如果分配了数据当前栏目的数据就是分配的栏目
                        data = object_to_dict(val)
                    if v.relation:
                        # 如果是关联数据，直接取当前栏目的子栏目
                        if val.pid == nav_id:
                            sub_category.append(val)
                    else:
                        # 当前栏目的子栏目
                        if val.pid == v.data_id:
                            sub_category.append(val)
            data['sub_category'] = sub_category
            #如果是栏目数据
            if v.data_type == 1: 
                if cate_id:
                    # url传了分类id
                    cates.append(cate_id)
                    cates = cates+[cate.id for cate in category_data if cate.pid == cate_id]
                else:
                    # URL没有传分类id，读取设置的数据
                    cates.append(v.data_id)
                    cates = cates+[cate.id for cate in sub_category]        
                tableName = getTableName(int(data['type']))
                # 如果是关联查询，就是通过   relation_id 进行搜索 
                if v.relation:
                    selectColumn = 'relation_id'
                # 如果不是关联查询，就是通过   category_id 进行搜索 
                else:
                    selectColumn = 'category_id'
                str_cats = ','.join([str(x) for x in cates])
                data['sub_data'] = selectSubData(tableName,"%s.%s in (%s)"%(tableName,selectColumn,str_cats),page,v.data_num)
            elif v.data_type == 2:
                data['sub_data'] = Crud.search_data(Ad,Ad.space_id == v.data_id,Ad.sort.desc(),v.data_num)
            data['tags'] = getTag()
            temp_data['data'] = data
            # 全部页面数据压入数组
            templates.append(temp_data)
    param = {
        'nav_data':nav_data,
        'cate_data':cate_data,
        'content_data':content_data
    }
    return render_template("home/%s/home.html"%getWebTemplate(),
        seo_data = seo_data,
        templates = templates,
        param = param
    )



def selectSubData(tableName,query,page,num):
    '''
    多个信息筛选
    tableName:表名
    query:查询语句，表名全部略为P
    page:页面
    num:页面数量
    '''
    sql='''
        SELECT SQL_CALC_FOUND_ROWS {tableName}.*,GROUP_CONCAT(tag_relation.tag_id SEPARATOR ',') as tags,category.pid as cate_pid
        FROM {tableName} 
            left join tag_relation on {tableName}.id = tag_relation.relation_id
            left join category on category.id = {tableName}.category_id
        WHERE {0} AND {tableName}.is_del = 0
        GROUP BY {tableName}.id
        ORDER BY {tableName}.sort DESC
        LIMIT {1},{2};
        '''.format(query,(page-1)*num,num,tableName=tableName)
    sql_data = Crud.auto_select(sql)
    count_num = Crud.auto_select("SELECT FOUND_ROWS() as countnum")
    count = int((count_num.first()).countnum)
    if sql_data:
        return Pagination(page,num,count,sql_data.fetchall())
    return False


def getSubData(tableName,id):
    '''
    单个信息查询
    tableName:表名
    id:查询的id
    '''
    sql='''
        SELECT SQL_CALC_FOUND_ROWS p.*,GROUP_CONCAT(r.tag_id SEPARATOR ',') as tags
        FROM %s as p
            left join tag_relation as r on p.id = r.relation_id
        WHERE p.id = %i;
        '''%(tableName,int(id))
    sql_data = Crud.auto_select(sql)
    if sql_data:
        return sql_data.first()
    return False


def getTableName(type):
    # 如果是产品
    if type == 1:
        return 'product'
    # 如果是文章
    elif type == 2:
        return 'article'
    else:
        return False


def getContentTemplate(type):
    # 如果是产品
    if type == 1:
        return 'product_page'
    # 如果是文章
    elif type == 2:
        return 'article_page'
    else:
        return False

def noneToZero(data):
    '''
    如果data==None,retun 0
    '''
    if data:
        return data
    else:
        return 0


