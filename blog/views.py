from django.shortcuts import render
# 导入/blog/models.py中的数据模型
from . import models
# 导入Django的认证模块，因为代码中要模拟用户登录
from django.contrib.auth.models import auth


def test_ckeditor_front(request):
    # 从loguser中取出第一条记录，loguser继承Abstract User
    # 也就是说loguser中的成员是系统用户，为了测试取出第一条记录
    user_obj = models.loguser.objects.all().first()
    # 通过认证模块让用户处于登录态
    # auth.login(request, user_obj)
    # 取出第一条测试数据
    blog = models.Blog.objects.get(id=1)
    # 把数据传递给页面
    return render(request, 'blog/test_ckeditor_front.html', {'blog': blog})
