from django.urls import path,re_path
from django.urls import include
from blog import views
urlpatterns = [

    path('',views.index),

    path('registUser/',views.registUser),
    path('login/',views.login),
    path('startLogin/',views.startLogin),
    path('clock.html', views.clock),
    re_path(r'articleEdit/', views.articleEditPage),
    re_path(r'delArticle/(?P<pk>\d+)', views.delArticle),
    path('article/<int:uid>/<int:articleid>', views.article),
    path('postedit/', views.postedit),

    path('addArticleClassify/', views.addArticleClassify),
    path('delArticleClassify/', views.delArticleClassify),

    path('addArticleTag/', views.addArticleTag),
    path('delArticleTag/', views.delArticleTag),

    path('addArticle/', views.addArticle),
    re_path(r'articles/(?P<type>\w+)/(?P<pk>\d*)', views.getArticles),
    path('articleDetails/', views.articleDetails),
    path('list_dir/', views.list_dir),
    path('async/', views.async),
    path('readFile/', views.readFile),
    path('videoPlay/', views.videoPlay),
    path('getVideoFilePlayUrl/', views.getVideoFilePlayUrl),

    re_path('bookMark/(?P<opration>[\w\d-]+)/(?P<pk>\d*)', views.bookMark),
    re_path('bookMarkClassify/(?P<opration>\w+)/(?P<pk>\d*)', views.bookMarkClassify),
    re_path('uploadEditorImage/', views.uploadEditorImage),
    re_path('confirmModufyPwd/', views.confirmModufyPwd),
    re_path('sendVerificationCodeToEmail/', views.sendVerificationCodeToEmail),

]

