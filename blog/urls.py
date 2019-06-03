from django.urls import path,re_path
from django.urls import include
from blog import views

urlpatterns = [
    path('index.html',views.index),
    path('clock.html', views.clock),
    path('add_blog.html', views.addBlog),
    path('article/<int:pk>', views.article),

    path('addArticleClassify/', views.addArticleClassify),
    path('delArticleClassify/', views.delArticleClassify),
    path('addArticleTag/', views.addArticleTag),
    path('delArticleTag/', views.delArticleTag),
    path('addArticle/', views.addArticle),
    path('getArticles/', views.getArticles),
    path('articleDetails/', views.articleDetails),

]
