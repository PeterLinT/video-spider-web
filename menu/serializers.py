# -*- coding:utf-8 -*-
from rest_framework import serializers
from .models import cartoon_menu, cartoon_detail, player_list


from drf_haystack.serializers import HaystackSerializer
from .search_indexes import cartoon_menu_Index


class  CartoonMenuIndexHaystackSerializer(HaystackSerializer):
    """课程搜索的序列化器"""
    class Meta:
        index_classes = [cartoon_menu_Index]
        fields = ['text','id', 'title', 'img_url', 'note','cartoon_detail','updated_time']


class CartoonDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = cartoon_detail
        fields = ['id', 'name', 'years', 'country', 'tag', 'introduction']

class CartoonMenusSerializer(serializers.ModelSerializer):
    cartoon_detail = CartoonDetailSerializer()
    class Meta:
        model = cartoon_menu
        fields = ['id', 'title', 'img_url', 'note','cartoon_detail','updated_time']


class PlayerListSeriallizer(serializers.ModelSerializer):

    class Meta:
        model = player_list
        fields = ['id','episode','m3u8_url','cartoon_menu']
