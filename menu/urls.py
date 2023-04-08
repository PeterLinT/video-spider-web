# -*- coding:utf-8 -*-
from django.urls import path,re_path
from rest_framework import routers

from . import views
router = routers.DefaultRouter()
# 注册全文搜索到视图集中生成url路由信息
router.register("search", views.SearchViewset, basename="Search")
urlpatterns = [
    path('',views.CartoonMenuView.as_view()),
    path("player/",views.PlayerListView.as_view()),
    # path('/detail/', views.CartoonDetailView.as_view())

] + router.urls