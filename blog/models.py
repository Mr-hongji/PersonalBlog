from django.db import models

# Create your models here.

class UserInfo(models.Model):
    uname = models.CharField(max_length=18, verbose_name='用户名')
    upwd = models.CharField(max_length=18, verbose_name='密码')
    email = models.CharField(max_length=200, verbose_name="邮箱", default="")
    #img = models.ImageField(verbose_name='用户头像', upload_to='./static/uploadfiles/userHeadImage')
    headImg_100x100 = models.TextField(verbose_name='用户头像 100x100', default="../static/images/defaultUserHead/default_userheag_img_100x100.png")
    headImg_48x48 = models.TextField(verbose_name='用户头像 48x48', default="../static/images/defaultUserHead/default_userheag_img_48x48.png")
    headImg_35x35 = models.TextField(verbose_name='用户头像 35x35', default="../static/images/defaultUserHead/default_userheag_img_35x35.png")
    chickenSoup = models.CharField(max_length=20, verbose_name='鸡汤文', default="")

    class Meta:
        verbose_name_plural = '用户信息'

    def natural_key(self):
        return {'id':self.pk, 'uname':self.uname}

    def __str__(self):
        return self.uname


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    createTime = models.DateTimeField(verbose_name='创建时间', null=True, blank=True, auto_now=True)
    user = models.ForeignKey('UserInfo', verbose_name='用户', on_delete=models.CASCADE)
    classify = models.ForeignKey('Classify', verbose_name='分类', on_delete=models.CASCADE)
    tag = models.ManyToManyField('Tag', verbose_name='标签')
    deleted = models.IntegerField(verbose_name="是否删除标识", default=0)

    class Meta:
        verbose_name_plural = '文章'

    def __str__(self):
        return self.title


class Classify(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey('UserInfo', null=True, on_delete=models.SET_NULL)
    class Meta:
        verbose_name_plural = '分类'

    def natural_key(self):
        return {'id':self.pk, 'name':self.name}

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey('UserInfo', null=True, on_delete=models.SET_NULL)
    class Meta:
        verbose_name_plural = '标签'

    def natural_key(self):
        return {'id':self.pk, 'name':self.name}

    def __str__(self):
        return self.name

class BookMarkClassify(models.Model):
    user = models.ForeignKey('UserInfo', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = '书签分类'

    def natural_key(self):
        return {'id':self.pk, 'name':self.name}

    def __str__(self):
        return self.name

class BookMark(models.Model):
    title = models.CharField(max_length=300)
    location = models.CharField(max_length=500)
    classify = models.ForeignKey('BookMarkClassify', null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey('UserInfo', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = '书签'

    def __str__(self):
        return self.title