from rest_framework.generics import ListAPIView
from .models import tv_play,tv_video,movie_video,movie_play
from .serializers import TvPlayListSerializer, TvVideoSerializer, Tvm3u8Serializer,MovieVideoSerializer,Moviem3u8Serializer,MoiveListSerializer
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .filter import TvPlayFilter,MenuPageNumberPagination
class fantuanMenuView(ListAPIView):
    queryset = tv_play.objects.filter(is_show=True)
    serializer_class = TvPlayListSerializer
    pagination_class = MenuPageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = TvPlayFilter

class fantuanVideoView(ListAPIView):
    queryset = tv_video.objects.filter(is_show=True)
    serializer_class = TvVideoSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = ['id','tv_play','api_from']

class fantuanm3u8View(ListAPIView):
    queryset = tv_video.objects.filter(is_show=True)
    serializer_class = Tvm3u8Serializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = ['id']


class fantuanMovieMenuView(ListAPIView):
    queryset = movie_play.objects.filter(is_show=True)
    serializer_class = MoiveListSerializer
    pagination_class = MenuPageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = TvPlayFilter

class fantuanMovieVideoView(ListAPIView):
    queryset = movie_video.objects.filter(is_show=True)
    serializer_class = MovieVideoSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = ['id','movie_play']

class fantuanMoviem3u8View(ListAPIView):
    queryset = movie_video.objects.filter(is_show=True)
    serializer_class = Moviem3u8Serializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = ['id']

from drf_haystack.viewsets import HaystackViewSet
from drf_haystack.filters import HaystackFilter
from .serializers import Movieplay_IndexHaystackSerializer, Tvplay_IndexHaystackSerializer

class TVSearchViewset(HaystackViewSet):
    index_models = [tv_play]
    serializer_class = Tvplay_IndexHaystackSerializer
    filter_backends = [OrderingFilter,HaystackFilter]
    ordering_fields = ('id','updated_time')
    pagination_class = MenuPageNumberPagination



class MVSearchViewset(HaystackViewSet):
    index_models = [movie_play]
    serializer_class = Movieplay_IndexHaystackSerializer
    filter_backends = [OrderingFilter,HaystackFilter]
    ordering_fields = ('id','updated_time')
    pagination_class = MenuPageNumberPagination