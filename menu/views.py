from django.shortcuts import render

from rest_framework.generics import ListAPIView
from .models import cartoon_menu, player_list,cartoon_detail
from .serializers import CartoonMenusSerializer, PlayerListSeriallizer,CartoonDetailSerializer
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .filters import CartoonMenuFilter,MenuPageNumberPagination



class CartoonMenuView(ListAPIView):
    queryset = cartoon_menu.objects.filter(is_show=True)
    serializer_class = CartoonMenusSerializer
    pagination_class = MenuPageNumberPagination
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = CartoonMenuFilter


# class CartoonDetailView(ListAPIView):
#     queryset = cartoon_detail.objects.all()
#     serializer_class = CartoonDetailSerializer
#     filter_backends = [DjangoFilterBackend]

class PlayerListView(ListAPIView):
    queryset = player_list.objects
    serializer_class = PlayerListSeriallizer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = ['cartoon_menu','id',]

from drf_haystack.viewsets import HaystackViewSet
from drf_haystack.filters import HaystackFilter
from .serializers import CartoonMenuIndexHaystackSerializer

class SearchViewset(HaystackViewSet):
    index_models = [cartoon_menu]
    serializer_class = CartoonMenuIndexHaystackSerializer
    filter_backends = [OrderingFilter,HaystackFilter]
    ordering_fields = ('id','orders','updated_time')
    pagination_class = MenuPageNumberPagination