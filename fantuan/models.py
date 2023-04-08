import json

from django.db import models
from utils.models import BaseModel
from .aesparse import get_video
# Create your models here.
class tv_play(BaseModel):
    title = models.CharField(max_length=100, null=False, unique=True, verbose_name='电视剧名')
    img_url = models.CharField(max_length=1000, null=False, verbose_name='图片地址')
    note = models.CharField(max_length=100, verbose_name='更新状态')
    detail_url = models.CharField(max_length=1000, verbose_name='详情页面地址')
    type = models.CharField(max_length=100,verbose_name='类型')
    region = models.CharField(max_length=20,verbose_name='地区')
    year = models.CharField(max_length=20,verbose_name='年份')
    performer = models.CharField(max_length=20,verbose_name='演员')
    director = models.CharField(max_length=20,verbose_name='导演')
    introduction = models.CharField(max_length=1000,verbose_name='简介')

    class Meta:
        db_table = "tv_play"
        verbose_name="电视剧列表"
        verbose_name_plural = "电视剧列表"
    def __str__(self):
        return "%s" % self.title



class tv_video(BaseModel):
    title = models.CharField(max_length=100,verbose_name='电视剧名')
    api_from = models.CharField(max_length=10,verbose_name='接口名')

    episode = models.CharField(max_length=10, verbose_name='第几集')
    player_url=models.CharField(max_length=1000, verbose_name='播放地址', null=True,
                                blank=True, unique=True)
    tv_play = models.ForeignKey('tv_play', on_delete=models.CASCADE, null=True,
                                blank=True, verbose_name='电视剧id')

    class Meta:
        db_table = "tv_video"
        verbose_name = "剧集列表"
        verbose_name_plural = "剧集列表"
    def video_play(self):
        return get_video(self.player_url).replace('\t','').replace('\u0005','')

class movie_play(BaseModel):
    title = models.CharField(max_length=100, null=False, unique=True, verbose_name='电影名')
    img_url = models.CharField(max_length=1000, null=False, verbose_name='图片地址')
    note = models.CharField(max_length=100, verbose_name='更新状态')
    detail_url = models.CharField(max_length=1000, verbose_name='详情页面地址')
    type = models.CharField(max_length=100,verbose_name='类型')
    region = models.CharField(max_length=20,verbose_name='地区')
    year = models.CharField(max_length=20,verbose_name='年份')
    performer = models.CharField(max_length=20,verbose_name='演员')
    director = models.CharField(max_length=20,verbose_name='导演')
    introduction = models.CharField(max_length=1000,verbose_name='简介')

    class Meta:
        db_table = "movie_play"
        verbose_name="电影列表"
        verbose_name_plural = "电影列表"
    def __str__(self):
        return "%s" % self.title

class movie_video(BaseModel):
    title = models.CharField(max_length=100,verbose_name='电影名')
    api_from = models.CharField(max_length=10,verbose_name='接口名')

    episode = models.CharField(max_length=10, verbose_name='第几集')
    player_url=models.CharField(max_length=1000, verbose_name='播放地址', null=True,
                                blank=True, unique=True)
    video_url = models.CharField(max_length=1000, verbose_name='m3u8地址', null=True,
                                blank=True)
    movie_play = models.ForeignKey('movie_play', on_delete=models.CASCADE, null=True,
                                blank=True, verbose_name='电影id')

    class Meta:
        db_table = "movie_video"
        verbose_name = "电影列表"
        verbose_name_plural = "电影列表"

    def video_play(self):
        return get_video(self.player_url).replace('\t','').replace('\u0005','')