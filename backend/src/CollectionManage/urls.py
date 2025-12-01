from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.CollectionView import (
    CollectionListViewSet,
    CollectionListSongIncludeViewSet,
    UserAlbumCollectViewSet,
    UserSingerFollowViewSet,
    SingerSongPublishViewSet,
    MyCollectionListsView,
    MyCollectionListDeleteView,
    MyCollectionListSongsView,
    MyCollectionListSongDeleteView,
    MyAlbumCollectView,
    MyAlbumCollectDeleteView,
    MySingerFollowView,
    MySingerFollowDeleteView,
    MyPublishSongLinkView,
)

router = DefaultRouter()
router.register(r'list', CollectionListViewSet, basename='collection-list')
router.register(r'list-song', CollectionListSongIncludeViewSet, basename='collection-list-song')
router.register(r'user-album', UserAlbumCollectViewSet, basename='user-album-collect')
router.register(r'user-singer', UserSingerFollowViewSet, basename='user-singer-follow')
router.register(r'singer-song', SingerSongPublishViewSet, basename='singer-song-publish')

urlpatterns = [
    path('', include(router.urls)),
    path('my/lists/', MyCollectionListsView.as_view(), name='my-collection-lists'),
    path('my/lists/<int:list_id>/', MyCollectionListDeleteView.as_view(), name='my-collection-list-delete'),
    path('my/lists/<int:list_id>/songs/', MyCollectionListSongsView.as_view(), name='my-collection-list-songs'),
    path('my/lists/<int:list_id>/songs/<int:song_id>/', MyCollectionListSongDeleteView.as_view(), name='my-collection-list-song-delete'),
    path('my/albums/', MyAlbumCollectView.as_view(), name='my-album-collect'),
    path('my/albums/<int:album_id>/', MyAlbumCollectDeleteView.as_view(), name='my-album-collect-delete'),
    path('my/artists/', MySingerFollowView.as_view(), name='my-singer-follow'),
    path('my/artists/<int:singer_id>/', MySingerFollowDeleteView.as_view(), name='my-singer-follow-delete'),
    path('my/publish-song/', MyPublishSongLinkView.as_view(), name='my-publish-song-link'),
]
