# -*- coding:utf-8 -*-
from .models import tv_play, tv_video, movie_play, movie_video
from rest_framework import serializers


class TvPlayListSerializer(serializers.ModelSerializer):
    class Meta:
        model = tv_play
        fields = ['title', 'img_url', 'detail_url', 'type', 'region', 'year', 'performer', 'director', 'introduction',
                  'updated_time', 'note', 'id']


class TvVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = tv_video
        fields = ['id', 'title', 'api_from', 'episode', 'player_url', 'tv_play']


class Tvm3u8Serializer(serializers.ModelSerializer):
    class Meta:
        model = tv_video
        fields = ['id', 'video_play']


class MoiveListSerializer(serializers.ModelSerializer):
    class Meta:
        model = movie_play
        fields = ['title', 'img_url', 'detail_url', 'type', 'region', 'year', 'performer', 'director', 'introduction',
                  'updated_time', 'note', 'id']


class MovieVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = movie_video
        fields = ['id', 'title', 'api_from', 'episode', 'player_url', 'movie_play']


class Moviem3u8Serializer(serializers.ModelSerializer):
    class Meta:
        model = movie_video
        fields = ['id', 'video_play']


from drf_haystack.serializers import HaystackSerializer
from .search_indexes import Tvplay_Index, Movieplay_Index


class Tvplay_IndexHaystackSerializer(HaystackSerializer):
    """课程搜索的序列化器"""

    class Meta:
        index_classes = [Tvplay_Index]
        fields = ['text', 'id', 'title', 'img_url', 'note', 'introduction', 'updated_time']

class Movieplay_IndexHaystackSerializer(HaystackSerializer):
    """课程搜索的序列化器"""

    class Meta:
        index_classes = [Movieplay_Index]
        fields = ['text', 'id', 'title', 'img_url', 'note', 'introduction', 'updated_time']
