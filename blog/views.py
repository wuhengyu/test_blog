from django.shortcuts import render, redirect
# 导入/blog/models.py中的数据模型
from . import models
# 导入Django的认证模块，因为代码中要模拟用户登录
from django.contrib.auth.models import auth


def test_ckeditor_front(request):
    # 从loguser中取出第一条记录，loguser继承Abstract User
    # 也就是说loguser中的成员是系统用户，为了测试取出第一条记录
    user_obj = models.loguser.objects.all().first()
    # 通过认证模块让用户处于登录态
    auth.login(request, user_obj)
    # 取出第一条测试数据
    blog = models.Blog.objects.get(id=1)
    # 把数据传递给页面
    return render(request, 'blog/test_ckeditor_front.html', {'blog': blog})


# 导入forms模块（文件），文件中定义了reg_form()
from . import forms


# 定义视图函数
def registe(request):
    if request.method == "POST":
        # 因为有图片上传，所以以下代码是错误的
        # form_obj = forms.reg_form(request.POST)
        """
        初始化reg_form的一般字段都包含在request.POST中
        文件、图片字段中包含上传功能的字段不在request.POST中保存
        而是保存在request.FILES中，所以在以下代码中添加request.FILES参数
        """
        form_obj = forms.reg_form(request.POST, request.FILES)
        # 判断校验是否通过
        if form_obj.is_valid():
            form_obj.cleaned_data.pop("repassword")
            """
            通过Django ORM语句新建一条记录，由于数据模型继承于Abstract User类
            可以用create_user()建立一个系统用户
            form_obj是reg_form类实例对象，它的cleaned_data是字典类型
            **form_obj.cleaned_data相当于key1=value1,key2=value2
            通过传递**form_obj.cleaned_data和 is_staff=1,is_superuser=1
            设置新生成的用户是系统用户且是超级用户
            """
            user_obj = models.loguser.objects.create_user(**form_obj.cleaned_data,
                                                          is_staff=1, is_superuser=1)
            # 用户登录，可将登录用户相关信息赋值给request.user
            auth.login(request, user_obj)
            # 根据URL配置，登录成功后转向博客首页
            return redirect('/')
        else:
            return render(request, "blog/registe.html", {"formobj": form_obj})
    # 初始化一个form对象，这个对象是reg_form类的实例对象
    form_obj = forms.reg_form()
    # 向模板blog/registe.html传递参数
    return render(request, "blog/registe.html", {"formobj": form_obj})


def login(request):
    # 请求方式是POST，表明是前端提交数据
    if request.method == "POST":
        # 从前端页面提交过来的数据中提取用户名和密码
        username = request.POST.get("username")
        pwd = request.POST.get("password")
        # 利用auth模块做用户名和密码的校验，也就是用户认证过程
        # 如果不通过，user就是None,也就是空
        user = auth.authenticate(username=username, password=pwd)
        # 校验通过user才有值，user有值说明user对象是系统认证用户
        if user:
            # 用代码设置用户为登录状态，并将登录用户对象赋值给request.user
            # 也就是说user对象存储在request.user中
            # 可以在代码和模板文件中直接调用request.user
            auth.login(request, user)
            # 登录完成后，重定向到博客首页
            return redirect("/")
        else:
            # 如果用户为空，说明认证不通过，给出错误信息，用render()页面传递错误信息
            errormsg = "用户名或密码错误！"
            return render(request, 'blog/login.html', {'error': errormsg})
    # 在请求方式不是POST时，也就是GET时，通过render()打开页面
    return render(request, 'blog/login.html')


def logout(request):
    # 调用认证模块，执行logout()函数，这样会把用户相关的cookie、session清空
    auth.logout(request)
    # 重定向到首页
    return redirect("/")


# 视图采用通用视图，这里采用的是列表形式，要继承ListView，因此要导入相关模块
from django.views.generic import ListView


# 视图indexview继承于ListView通用视图类
class indexview(ListView):
    # 指定数据模型（数据库表），默认取全部记录
    model = models.Blog
    # 指定模块文件的地址与名字
    template_name = 'blog/index.html'
    """
    以下语句指定传递给模板文件的模板变量名
    这个模板变量blog_list保存着model指定的数据模型的记录集合
    也就是model与context_object_name这个属性有关联
    """
    context_object_name = 'blog_list'
    # 设置每页显示的记录数
    paginate_by = 10

    # 重写get_context_data()方法
    def get_context_data(self, **kwargs):
        """
        在普通视图函数中将模板变量传递给模板
        通过给 render() 函数向模板文件传递一个字典来实现
        例如 render(request, 'blog/index.html', context={'Blog_list':blog_list})
        或者 render(request, 'blog/index.html', {'Blog_list':blog_list})
        在通用类视图中，如果不是获取数据模型的全部记录
        需要重写 get_context_data()方法，获得条件过滤后的记录
        注意本视图的代码并没有对数据库表记录进行条件过滤
        这里的目的是利用父类的get_context_data()方法返回值中有关分页的数值
        利用这些分页相关数值进行自定义分页代码的编写
        在复写该方法时，还可以增加一些自定义的模板变量
        """
        # 　首先获得父类生成的包含模板变量的字典
        context = super().get_context_data(**kwargs)
        """
        父类(List View类)生成的字典(context)中已有paginator、page_obj、is_paginated 这3个键值对
        paginator 是 Paginator 的一个实例
        page_obj 是 Page 的一个实例
        is_ paginated 是一个布尔变量，用于指示是否已分页
        例如，如果规定每页10条记录，而本身只有5条记录
        其实就用不着分页，此时 is_paginated=False
        由于 context 是一个字典，所以调用get()方法从中取出某个键对应的值
        """
        paginator = context.get('paginator')
        pageobj = context.get('page_obj')
        is_paginated = context.get('is_paginated')
        # 设置每页中分页导航条页码标签的个数
        show_pagenumber = 7
        # 调用自定义 get_page_data()方法获得显示分页导航条所需要的数据
        page_data = self.get_page_data(is_paginated, paginator, pageobj, show_pagenumber)
        # 将page_data变量更新到 context 中，注意 page_data 是一个字典
        context.update(page_data)
        # 传递标识值，如果这个值为firsttab，表示显示“首页”链接被选中
        context['tabname'] = 'firsttab'
        # 将更新后的 context 返回，以便 List View 使用这个字典中的模板变量去渲染模板
        # 注意此时 context 字典中已有了显示分页导航条所需的数据
        return context

    # 自定义 get_page_data()方法，返回当前页的前面页码标签的个数以及后面页码标签的个数
    def get_page_data(self, is_pageinated, paginator, pageobj, show_pagenumber):
        # 如果没有分页，返回空字典
        if not is_pageinated:
            return {}
        """
        分页数据由3部分组成
        前面用left存页码，后面用right存页码，中间部分就是当前页pageobj.number
        lefe，right都初始化为空列表
        """
        left = []
        right = []
        # 当前页面数值的获取，得当前请求的页码号
        cur_page = pageobj.number
        # 取出分页中最后的页码
        total = paginator.num_pages
        # 得到显示页数的一半，“//”可以取得两数相除的商的整数部分
        # show_pagenumber是页码标签的个数
        half = show_pagenumber // 2
        # 取出当前页面前面(letf)显示页标签个数，注意range()
        # 如range(start, stop)用法，计数从 start 开始，计数到 stop 结束，但不包括 stop
        for i in range(cur_page - half, cur_page):
            # 数值大于等于1时，才取数值放到left列表中
            if i >= 1:
                left.append(i)
        # 取出当前页面后面(right)显示页标签个数，再次提示注意range()用法
        for i in range(cur_page + 1, cur_page + half + 1):
            # 数值小于等于页数的最大页数时，才取数值放到right列表中
            if i <= total:
                right.append(i)
                page_data = {
                    'left': left,
                    'right': right,
                }
                return page_data


# 导入Detail View类
from django.views.generic import DetailView


# 视图继承于Detail View通用视图类
class blogdetailview(DetailView):
    # 指定数据模型，从中取出一条记录
    model = models.Blog
    # 指定模板文件
    template_name = 'blog/detail.html'
    # 指定传给模板文件的模板变量名
    context_object_name = 'blog'
    # pk_url_kwarg指定取得一条记录的主键值，pk是指配置项中的URL表达式中的参数名
    # 可以理解为获取主键值等于URL表达式中参数pk值的数据记录
    pk_url_kwarg = 'pk'

    # 重写父类get_object()方法，常用于返回定制的数据记录
    def get_object(self, queryset=None):
        blog = super(blogdetailview, self).get_object(queryset=None)
        blog.increase_views()
        return blog

    # 重写get_context_data()方法，常用于增加数据模板变量
    def get_context_data(self, **kwargs):
        return 0


# 视图继承于List View类
class categoryview(ListView):
    # 设置数据模型，指定数据取自Blog，默认取全部记录
    model = models.Blog
    # 指定模板文件
    template_name = 'blog/index.html'
    # 指定传递给模板文件的参数名
    context_object_name = 'blog_list'

    def get_queryset(self):
        cate = get_object_or_404(models.Category, pk=self.kwargs.get('pk'))
        # 继承父类的get_queryset()方法，并通过filter()函数对记录进行过滤
        # 通过order_by()进行排序
        return super(categoryview, self).get_queryset().filter(category=cate).order_by('-created_time')


# 视图继承于List View类
class tagview(ListView):
    model = models.Blog
    template_name = 'blog/index.html'
    context_object_name = 'blog_list'

    def get_queryset(self):
        tag = get_object_or_404(models.Tag, pk=self.kwargs.get('pk'))
        return super(tagview, self).get_queryset().filter(tags=tag).order_by('created_time')


from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from . import models
# 导入Comment Form表单
from comments1.forms import CommentForm
from django.views.generic import ListView, DetailView


class blogdetailview(DetailView):
    # 指定数据模型
    model = models.Blog
    # 指定模板文件
    template_name = 'blog/detail.html'
    # 指定模板变量名
    context_object_name = 'blog'
    # 指定主键，'pk'为配置文件中的URL参数名
    pk_url_kwarg = 'pk'

    # 重写父类的get_object()方法，这个方法可以返回主键等于URL参数值的记录对象
    # 可以进一步对这个记录对象进行操作，如调用该对象的方法
    def get_object(self, queryset=None):
        # 调用父类get_object()取得一条记录，主键等于URL参数pk的值
        blog = super(blogdetailview, self).get_object(queryset=None)
        # 调用这条记录对象的increase_views()方法，把views字段值加1
        blog.increase_views()
        return blog

    def get_context_data(self, **kwargs):
        # 通过调用父类方法得到一个包含模板变量的字典
        context = super(blogdetailview, self).get_context_data(**kwargs)
        # 初始化Commetn Form表单
        form = CommentForm()
        # 取得本条记录对象的所有评论
        comment_list = self.object.comment_set.all()
        # 在模板变量字典中加入新的字典项
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context
