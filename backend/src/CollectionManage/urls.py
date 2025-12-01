from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.CollectionView import (
    CollectionListViewSet,
    CollectionListSongIncludeViewSet,
    UserAlbumCollectViewSet,
    UserSingerFollowViewSet,
    SingerSongPublishViewSet,
)

router = DefaultRouter()
router.register(r'list', CollectionListViewSet, basename='collection-list')
router.register(r'list-song', CollectionListSongIncludeViewSet, basename='collection-list-song')
router.register(r'user-album', UserAlbumCollectViewSet, basename='user-album-collect')
router.register(r'user-singer', UserSingerFollowViewSet, basename='user-singer-follow')
router.register(r'singer-song', SingerSongPublishViewSet, basename='singer-song-publish')

urlpatterns = [
    path('', include(router.urls)),
]
