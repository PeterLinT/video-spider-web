# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from fantuan import models
from scrapy_djangoitem import DjangoItem

class GetTvItem(DjangoItem):
    # define the fields for your item here like:
    # name = scrapy.Field()
    django_model = models.tv_play

class Getm3u8Item(DjangoItem):
    # define the fields for your item here like:
    # name = scrapy.Field()
    django_model = models.tv_video

class GetMovieItem(DjangoItem):
    # define the fields for your item here like:
    # name = scrapy.Field()
    django_model = models.movie_play

class moviem3u8Item(DjangoItem):
    # define the fields for your item here like:
    # name = scrapy.Field()
    django_model = models.movie_video