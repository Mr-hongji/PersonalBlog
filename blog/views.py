from django.shortcuts import render, HttpResponse
from blog import models

import json
# Create your views here.

def index(request):
    ret = models.Article.objects.all()
    return render(request, 'index.html',{'articles':ret})

def clock(request):
    return render(request, 'clock.html')

def addBlog(request):
    classify_ret = models.Classify.objects.all()
    tag_ret = models.Tag.objects.all()
    return render(request, 'add_blog.html', {'classify_ret':classify_ret, 'tag_ret':tag_ret})

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

        msg['status'] = 1
    except Exception as e:
        print(e)
        msg['status'] = 0
    data = models.Article.objects.create(title=articleTitle, content=articleContent, classify_id=classifyId, user_id=1)
    data.tag.add(*list(map(int, tagIds))) # ['1','2'] 转 [1, 2]

    return HttpResponse(json.dumps(msg, ensure_ascii=False))
