# 导入haystack中的相关模块indexes
from haystack import indexes
# 导入数据模型
from .models import Blog

"""
建立索引类名，名字规定，为“modelname Index”形式,其中modelname是数据模型名
要为哪个数据模型建立索引类就用哪个数据模型名
类必须继承indexes.Search Index、indexes.Indexable
"""


class BlogIndex(indexes.SearchIndex, indexes.Indexable):
    """
    use_template = True允许我们使用数据模板去建立搜索引擎要用到的索引文件
    数据模板的路径形式一般为templates/search/indexes/yourapp/modelname_text.txt
    templates是在settings.py中设定的模板文件目录
    yourapp指的是要检索数据的应用程序
    modelname_text.txt中的modelname指的是要检索数据的数据模型
    """
    text = indexes.CharField(document=True, use_template=True)

    # 重写get_model()方法，返回相应的数据模型，这个方法必须有
    def get_model(self):
        return Blog

    # 重写index_queryset()方法，返回数据模型需要检索的记录
    def index_queryset(self, using=None):
        return self.get_model().objects.all()
