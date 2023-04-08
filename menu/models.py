import json

from django.db import models
from utils.models import BaseModel


# Create your models here.
class cartoon_menu(BaseModel):
    title = models.CharField(max_length=100, null=False, unique=True, verbose_name='动漫名称')
    img_url = models.CharField(max_length=1000, null=False, verbose_name='图片地址')
    note = models.CharField(max_length=100, verbose_name='更新状态')
    href = models.CharField(max_length=1000, verbose_name='详情页面')
    cartoon_detail = models.ForeignKey('cartoon_detail', on_delete=models.CASCADE, null=True, blank=True,
                                       related_name='cartoondetail', verbose_name='动漫详情')

    class Meta:
        db_table = "cartoon_menu"
        verbose_name = "动漫目录"
        verbose_name_plural = "动漫目录"

    def __str__(self):
        return "%s" % self.title




class cartoon_detail(BaseModel):
    cartoon_menu = models.ForeignKey('cartoon_menu', on_delete=models.CASCADE, verbose_name='动漫目录', null=True,
                                     blank=True, related_name='cartoonmenu')
    name = models.CharField(max_length=50, verbose_name='动漫名称')
    years = models.CharField(max_length=10, verbose_name='发行年份')
    country = models.CharField(max_length=10, verbose_name='发行国家')
    tag = models.CharField(max_length=50, verbose_name='动漫标签')
    introduction = models.CharField(max_length=1000, verbose_name='动漫简介')

    class Meta:
        db_table = "cartoon_detail"
        verbose_name = "动漫详情"
        verbose_name_plural = "动漫详情"

    def __str__(self):
        return "%s" % self.name


class player_list(BaseModel):
    cartoon_menu = models.ForeignKey('cartoon_menu', on_delete=models.CASCADE, null=True,
                                     blank=True, verbose_name='动漫')
    name = models.CharField(max_length=100, default='', null=True, blank=True)
    episode = models.CharField(max_length=10, verbose_name='第几集')
    player_url = models.CharField(max_length=1000, verbose_name='播放地址')
    m3u8_url = models.CharField(max_length=1000, verbose_name='m3u8地址', null=True,
                                blank=True,unique=True )

    class Meta:
        db_table = "player_list"
        verbose_name = "播放列表"
        verbose_name_plural = "播放列表"

    def __str__(self):
        return "%s" % self.name
    @property
    def newepisode(self):
        return int(self.episode.replace('第','').replace('集',''))

