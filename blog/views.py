from django.shortcuts import render, HttpResponse
from blog import models
from django.core import serializers

import json
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
    return render(request, 'articleEdit.html')

def getClassify():
    classify_ret = models.Classify.objects.all()
    return classify_ret

def getTag():
    tag_ret = models.Tag.objects.all()
    return tag_ret

def addArticleClassify(request):
    msg = {'action':'updateArticleClassify', 'msg':None, 'status':None}
    classify_name = request.GET.get('value')
    classify_id = request.GET.get('id', None)

    if(classify_id):
       return updateArticleClassify(classify_id,classify_name )

    try:
        re = models.Classify.objects.create(name=classify_name)
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

    if (tag_id):
        return updateArticleTag(tag_id, tag_name)
    try:
        re = models.Tag.objects.create(name=tag_name)
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
    return render(request, 'async.html')

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