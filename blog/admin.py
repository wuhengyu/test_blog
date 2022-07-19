# 导入admin模块，这个模块封装了Django Admin的后台管理功能，包括register()
from django.contrib import admin
# 导入建立的数据模型
from .models import Blog, Category, Tag, loguser


# 定义一个自定义数据显示管理模型类，要继承Model Admin类
class BlogAdmin(admin.ModelAdmin):
    # 定义了管理后台列表页面上显示的字段
    list_display = ("title", "created_time", "modified_time", "category", "author", "views",)


# 注册loguser，没有自定义管理模型类，将按Django Admin后台默认页面样式进行管理
admin.site.register(loguser)

# 注册博客，有第二个参数，按照BlogAdmin定义进行管理
admin.site.register(Blog, BlogAdmin)

# 注册Category，默认样式管理
admin.site.register(Category)

# 注册Tag，默认样式管理
admin.site.register(Tag)
