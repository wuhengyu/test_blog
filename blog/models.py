# 数据表Category
# 代码段1
# 数据模型都继承models类，因此必须先导入models类相关的模块
from django.db import models


# 每个数据模型一定要继承 models.Model 类
class Category(models.Model):
    # 设置name为CharField ，并设置max_length参数指定其最大长度
    # verbose_name指定字段的名称
    name = models.CharField(max_length=32, verbose_name='分类名')
    des = models.CharField(max_length=100, verbose_name='备注', null=True)
    """
    在__str__(self)函数中返回（return）的值是这个数据模型类的实例对象表述
    可理解为数据库表的一条记录对象的别名
    如果print()函数的参数为该数据模型对象实例（记录对象）时，会输出值self.name
    Django Admin管理后台默认列表页面的每一条记录，会显示这个函数的返回值self.name
    """

    def __str__(self):
        return self.name

    """
    Meta类封装了一些数据库的信息
    如verbose_name,verbose_name_plural指定Django Admin后台管理中数据库表名的单复数
    db_table可自定义数据库表名，不用默认名称
    Django默认用“app_类”命名数据库表，如blog_category
    index_together 联合索引，unique_together联合唯一索引
    ordering指定默认排序字段
    """

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'


# 数据表Tag
class Tag(models.Model):
    name = models.CharField(max_length=32, verbose_name='标签名')
    des = models.CharField(max_length=100, verbose_name='备注', null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'


# 数据表Blog
# 代码段2
# Django 2.0以上版本开始用djang.urls，如需对URL进行解析，就要导入reverse相关模块
from django.urls import reverse
# 调用富文本编辑相关模块，从富文本编辑器ckeditor_uploader.fields中导入Rich Text Uploading Field
from ckeditor_uploader.fields import RichTextUploadingField
# 导入strip_tags()函数，代码中用这个函数截取字段中的字符串
from django.urls import reverse
from django.utils.html import strip_tags


class Blog(models.Model):
    # 文章标题
    title = models.CharField(max_length=70, verbose_name='文章标题')
    """
    文章正文，文章正文存放大段文本、格式、图片地址等内容，一方面字段长度大
    另一方面需要排版，因此使用了 Rich Text Uploading Field调用富文本编辑器
    这样可以用富文本编辑器进行博客文章的排版
    """
    body = RichTextUploadingField(verbose_name='文本内容')
    # 文章的创建时间，存储时间的字段用 Date Time Field 类型
    created_time = models.DateTimeField(verbose_name='创建时间')
    # 文章的最后一次修改时间，存储时间的字段用 Date Time Field 类型
    modified_time = models.DateTimeField(verbose_name='修改时间')
    """
    excerpt 字段存储文章的摘要
    Char Field类型字段默认不能为空，这里文章摘要可以为空
    因此指定blank=True 就可以允许为空值了
    """
    excerpt = models.CharField(max_length=200, blank=True, verbose_name='文章摘要')
    """
    category是设置博客文章分类的字段，与前面定义的Category是多对一关系
    即多个博客文章记录可归于一个类别
    Foreign Key()中参数Category指定外键关联的数据模型（数据库表）的名称
    on_delete=models.CASCADE指明如果在Category中删除一条记录
    与这条记录有关联的博客记录也被删除
    """
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='分类')
    """
    tags是标签字段，一篇博客文章可以有多个标签，一个标签下可能有多篇博客文章
    因此用 Many To Many Field类型设置多对多的关联关系
    这里标签 tags 指定 blank=True以允许博客文章没有标签
    """
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='标签')
    # author为博客文章作者，文章作者我们用的是loguser表中定义的用户
    # 这里用外键与该表相关联
    author = models.ForeignKey(to='loguser', on_delete=models.CASCADE, verbose_name='作者')
    # 记录博客文章阅读量，起始值设为0
    # 后面代码为这个字段定义一个increase_views()函数，文章每被查看一次，该字段值加1
    views = models.IntegerField(default=0, verbose_name='查看次数')

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    # increase_views()把views 字段的值加1
    # 然后调用 save() 方法将更改后的值保存到数据库，注意self的用法
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    # save()函数是数据模型类的方法，我们重写这个方法是为了自动提取摘要内容
    def save(self, *args, **kwargs):
        # 如果没有填写博客文章的摘要内容
        if not self.excerpt:
            """
            由于博客文章是由富文本编辑器编写的，文件中带有大量HTML标签
            用strip()函数可能会把HTML标签截断
            这样博客文章的摘要在页面显示时，可能会有乱码或不易查看
            strip_tags() 会把字段中的HTML 标签删去，然后在纯文本中截取字符串
            """
            self.excerpt = strip_tags(self.body)[:118]
            # 调用父类的save()方法将数据保存到数据库中
            super(Blog, self).save(*args, **kwargs)
        else:
            # 重写save()必须调用父类的save()方法，否则数据不会保存到数据库
            super(Blog, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        # 设置按created_time的值倒序排列，这样最新的博客文章排在前面
        # 指定倒序需在字段名前加负号
        ordering = ['-created_time']
        verbose_name = '文档管理表'
        verbose_name_plural = '文档管理表'

# 数据表loguser
# 代码段3
from django.db import models
# Django用户认证系统提供了一个内置的 User 对象，我们想通过扩展这个用户以增加新字段，扩展方式可以通过继承Abstract User的方式，所以要导入Abstract User类
from django.contrib.auth.models import AbstractUser


# 建立一个数据模型类loguser，继承Abstract User，就可以生成系统用户
class loguser(AbstractUser):
    # 增加一个nikename字段用来存储用户的名字，我们在博客相关网页上显示这个名字
    nikename = models.CharField(max_length=32, verbose_name="昵称", blank=True)
    # telephone字段限制了最大长度为11位
    telephone = models.CharField(max_length=11, null=True, unique=True)
    """
    head_img存储用户头像，在数据库表中存储的是文件的相对地址
    字段值形式为upload_to的值/filename
    图片文件的实际地址值由settings.py中的MEDIA_ROOT和head_img中的upload_to决定
    地址为/MEDIA_ROOT的值/upload_to的值/filename
    """
    head_img = models.ImageField(upload_to='headimage', blank=True, null=True, verbose_name='头像')  # 头像

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "用户信息表"
        verbose_name_plural = verbose_name
