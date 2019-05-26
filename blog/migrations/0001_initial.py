# Generated by Django 2.1.8 on 2019-05-25 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='标题')),
                ('summery', models.CharField(max_length=1000, verbose_name='简介')),
                ('content', models.TextField(verbose_name='内容')),
                ('createTime', models.DateTimeField(auto_now=True, null=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name_plural': '文章',
            },
        ),
        migrations.CreateModel(
            name='Classify',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': '分类',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': '标签',
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uname', models.CharField(max_length=18, verbose_name='用户名')),
                ('upwd', models.CharField(max_length=18, verbose_name='密码')),
                ('img', models.ImageField(upload_to='./static/uploadfiles/userHeadImage', verbose_name='用户头像')),
                ('chickenSoup', models.CharField(max_length=20, verbose_name='鸡汤文')),
            ],
            options={
                'verbose_name_plural': '用户信息',
            },
        ),
        migrations.AddField(
            model_name='article',
            name='classify',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='blog.Classify', verbose_name='分类'),
        ),
        migrations.AddField(
            model_name='article',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='blog.Tag', verbose_name='标签'),
        ),
        migrations.AddField(
            model_name='article',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='blog.UserInfo', verbose_name='用户'),
        ),
    ]
