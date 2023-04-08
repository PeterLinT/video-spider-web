# -*- coding:utf-8 -*-
from rest_framework import routers
from django.urls import path
from . import views
router = routers.DefaultRouter()
# 注册全文搜索到视图集中生成url路由信息
router.register("search", views.TVSearchViewset, basename="TVSearch")
router.register("movie/search", views.MVSearchViewset, basename="MVSearch")

urlpatterns = [
    path('',views.fantuanMenuView.as_view()),
    path('player/',views.fantuanVideoView.as_view()),
    path('player/m3u8',views.fantuanm3u8View.as_view()),
    path('movie/',views.fantuanMovieMenuView.as_view()),
    path('movie/list',views.fantuanMovieVideoView.as_view()),
    path('movie/list/m3u8',views.fantuanMoviem3u8View.as_view()),

]+ router.urls