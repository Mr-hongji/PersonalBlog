from django.db import models

# Create your models here.

class UserInfo(models.Model):

    uname = models.CharField(max_length=18, verbose_name='用户名')
    upwd = models.CharField(max_length=18, verbose_name='密码')
    img = models.ImageField(verbose_name='用户头像', upload_to='./static/uploadfiles/userHeadImage')
    chickenSoup = models.CharField(max_length=20, verbose_name='鸡汤文')

    class Meta:
        verbose_name_plural = '用户信息'


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='标题')
    summery = models.CharField(max_length=1000, verbose_name='简介')
    content = models.TextField(verbose_name='内容')
    createTime = models.DateTimeField(verbose_name='创建时间', null=True, blank=True, auto_now=True)
    user = models.ForeignKey('UserInfo', verbose_name='用户', on_delete=models.PROTECT)
    classify = models.ForeignKey('Classify', verbose_name='分类', on_delete=models.PROTECT)
    tag = models.ForeignKey('Tag', verbose_name='标签', on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = '文章'


class Classify(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = '分类'

class Tag(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = '标签'