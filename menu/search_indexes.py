# -*- coding:utf-8 -*-
from haystack import indexes
from .models import cartoon_menu


class cartoon_menu_Index(indexes.SearchIndex, indexes.Indexable):
    # 下面要搜索哪些数据配置就行了

    # 全文索引[可以根据配置，可以包括多个字段索引]
    # document=True 表示当前字段为全文索引
    # use_template=True 表示接下来haystack需要加载一个固定路径的html模板文件，此模板文件里让text与其他索引字段绑定映射关系（看下面会有设置）
    text = indexes.CharField(document=True, use_template=True)
    id = indexes.IntegerField(model_attr="id")
    title = indexes.CharField(model_attr='title')
    img_url = indexes.CharField(model_attr='img_url')
    note = indexes.CharField(model_attr='note')
    href = indexes.CharField(model_attr='href')
    cartoon_detail = indexes.CharField(model_attr='cartoon_detail')
    updated_time = indexes.DateTimeField(model_attr='updated_time')
    # 普通索引[单字段，只能提供单个字段值的搜索，所以此处的声明更主要是为了提供给上面的text全文索引使用的]
    # 格式：es索引名 = indexes.索引数据类型(model_attr="ORM中的字段名")



    # 指定与当前es索引模型对接的mysql的ORM模型
    def get_model(self):
        return cartoon_menu


    # 当用户搜索es索引的文档信息时，对应的提供给客户端的mysql数据集有哪些？
    # 基于index_queryset 操作elasticsearch 拿到索引 通过索引来这里查
    def index_queryset(self, using=None):
        return self.get_model().objects.filter(is_deleted=False, is_show=True)