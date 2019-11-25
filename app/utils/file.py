#!/usr/bin/env python
# coding=utf-8
'''
@Description: 
@Author: Xuannan
@Date: 2019-11-25 10:34:07
@LastEditTime: 2019-11-25 13:11:23
@LastEditors: Xuannan
'''


from PIL import Image
import os, time, random,re,requests
from io import BytesIO
from datetime import datetime
from pathlib import Path
from app.config import UPLOAD_FOLDER

#下载图片并替换HTML中的图片链接
def replaceSrc(content,url):
    etree = html.etree
    selector = etree.HTML(content)
     #将页面上图片的链接加入list
    imgs = selector.xpath("//img/@src")
    for img in imgs:
        src = full_url(url,img)
        new_src = downImage(src)
        content = content.replace(img,new_src)
    return content
#是否为<class 'lxml.etree._Element'>
def isEtreeElement(obj):
    if str(type(obj))=="<class 'lxml.etree._Element'>":
        return True
    else:
        return False
#下载图片
def downImage(src):
    response = requests.get(src)
    im = Image.open(BytesIO(response.content))
    # 文件目录
    path = time.strftime('%Y%m%d')
    d = UPLOAD_FOLDER+'/'+path
    if not os.path.exists(d):
        os.makedirs(d)
    # 文件扩展名
    ext = os.path.splitext(src)[1]
    # 定义文件名，年月日时分秒随机数
    fn = time.strftime('%Y%m%d%H%M%S')
    fn = fn + '_%d' % random.randint(100,999)
    # 重写合成文件名
    im.save(os.path.join(d, fn + ext))
    return '/static/uploads/'+path+'/'+fn + ext

def thumb_image(img, w=128, h=128):
    '''
    缩略图
    '''
    img.thumbnail((w,h))
    return img


def logo_watermark(im, mark_path):
    '''
    添加一个图片水印,原理就是合并图层，用png比较好
    '''
    mark=Image.open(mark_path)
    layer=Image.new('RGBA', im.size, (0,0,0,0))
    w,h = mark.size
    layer.paste(mark, (im.size[0]-w,im.size[1]-h))
    out=Image.composite(layer,im,layer)
    return out



#等比例压缩图片
def resizeImg(img, dst_w=0, dst_h=0):
    '''
    只给了宽或者高，或者两个都给了，然后取比例合适的
    如果图片比给要压缩的尺寸都要小，就不压缩了
    '''
    ori_w, ori_h = img.size
    widthRatio = heightRatio = None
    ratio = 1

    if (ori_w and ori_w > dst_w) or (ori_h and ori_h  > dst_h):
        if dst_w and ori_w > dst_w:
            widthRatio = float(dst_w) / ori_w                                      #正确获取小数的方式
        if dst_h and ori_h > dst_h:
            heightRatio = float(dst_h) / ori_h

        if widthRatio and heightRatio:
            if widthRatio < heightRatio:
                ratio = widthRatio
            else:
                ratio = heightRatio

        if widthRatio and not heightRatio:
            ratio = widthRatio

        if heightRatio and not widthRatio:
            ratio = heightRatio

        newWidth = int(ori_w * ratio)
        newHeight = int(ori_h * ratio)
    else:
        newWidth = ori_w
        newHeight = ori_h
    img = img.resize((newWidth,newHeight),Image.ANTIALIAS)
    return img


#裁剪压缩图片
def clipResizeImg(img, dst_w, dst_h):

    '''
        先按照一个比例对图片剪裁，然后在压缩到指定尺寸
        一个图片 16:5 ，压缩为 2:1 并且宽为200，就要先把图片裁剪成 10:5,然后在等比压缩
    '''
    ori_w,ori_h = img.size

    dst_scale = float(dst_w) / dst_h  #目标高宽比
    ori_scale = float(ori_w) / ori_h #原高宽比

    if ori_scale <= dst_scale:
        #过高
        width = ori_w
        height = int(width/dst_scale)

        x = 0
        y = (ori_h - height) / 2

    else:
        #过宽
        height = ori_h
        width = int(height*dst_scale)

        x = (ori_w - width) / 2
        y = 0

    #裁剪
    box = (x,y,width+x,height+y)
    #这里的参数可以这么认为：从某图的(x,y)坐标开始截，截到(width+x,height+y)坐标
    #所包围的图像，crop方法与php中的imagecopy方法大为不一样
    newIm = img.crop(box)
    img = None

    #压缩
    ratio = float(dst_w) / width
    newWidth = int(width * ratio)
    newHeight = int(height * ratio)
    img = newIm.resize((newWidth,newHeight),Image.ANTIALIAS)
    return img

def allowed_file(filename,extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in extensions

def save_file(file,type = "image",max_width = 800,max_height = 0,watermark = None,thumb = False):
    filename = (file.filename)
    # 打开一个jpg图像文件，注意是当前路径:
    max_width = int(max_width)
    max_height = int(max_height)
    if type == "image":
        im = Image.open(file)
        # 获得图像尺寸:
        w, h = im.size
        # 如果宽度大于最大宽度，就压缩到最大宽度:
        if w > max_width and max_height == 0:
            im = resizeImg(im,max_width)
            # 如果设定了高度，说明要进行裁剪:
        if max_height > 0 and w > max_width and h > max_height:
            im = clipResizeImg(im,max_width,max_height)
        if watermark:
            im = logo_watermark(im,watermark)
        if thumb:
            im = thumb_image(im,max_width,max_height)
    else:
        im = file
    # 文件目录
    path = time.strftime('%Y%m%d')
    d = UPLOAD_FOLDER+'/'+path
    if not os.path.exists(d):
        os.makedirs(d)
    # 文件扩展名
    ext = os.path.splitext(filename)[1]
    # 定义文件名，年月日时分秒随机数
    fn = time.strftime('%Y%m%d%H%M%S')
    fn = fn + '_%d' % random.randint(100,999)
    # 重写合成文件名
    im.save(os.path.join(d, fn + ext))
    return '/static/uploads/'+path+'/'+fn + ext


def delete_file(filename):
    path = UPLOAD_FOLDER+'/'+filename[:8]+'/'+filename
    if os.path.exists(path): # 如果文件存在
    #删除文件，可使用以下两种方法。
        os.remove(path) # 则删除
        return {"code":1,'msg':"删除成功！"}
    #os.unlink(my_file)
    else:
        return {"code":2,'msg':"文件不存在！"}

def get_FileSize(filePath):
    '''获取文件的大小,结果保留两位小数，单位为MB'''
    fsize = os.path.getsize(filePath)
    fsize = fsize / float(1024 * 1024)
    return round(fsize, 2)


def checkMobile(userAgent):
    _long_matches = r'googlebot-mobile|android|avantgo|blackberry|blazer|elaine|hiptop|ip(hone|od)|kindle|midp|mmp|mobile|o2|opera mini|palm( os)?|pda|plucker|pocket|psp|smartphone|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce; (iemobile|ppc)|xiino|maemo|fennec'
    _long_matches = re.compile(_long_matches, re.IGNORECASE)
    _short_matches = r'1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|e\-|e\/|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(di|rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|xda(\-|2|g)|yas\-|your|zeto|zte\-'
    _short_matches = re.compile(_short_matches, re.IGNORECASE)

    if _long_matches.search(userAgent) != None:
        return True
    user_agent = userAgent[0:4]
    if _short_matches.search(user_agent) != None:
        return True
    return False

def get_file_list(path=''):
    file_list = []
    if(path):
        p = Path(path)
    else:
        p = Path(UPLOAD_FOLDER)
        path=UPLOAD_FOLDER
    for cp in os.listdir(p):
        if os.path.isdir(os.path.join(p,cp)):
            file_list.append({
                'path':path+'/'+cp,
                'name':cp,
                'type':'dir',
            })
        else:
            file_list.append({
                'name':cp,
                'path':'/static/uploads/'+cp[:8]+'/'+cp,
                'type':'file'
            })
    return file_list


def make_dir(make_dir_path):
    path = make_dir_path.strip()
    if not os.path.exists(path):
        os.makedirs(path)
    return path


