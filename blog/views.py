from django.shortcuts import render, HttpResponse
from blog import models
from django.core import serializers
import os, shutil, json, time
from PersonalBlog import settings
# Create your views here.

def index(request):
    ret_user = models.UserInfo.objects.all()

    return render(request, 'index.html',{'userinfo':ret_user, 'classify':getClassify(), 'tag':getTag()})

def article(request, pk):
    ret_user = models.UserInfo.objects.all()

    return render(request, 'article.html', {'userinfo': ret_user, 'classify': getClassify(), 'tag': getTag()})

def postedit(request):
    ret = {'status': None, 'article': None, 'classify': None, 'tag': None}
    pk = request.GET.get('pk', None)
    ret_classify = getClassify()
    ret_tag = getTag()
    ret['classify'] = serializers.serialize('json', ret_classify)
    ret['tag'] = serializers.serialize('json', ret_tag)
    ret['status'] = 1

    if pk:
        ret_article = models.Article.objects.all().filter(pk=int(pk))
        ret['article'] = serializers.serialize('json', ret_article, use_natural_foreign_keys=True)
        return HttpResponse(json.dumps(ret))
    else:
        return HttpResponse(json.dumps(ret));

def getArticles(request, type, pk):
    pgnum = int(request.GET.get('pgnum', 0))
    pageSize = 10
    ret = {'pgnum': pgnum+1,'type':type, 'id':pk, 'data':None}
    start_index = pgnum * pageSize
    end_index = pgnum * pageSize + pageSize

    if type == 'all':
        ret_article = models.Article.objects.all()[start_index:end_index]
    elif type == 'classify':
        ret_article = models.Article.objects.all().filter(classify_id = pk)[start_index:end_index]
    elif type == 'tag':
        ret_article = models.Article.objects.all().filter(tag__id=pk)[start_index:end_index]

    json_data = serializers.serialize('json', ret_article, use_natural_foreign_keys=True)
    print(json_data)
    ret['data'] = json_data
    return HttpResponse(json.dumps(ret))


def articleDetails(request):
    pk = request.GET.get('pk')
    ret = models.Article.objects.all().filter(pk=int(pk))
    return HttpResponse(serializers.serialize('json', ret, use_natural_foreign_keys=True))

def clock(request):
    return render(request, 'clock.html')

def articleEditPage(request, pk):
    ret_user = models.UserInfo.objects.all()
    return render(request, 'articleEdit.html', {'userinfo': ret_user})

def getClassify():
    classify_ret = models.Classify.objects.all()
    return classify_ret

def getTag():
    tag_ret = models.Tag.objects.all()
    return tag_ret

def addArticleClassify(request):
    msg = {'action':'addArticleClassify', 'msg':None, 'status':None}
    classify_name = request.GET.get('value')
    classify_id = request.GET.get('id', None)
    uid = request.GET.get('uid', None)

    if(classify_id):
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

        if pk:
            article = models.Article.objects.filter(pk=int(pk))
            article.update(title=articleTitle, content=articleContent, classify_id=classifyId, user_id=1)
            article.first().tag.set(list(map(int, tagIds)))
        else:
            article = models.Article.objects.create(title=articleTitle, content=articleContent, classify_id=classifyId)
            article.tag.add(*list(map(int, tagIds)))  # ['1','2'] 转 [1, 2]
        msg['status'] = 1
    except Exception as e:
        print(e)
        msg['status'] = 0

    return HttpResponse(json.dumps(msg, ensure_ascii=False))

from blog import fileTree

def async(request):
    ret_user = models.UserInfo.objects.all()
    return render(request, 'async.html', {'userinfo': ret_user})

def list_dir(request):
    p = request.POST.get('fpath', None)
    type = request.POST.get('type', None)

    return HttpResponse(fileTree.list_dir(p, type))

def readFile(request):
    fpath = request.POST.get('fpath', None)
    return HttpResponse(fileTree.readFile(fpath))


def videoPlay(request):
    ret_user = models.UserInfo.objects.all()
    ret_article = models.Article.objects.all()[:18]
    return render(request, 'videoPlay.html', {'userinfo': ret_user, 'articles':ret_article})

def getVideoUrl(request):

    ret = {'status':0, 'vPath':None,'vTrueName':None, 'vExtName':None}
    path = request.POST.get('path', None)
    if path:
        fpath, fname = os.path.split(path) # 获取文件路径，和文件名
        shotname, extension = os.path.splitext(fname) # 获取文件名 和 文件扩展名
        fsize = os.path.getsize(path)
        print(fsize)
        tempFileUrl= os.path.join(settings.BASE_DIR, '1') + '/112233' + extension
        #shutil.copyfile(path, tempFileUrl)
        #newfsize = os.path.getsize(tempFileUrl)

        ret['status'] = 1
        ret['vPath'] = '/static/112233' + extension
        ret['vTrueName'] = fname
        ret['vExtName'] = extension


    return HttpResponse(json.dumps(ret, ensure_ascii=False))

from django.db.models import Max,Avg,F,Q,Min,Count,Sum

def bookMark(request, opration, pk):
    if opration == 'p':
        ret_user = models.UserInfo.objects.all()
        ret_article = models.Article.objects.all()[:10]

        book_mark_classify_ret = models.BookMarkClassify.objects.all()
        ret_classify_count = models.BookMark.objects.values('classify').annotate(classifyCount=Count('pk'))
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
        return render(request, 'bookMark.html', {'userinfo': ret_user, 'articles': ret_article, 'bookMarkClassifyRet': ret_mark_classify, 'allBookMarkCount':allBookMarkCount})

    elif opration == 'add':
        ret = addBookMark(request, pk)

    elif opration == 'edit':
        ret = editBookMark(request, pk)

    elif opration == 'del':
        delBookMark(request, pk)

    elif opration.find('loadMoreBookMark-') > -1:
        l = opration.split('-')
        pageSize = l[1]
        currentPageNum = l[2]
        classifyid = None
        if len(l) > 3:
            classifyid = l[3]

        ret = loadMoreBookMark(request, int(pageSize), int(currentPageNum), classifyid)

    return HttpResponse(json.dumps(ret, ensure_ascii=False))

def delBookMark(request, pk):
    ret = {'status': None, 'bookMark': None, "message": None, 'opration': 'edit'}
    try:
        models.BookMark.objects.filter(pk=pk).delete()
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

        # if int(classifyId) < 0:
        #     obj = models.BookMark.objects.raw("UPDATE blog_bookmark SET title='"+title+"', location='"+location+"', classify_id=null WHERE id="+pk)#filter().update(title=title, location=location, classify_id=-1)
        #
        # else:
        #     models.BookMark.objects.filter(pk=pk).update(title=title, location=location, classify_id=classifyId)

        old_classify_id = models.BookMark.objects.filter(pk=pk).values('classify_id').first()['classify_id']
        models.BookMark.objects.filter(pk=pk).update(title=title, location=location, classify_id=new_classifyId)
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
    try:
        start_index = currentPageNum * pageSize
        end_index = (currentPageNum + 1) * pageSize

        if classifyid and classifyid != 'all':
            ret_bookmark = models.BookMark.objects.all().filter(classify_id=int(classifyid))[start_index:end_index]
        else:
            ret_bookmark = models.BookMark.objects.all()[start_index:end_index]

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
        obj = models.BookMarkClassify.objects.get(name=name)
        ret['status'] = 0
        ret['message'] = '分类名称已存在'
    except:
        try:
            classify = models.BookMarkClassify.objects.create(name=name, user_id=uid)
            ret['status'] = 1
            ret['classify'] = {'name': classify.name, 'id': classify.id}
            ret['message'] = '数据已更新'
        except:
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