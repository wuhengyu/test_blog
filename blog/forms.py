# 导入forms类
from django import forms
# 导入该应用程序的数据模型
from . import models
# 导入出错信息处理模块
from django.core.exceptions import ValidationError


# 定义一个继承Form类的reg_form，这也是一个类
class reg_form(forms.Form):
    """
    定义了username字段类型为Char Field，通过error_message设置对应出错类型的文字提示
    widget设置了字段在页面的表现形式，这里显示为<input>标签
    """
    username = forms.CharField(
        max_length=20,
        label='登录账号',
        error_messages={
            "max_length": "登录账号不能超过20位",
            "required": "登录账号不能为空"
        },
        widget=forms.widgets.TextInput(
            # attrs属性是字典类型，设置"class"为"form-control"，这是Bootstrap样式类
            # 是为了同Bootstrap框架的样式类一致
            attrs={"class": "form-control"},
        )
    )
    # password也是Char Field，通过widget设置
    # 该字段在页面上显示为<input type="password" >标签
    password = forms.CharField(
        min_length=6,
        label='密码',
        error_messages={
            'min_length': '密码最少6位',
            "required": "密码不能为空",
        },
        widget=forms.widgets.PasswordInput(
            attrs={'class': 'form-control'},
            # 当render_value=True，表单数据校验不通过，重新返回页面时
            # 这个字段输入值还存在，没有在页面刷新过程中被清空
            render_value=True,
        )
    )
    # 增加一个repassword字段，让用户在输入密码进行两次输入，保证注册密码正确
    repassword = forms.CharField(
        min_length=6,
        label='确认密码',
        error_messages={
            'min_length': '密码最少6位',
            "required": "密码不能为空",
        },
        widget=forms.widgets.PasswordInput(
            attrs={'class': 'form-control'},
            render_value=True,
        )
    )
    nikename = forms.CharField(
        max_length=20,
        required=False,
        label='姓名',
        error_messages={
            'max_length': '姓名长度不能超过20位',
        },
        # 如果不输入nikename字段值，默认值为“无名氏”
        initial='无名氏',
        widget=forms.widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    # 设em
    # 设email为Email Field类型，实际上还是字符类型，但增加了邮箱的格式校验功能
    email = forms.EmailField(
        label='邮箱',
        error_messages={
            'invalid': '邮箱格式不对',
            'required': '邮箱不能为空',
        },
        widget=forms.widgets.EmailInput(
            attrs={'class': 'form-control', }
        )
    )
    telephone = forms.CharField(label='电话号码', required=False, error_messages={
        'max_length': '最大长度不超过11位', }, widget=forms.widgets.TextInput(attrs={'class': 'form-control'}
                                                                      )
                                )
    # head_img为Image Field类型，在页面生成<input type="file">标签
    head_img = forms.ImageField(label='头像', widget=forms.widgets.FileInput(
        # 在attrs中设置style为display:none是为了在页面中不显示这个标签
        attrs={'style': "display: none"}
    )
                                )
    """
    定义一个校验字段的函数，校验字段函数命名是有规则的，形式：clean_字段名()
    这个函数保证username值不重复
    """

    def clean_username(self):
        # 取得字段值，clean_data保存着通过第一步is_vaild()校验的各字段值，是字典类型
        # 因此要用get()函数取值
        uname = self.cleaned_data.get('username')
        # 从数据库表中查询是否有同名的记录
        vexist = models.loguser.objects.filter(username=uname)
        if vexist:
            # 如果有同名记录，增加一条错误信息给该字段的errors属性
            self.add_error('username', ValidationError('登录账号已存在!'))
        else:
            return uname

    # 定义一个校验程序，判断两次输入的密码是否一致
    def clean_repassword(self):
        passwd = self.cleaned_data.get('password')
        repasswd = self.cleaned_data.get('repassword')
        # print(repasswd)
        if repasswd and repasswd != passwd:
            self.add_error('repassword', ValidationError('两次输入的密码不一致'))
            # raise Validation Error('两次密码不一致')
        else:
            return repasswd
