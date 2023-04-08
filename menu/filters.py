# -*- coding:utf-8 -*-
from django_filters.rest_framework import FilterSet
import django_filters
from rest_framework.pagination import PageNumberPagination

from .models import cartoon_menu

class CartoonMenuFilter(FilterSet):
    """
    title 过滤器 用作全局模糊搜索
    """
    title = django_filters.CharFilter(field_name='title',lookup_expr='icontains')
    id = django_filters.NumberFilter(field_name='id',lookup_expr='exact')
    class Meta:
        models = cartoon_menu
        fieids = ['title','id']


class MenuPageNumberPagination(PageNumberPagination):
    # page_query_param = "" # 地址上面代表页码的变量名，默认为page
    page_size = 50  # 每一页显示的数据量，没有设置页码，则不进行分页
    # 允许客户端通过指定的参数名来设置每一页数据量的大小，默认是size
    page_size_query_param = "size"
    max_page_size = 50  # 限制每一页最大展示的数据量
