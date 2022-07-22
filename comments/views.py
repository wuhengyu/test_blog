from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Blog
from .forms import CommentForm


# blog_pk是URL实名参数
def blog_comment(request, blog_pk):
    # get_object_or_404()函数的作用是当要获取的文章（Blog）存在时，则获取该文章
    # 否则返回 404 页面给用户
    blog = get_object_or_404(Blog, pk=blog_pk)
    # HTTP 请求使用最多的是 GET 和 POST 两种
    # 如果是POST 请求，说明是前端页面提交数据
    # 因此当请求为 POST时才需要处理表单数据
    if request.method == 'POST':
        # request.POST是一个字典类型的对象，表单提交的数据也保存在这个对象中
        # 因此可用request.POST给CommentForm对象赋值
        form = CommentForm(request.POST)
        # form.is_valid() 方法检查表单的数据是否符合格式要求
        if form.is_valid():
            # 由于form是ModelFormo类型，可以直接调用save() 方法保存数据到数据库表中
            # commit=False 的作用是生成 Comment 类的实例对象
            # 但不立刻保存数据到数据库表中
            comment = form.save(commit=False)
            # 用户登录后，request.user保存用户的nikename、email等值
            comment.name = request.user.nikename
            comment.email = request.user.email
            # 通过外键关系将评论和被评论的文章关联起来
            comment.blog = blog
            # 真正保存到数据库表中
            comment.save()
            # redirect(blog)调用数据模型Blog的实例对象blog的 get_absolute_url()方法
            # 然后重定向到 get_absolute_url()方法返回的 URL
            return redirect(blog)
        else:
            # 数据校验不通过，需要重新渲染页面
            # 需要传递3个模板变量给 detail.html，文章（blog）、评论列表、表单对象（form）
            comment_list = blog.comment_set.all()
            context = {'blog': blog,
                       'form': form,
                       'comment_list': comment_list
                       }
        return render(request, 'blog/detail.html', context=context)
    # 如果请求方法不是POST，说明是第一次打开页面
    # 重定向到实例对象blog的 get_absolute_url()方法返回的地址
    return redirect(blog)
