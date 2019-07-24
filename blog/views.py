from django.shortcuts import render, HttpResponse, redirect
from blog import models
from django.core import serializers
import os, shutil, json, time
from PersonalBlog import settings

# 引入随机函数模块
import os
import random
from io import BytesIO
import base64
# 引入绘图模块
from PIL import Image, ImageDraw, ImageFont
# Create your views here.


def verifycode(request):
    """
    function:较复杂的生成验证码，返回给前端， PS:识别难度较大
    :param request: 前端发来的请求
    :return: 验证码为内容的HttpResponse
    """

    # 定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), 255)
    width = 100
    # height = 25
    height = 30
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    str1 = 'ABCD123EFGHJK456LMNPQRS789TUVWXYZ'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 构造字体对象
    font_path = os.path.join(settings.BASE_DIR, "common", "Roboto-Bold-webfont.woff")
    font = ImageFont.truetype(font_path, 25)

    # 构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, 0), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 0), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 0), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 0), rand_str[3], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    # 存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    # 内存文件操作
    buf = BytesIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    #print(buf.getvalue())

    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')

def login(request):
    return render(request, 'login.html')

def startLogin(request):
    ret = {"status":None, "message":None, "user":None}
    uname = request.POST.get("uname", None)
    upwd = request.POST.get("upwd", None)
    verificationcode = request.POST.get("verificationcode", None)

    verifycode = request.session['verifycode']
    verifycode = str(verifycode).lower()
    if verifycode != str(verificationcode).lower():
        ret["status"] = 0;
        ret["message"] = "验证码输入错误"
    else:
        try:
            user = models.UserInfo.objects.get(uname=uname)
            if user.uname != uname:
                ret["status"] = 0;
                ret["message"] = "用户名错误"
            if user.upwd != upwd:
                ret["status"] = 0;
                ret["message"] = "密码错误"
            else:
                ret["status"] = 1;
                ret["message"] = "登录成功"
                ret["user"] = get_user_info_data(user)

                request.session.set_expiry(0)
                request.session['uname'] = user.uname
        except Exception as e:
            ret["status"] = 0;
            ret["message"] = "用户不存在"

    return HttpResponse(json.dumps(ret, ensure_ascii=False))

def registUser(request):
    ret = {"status":None, "message":None}
    try:
        uname = request.POST.get("uname", None);
        users = models.UserInfo.objects.filter(uname=uname)
        if users:
            ret["status"] = 0
            ret["message"] = "用户名已存在"
        else:
            upwd = request.POST.get("upwd", None);
            uemail = request.POST.get("uemail", None);
            uhead_100x100 = request.POST.get("uhead_100x100",
                                             "/static/images/defaultUserHead/default_userheag_img_100x100.png");
            uhead_48x48 = request.POST.get("uhead_48x48",
                                           "/static/images/defaultUserHead/default_userheag_img_48x48.png");
            uhead_35x35 = request.POST.get("uhead_35x35",
                                           "/static/images/defaultUserHead/default_userheag_img_35x35.png");
            chickenSoup = "只要思想不滑坡，办法总比困难多"

            ret_u = models.UserInfo.objects.create(uname=uname, upwd=upwd, email=uemail,
                                                   headImg_100x100=uhead_100x100,
                                                   headImg_48x48=uhead_48x48, headImg_35x35=uhead_35x35,
                                                   chickenSoup=chickenSoup)
            ret["status"] = 1
            ret["message"] = "注册成功"
    except Exception as e:
        ret["status"] = 0
        ret["message"] = "注册失败"


    return HttpResponse(json.dumps(ret, ensure_ascii=False))

def index(request):
    if 'uname' in request.session:
        uid = request.GET.get("uid", None)
        user = models.UserInfo.objects.filter(pk=uid)[0]
        ret_user = get_user_info_data(user)

        return render(request, 'index.html',{'userinfo':ret_user, 'classify':getClassify(uid), 'tag':getTag(uid)})
    else:
        return redirect('../')

def article(request, uid, articleid):
    if 'uname' in request.session:
        user = models.UserInfo.objects.filter(pk=uid)[0]
        return render(request, 'article.html', {'userinfo': get_user_info_data(user), 'classify': getClassify(uid), 'tag': getTag(uid)})
    else:
        return redirect('../')

def postedit(request):
    ret = {'status': None, 'article': None, 'classify': None, 'tag': None}
    pk = request.POST.get('pk', None)
    uid = request.POST.get('uid', None)

    ret_classify = getClassify(uid)
    ret_tag = getTag(uid)

    ret['classify'] = serializers.serialize('json', ret_classify)
    ret['tag'] = serializers.serialize('json', ret_tag)
    ret['status'] = 1

    if pk:
        ret_article = models.Article.objects.filter(pk=int(pk))
        ret['article'] = serializers.serialize('json', ret_article, use_natural_foreign_keys=True)
        return HttpResponse(json.dumps(ret))
    else:
        return HttpResponse(json.dumps(ret));

def getArticles(request, type, pk):
    pgnum = int(request.GET.get('pgnum', 0))
    uid = int(request.GET.get('uid', 0))
    pageSize = 10
    ret = {'pgnum': pgnum+1,'type':type, 'id':pk, 'data':None}
    start_index = pgnum * pageSize
    end_index = pgnum * pageSize + pageSize

    if type == 'all':
        ret_article = models.Article.objects.filter(user_id=uid, deleted=0)[start_index:end_index]
    elif type == 'classify':
        ret_article = models.Article.objects.filter(user_id=uid, deleted=0).filter(classify_id = pk)[start_index:end_index]
    elif type == 'tag':
        ret_article = models.Article.objects.filter(user_id=uid, deleted=0).filter(tag__id=pk)[start_index:end_index]

    json_data = serializers.serialize('json', ret_article, use_natural_foreign_keys=True)
    #print(json_data)
    ret['data'] = json_data
    return HttpResponse(json.dumps(ret))

def articleDetails(request):
    pk = request.GET.get('pk')
    ret = models.Article.objects.all().filter(pk=int(pk))
    return HttpResponse(serializers.serialize('json', ret, use_natural_foreign_keys=True))

def clock(request):
    return render(request, 'clock.html')

def articleEditPage(request):
    if 'uname' in request.session:
        pk = request.GET.get("articleid", None)
        uid = request.GET.get("uid", None)
        user = models.UserInfo.objects.filter(pk=uid)[0]
        return render(request, 'articleEdit.html', {'userinfo': get_user_info_data(user)})
    else:
        return redirect('../')

def delArticle(request, pk):
    ret = {"status":None, "message":None, "article":None}
    try:
        models.Article.objects.filter(pk=pk).update(deleted=1)
        ret["status"] = 1
        ret["message"] = "删除成功"
        ret["article"] = pk
    except Exception as e:
        print(e)
        ret["status"] = 0
        ret["message"] = "删除失败"

    return HttpResponse(json.dumps(ret, ensure_ascii=False))

def getClassify(uid):
    classify_ret = models.Classify.objects.filter(user_id=uid)
    return classify_ret

def getTag(uid):
    tag_ret = models.Tag.objects.filter(user_id=uid)
    return tag_ret

def addArticleClassify(request):
    msg = {'action':'addArticleClassify', 'msg':None, 'status':None}
    classify_name = request.GET.get('value')
    classify_id = request.GET.get('id', None)
    uid = request.GET.get('uid', None)

    if classify_id:
       return updateArticleClassify(classify_id,classify_name )

    try:
        re = models.Classify.objects.create(name=classify_name, user_id=uid)
        print(re)
        msg['status'] = 1
        msg['msg'] = '保存成功'
        msg['id'] = re.id

    except Exception as e:
        msg['status'] = 0
        msg['msg'] = '保存失败'
    return HttpResponse(json.dumps(msg, ensure_ascii=False))

def updateArticleClassify(classify_id, classify_name):
    msg = {'action':'updateArticleClassify', 'msg': None, 'status': None}
    try:
        re = models.Classify.objects.filter(id=classify_id).update(name=classify_name)
        print(re)
        msg['status'] = 1
        msg['msg'] = '修改成功'

    except Exception as e:
        msg['status'] = 0
        msg['msg'] = '修改失败'

    return HttpResponse(json.dumps(msg, ensure_ascii=False))

def addArticleTag(request):
    msg = {'action':'addArticleTag', 'msg': None, 'status': None}
    tag_name = request.GET.get('value')
    tag_id = request.GET.get('id', None)
    uid = request.GET.get('uid', None)

    if (tag_id):
        return updateArticleTag(tag_id, tag_name)
    try:
        re = models.Tag.objects.create(name=tag_name, user_id=uid)
        msg['status'] = 1
        msg['msg'] = '保存成功'
        msg['id'] = re.id
    except Exception as e:
        msg['status'] = 0
        msg['msg'] = '保存失败'
    return HttpResponse(json.dumps(msg, ensure_ascii=False))

def updateArticleTag(tag_id, tag_name):
    msg = {'action':'updateArticleTag', 'msg': None, 'status': None}
    try:
        re = models.Tag.objects.filter(id=tag_id).update(name=tag_name)
        print(re)
        msg['status'] = 1
        msg['msg'] = '修改成功'

    except Exception as e:
        msg['status'] = 0
        msg['msg'] = '修改失败'

    return HttpResponse(json.dumps(msg, ensure_ascii=False))

def delArticleClassify(request):
    msg = {'msg': None, 'status': None}
    id = request.GET.get('id')
    try:
        models.Classify.objects.filter(id=id).delete()
        msg['status'] = 1
        msg['msg'] = '删除成功'
    except Exception as e:
        msg['status'] = 0
        msg['msg'] = '删除失败'
    return HttpResponse(json.dumps(msg, ensure_ascii=False))

def delArticleTag(request):
    msg = {'msg': None, 'status': None}
    id = request.GET.get('id')
    try:
        models.Tag.objects.filter(id=id).delete()
        msg['status'] = 1
        msg['msg'] = '删除成功'
    except Exception as e:
        msg['status'] = 0
        msg['msg'] = '删除失败'
    return HttpResponse(json.dumps(msg, ensure_ascii=False))

def addArticle(request):
    msg = {'status': None}
    try:
        articleTitle = request.GET.get('articleTitle')
        articleContent = request.GET.get('articleContent')
        classifyId = request.GET.get('classifyId')
        tagIds = request.GET.getlist('tagIds')
        pk = request.GET.get('pk')
        uid = request.GET.get('uid')

        if pk:
            article = models.Article.objects.filter(pk=int(pk))
            article.update(title=articleTitle, content=articleContent, classify_id=classifyId)
            article.first().tag.set(list(map(int, tagIds)))
        else:
            article = models.Article.objects.create(title=articleTitle, content=articleContent, classify_id=classifyId, user_id=uid)
            article.tag.add(*list(map(int, tagIds)))  # ['1','2'] 转 [1, 2]
        msg['status'] = 1
    except Exception as e:
        print(e)
        msg['status'] = 0

    return HttpResponse(json.dumps(msg, ensure_ascii=False))

from blog import fileTree

def async(request):
    if 'uname' in request.session:
        uid = request.GET.get("uid", None)
        user = models.UserInfo.objects.filter(pk=uid)[0]
        return render(request, 'async.html', {'userinfo': get_user_info_data(user)})
    else:
        return redirect('../')

def list_dir(request):
    p = request.POST.get('fpath', None)
    type = request.POST.get('type', None)

    return HttpResponse(fileTree.list_dir(p, type))

def readFile(request):
    fpath = request.POST.get('fpath', None)
    return HttpResponse(fileTree.readFile(fpath))

def videoPlay(request):
    if 'uname' in request.session:
        uid = request.GET.get("uid", None)
        user = models.UserInfo.objects.filter(pk=uid)[0]
        ret_article = models.Article.objects.filter(user_id=uid)[:18]
        return render(request, 'videoPlay.html', {'userinfo': get_user_info_data(user), 'articles':ret_article})
    else:
        return redirect('../')

def getVideoFilePlayUrl(request):

    ret = {'status':0, 'playUrl':None,'vTrueName':None, 'vExtName':None}
    path = request.GET.get('path', None)
    try:
        if path:
            fpath, fname = os.path.split(path)  # 获取文件路径，和文件名
            shotname, extension = os.path.splitext(fname)  # 获取文件名 和 文件扩展名
            playUrl = path

            if settings.VIDEO_BASE_HOST_NAME:
                playUrl = settings.VIDEO_BASE_HOST_NAME + '/' + fname

            ret['status'] = 1
            ret['playUrl'] = playUrl
            ret['vTrueName'] = fname
            ret['vExtName'] = extension
        else:
            ret['status'] = 0
    except Exception as e:
        ret['status'] = 0

    return HttpResponse(json.dumps(ret, ensure_ascii=False))

from django.db.models import Max,Avg,F,Q,Min,Count,Sum

def bookMark(request, opration, pk):
    if 'uname' in request.session:
        if opration == 'p':
            uid = request.GET.get("uid", None)
            user = models.UserInfo.objects.filter(pk=uid)[0]
            ret_article = models.Article.objects.filter(user_id=uid)[:10]

            book_mark_classify_ret = models.BookMarkClassify.objects.filter(user_id=uid)
            ret_classify_count = models.BookMark.objects.filter(user_id=uid).values('classify').annotate(classifyCount=Count('pk'))
            ret_mark_classify = []

            allBookMarkCount = 0

            for markClassify in book_mark_classify_ret:
                count = 0
                for item in ret_classify_count:
                    classifyid = item['classify']
                    if classifyid == markClassify.id:
                        count = item['classifyCount']

                allBookMarkCount += count
                obj = {'id':markClassify.id, 'name':markClassify.name, 'count':count}

                ret_mark_classify.append(obj)
            return render(request, 'bookMark.html', {'userinfo': get_user_info_data(user), 'articles': ret_article, 'bookMarkClassifyRet': ret_mark_classify, 'allBookMarkCount':allBookMarkCount})

        elif opration == 'add':
            ret = addBookMark(request, pk)

        elif opration == 'edit':
            ret = editBookMark(request, pk)

        elif opration == 'del':
            ret = delBookMark(request, pk)

        elif opration.find('loadMoreBookMark-') > -1:
            l = opration.split('-')
            pageSize = l[1]
            currentPageNum = l[2]
            classifyid = None
            if len(l) > 3:
                classifyid = l[3]

            ret = loadMoreBookMark(request, int(pageSize), int(currentPageNum), classifyid)

        return HttpResponse(json.dumps(ret, ensure_ascii=False))
    else:
        return redirect('../')

def delBookMark(request, pk):
    ret = {'status': None, 'bookMark': None, "message": None, 'opration': 'del'}
    uid = request.POST.get('uid', None)
    try:
        models.BookMark.objects.filter(pk=pk, user_id=uid).delete()
        ret['status'] = 1
        ret['bookMark'] = pk
        ret['message'] = '书签已删除'
    except Exception as e:
        print(e)
        ret['status'] = 0
        ret['message'] = '书签删除失败'

    return ret


def editBookMark(request, pk):
    ret = {'status': None, 'bookMark': None, "message": None, 'opration': 'edit'}
    try:
        title = request.POST.get('des', None)
        location = request.POST.get('url', None)
        new_classifyId = request.POST.get('classifyId', None)
        uid = request.POST.get('uid', None)

        # if int(classifyId) < 0:
        #     obj = models.BookMark.objects.raw("UPDATE blog_bookmark SET title='"+title+"', location='"+location+"', classify_id=null WHERE id="+pk)#filter().update(title=title, location=location, classify_id=-1)
        #
        # else:
        #     models.BookMark.objects.filter(pk=pk).update(title=title, location=location, classify_id=classifyId)

        old_classify_id = models.BookMark.objects.filter(pk=pk, user_id=uid).values('classify_id').first()['classify_id']
        models.BookMark.objects.filter(pk=pk, user_id=uid).update(title=title, location=location, classify_id=new_classifyId)
        ret['status'] = 1
        ret['bookMark'] = {'des':title, 'localtion':location, 'newClassifyId':new_classifyId ,'oldClassifyId':old_classify_id, 'bookMarkPk':pk}
        ret['message'] = '书签已更新'
    except Exception as e:
        print(e)
        ret['status'] = 0
        ret['message'] = '书签更新失败'

    return ret

def loadMoreBookMark(request, pageSize, currentPageNum, classifyid):

    ret = {'status':None, 'currentPageNum': None, 'bookMarks':None, 'message':None, 'opration':'loadMoreBookMark', 'classifyid':None}

    uid = request.POST.get('uid')
    try:
        start_index = currentPageNum * pageSize
        end_index = (currentPageNum + 1) * pageSize

        if classifyid and classifyid != 'all':
            ret_bookmark = models.BookMark.objects.all().filter(classify_id=int(classifyid), user_id=uid)[start_index:end_index]
        else:
            ret_bookmark = models.BookMark.objects.all().filter(user_id=uid)[start_index:end_index]

        ret_bookMark = serializers.serialize('json', ret_bookmark, use_natural_foreign_keys=True)

        ret['status'] = 1
        ret['message'] = 'OK'
        ret['currentPageNum'] = currentPageNum + 1
        ret['bookMarks'] = ret_bookMark
        ret['classifyid'] = classifyid

    except Exception as e:
        print(e)
        ret['status'] = 0
        ret['message'] = 'load book mark failed！'

    return ret

def addBookMark(request, pk):
    ret = {'status': None, 'bookMark': None, "message": None, 'opration': 'add'}

    try:
        des = request.POST.get('des')
        url = request.POST.get('url')
        uid = request.POST.get('uid')
        classifyId = request.POST.get('classifyId')
        # if int(classifyId) == -1:
        #     new_book_mark = models.BookMark.objects.create(title=des, location=url, user_id=uid)
        # else:
        #     new_book_mark = models.BookMark.objects.create(title=des, location=url, user_id=uid, classify_id=classifyId)
        new_book_mark = models.BookMark.objects.create(title=des, location=url, user_id=uid, classify_id=classifyId)
        classifyid = None
        if new_book_mark.classify:
            classifyid = new_book_mark.classify.id

        ret['status'] = 1
        ret['bookMark'] = {'pk':new_book_mark.id, 'title': new_book_mark.title, 'location': new_book_mark.location, 'classifyid':classifyid}
        ret['message'] = '数据已更新'
    except Exception:
        ret['status'] = 0
        ret['message'] = '书签添加失败'

    return ret

def bookMarkClassify(request, opration, pk):
    if opration == 'add':
        ret = addBookMarkClassify(request)
    elif opration == 'del':
        ret = delBookMarkClassify(request, pk)
    elif opration == 'update':
        ret = modifyBookMarkClassify(request, pk)

    return HttpResponse(json.dumps(ret, ensure_ascii=False))

def addBookMarkClassify(request):
    ret  = {'status':None, 'classify':None, "message":None, 'opration':'add'}
    name = request.GET.get('name', None)
    uid = request.GET.get('uid', None)
    if not name or not uid:
        ret['status'] = 0
        ret['message'] = '缺少参数'
        return ret

    try:
        obj = models.BookMarkClassify.objects.filter(name=name, user_id=uid)
        if obj:
            ret['status'] = 0
            ret['message'] = '分类名称已存在'
        else:
            try:
                classify = models.BookMarkClassify.objects.create(name=name, user_id=uid)
                ret['status'] = 1
                ret['classify'] = {'name': classify.name, 'id': classify.id}
                ret['message'] = '数据已更新'
            except Exception as e:
                print(e)
                ret['status'] = 0
                ret['message'] = '数据更新失败'
    except Exception as e:
        print(e)
        ret['status'] = 0
        ret['message'] = '数据更新失败'

    return  ret

def delBookMarkClassify(request, pk):
    ret = {'status': None, 'classify': None, "message": None, 'opration': 'del'}

    if not pk:
        ret['status'] = 0
        ret['message'] = '缺少参数'
        return ret
    try:
        obj = models.BookMarkClassify.objects.filter(pk = pk).delete()
        ret['status'] = 1
        ret['classify'] = pk
        ret['message'] = '数据已更新'
    except:
        ret['status'] = 0
        ret['message'] = '数据更新失败'

    return ret

def modifyBookMarkClassify(request, pk):
    ret = {'status': None, 'classify': None, "message": None, 'opration': 'update'}
    name = request.GET.get('name', None)
    if not pk or not name:
        ret['status'] = 0
        ret['message'] = '参数错误'
        return ret
    try:
        obj = models.BookMarkClassify.objects.filter(pk=pk).update(name=name)
        ret['status'] = 1
        ret['classify'] = {'name':name, 'pk':pk}
        ret['message'] = '数据已更新'
    except:
        ret['status'] = 0
        ret['message'] = '数据更新失败'

    return ret

def get_user_info_data(user):
   return {"uid": user.pk, "uname": user.uname, "upwd": user.upwd,
     "headImg_100x100": user.headImg_100x100, "headImg_48x48": user.headImg_48x48,
     "headImg_35x35": user.headImg_35x35, "chickenSoup": user.chickenSoup}
