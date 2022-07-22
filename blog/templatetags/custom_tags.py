# 导入 template 这个模块
from django import template
# 导入用到的数据模型，由于models文件存放在本文件的上一级目录，所以在models前加上..
from ..models import Blog, Category, Tag
# 导入聚合模块相关函数
from django.db.models.aggregates import Count

# 实例化了一个 template.Library 类，是固定写法
register = template.Library()


# 将函数get_new_blogs() 装饰为 register.simple_tag
# 这样就可以在模板文件中使用 {% get_new_blogs %} 调用这个函数
@register.simple_tag
def get_new_blogs(num=5):
    # 通过Django ORM查询语句返回最新的5篇文章
    # 通过按created_time字段倒序和切片操作实现
    return Blog.objects.all().order_by('-created_time')[:num]


@register.simple_tag
def archives():
    # dates()函数返回一个列表，列表中的文章的创建时间精确到月份，降序排列（order='DESC'）
    return Blog.objects.dates('created_time', 'month', order='DESC')


@register.simple_tag
def get_categories():
    # 通过Django分类聚合函数统计每个分类中的文章的数量，并过滤掉没有文章的分类
    return Category.objects.annotate(num_blogs=Count('blog')).filter(num_blogs__gt=0)


@register.simple_tag
def get_tags():
    # 通过Django分类聚合函数统计每个标签中的文章的数量，并过滤掉没有文章的标签
    return Tag.objects.annotate(num_blogs=Count('blog')).filter(num_blogs__gt=0)
