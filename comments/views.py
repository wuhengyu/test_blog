from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Blog
from .forms import CommentForm


# blog_pk是URL实名参数
def blog_comment(request, blog_pk):
    # get_object_or_404()函数的作用是当要获取的文章（Blog）存在时，则获取该文章
    # 否则返回 404 页面给用户
    blog = get_object_or_404(Blog, pk=blog_pk)
    # HTTP 请求使用最多的是 GET 和 POST 两种
