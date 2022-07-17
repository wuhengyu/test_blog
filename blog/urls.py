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
]
