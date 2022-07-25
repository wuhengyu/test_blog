# -*- coding: utf-8 -*-
# @Time    : 2022/7/17 23:00
# @Author  : Walter
# @File    : urls.py
# @License : (C)Copyright Walter
# @Desc    :

from django.urls import path, re_path
from .views import *

app_name = 'blog'

urlpatterns = [
    # 加入一个URL配置项
    path('test_ckeditor_front/', test_ckeditor_front),
    # 加入登录URL与视图函数的关系
    path('login/', login, name='login'),
    # 用户注册的URL配置项
    path('registe/', registe, name='registe'),
    # 注销的URL配置项
    path('logout/', logout, name='logout'),
    path('indexview/', indexview.as_view(), name='index'),

    re_path(r'^category/(?P<pk>[0-9]+)/', categoryview.as_view(), name='category'),

    re_path('blog/(?P<pk>[0-9]+)/', blogdetailview.as_view(), name='detail')
]
