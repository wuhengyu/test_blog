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
    auth.login(request, user_obj)
    # 取出第一条测试数据
    blog = models.Blog.objects.get(id=1)
    # 把数据传递给页面
    return render(request, 'blog/test_ckeditor_front.html', {'blog': blog})


from django.shortcuts import redirect
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
