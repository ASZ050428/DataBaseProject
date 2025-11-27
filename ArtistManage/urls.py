from django.urls import path
from rest_framework.routers import DefaultRouter
from .views.ArtistView import ArtistViewSet  

router = DefaultRouter()
router.register(r'', ArtistViewSet, basename='artist')  # 歌手相关接口

urlpatterns = [
    # 仅保留歌手模块自身的接口
    path('detail/<int:pk>/', ArtistViewSet.as_view({'get': 'retrieve'}), name='artist-detail'),
    path('search/', ArtistViewSet.as_view({'get': 'search'}), name='artist-search'),
] + router.urls