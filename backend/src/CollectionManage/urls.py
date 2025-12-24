from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.CollectionView import (
    MyCollectionListsView,
    MyCollectionListDeleteView,
    MyCollectionListSongsView,
    MyCollectionListSongDeleteView,
    MyAlbumCollectView,
    MyAlbumCollectDeleteView,
    MyArtistFollowView,
    MyArtistFollowDeleteView,
)

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('my/lists/', MyCollectionListsView.as_view(), name='my-collection-lists'),
    path('my/lists/<int:list_id>/', MyCollectionListDeleteView.as_view(), name='my-collection-list-delete'),
    path('my/lists/<int:list_id>/songs/', MyCollectionListSongsView.as_view(), name='my-collection-list-songs'),
    path('my/lists/<int:list_id>/songs/<int:song_id>/', MyCollectionListSongDeleteView.as_view(), name='my-collection-list-song-delete'),
    path('my/albums/', MyAlbumCollectView.as_view(), name='my-album-collect'),
    path('my/albums/<int:album_id>/', MyAlbumCollectDeleteView.as_view(), name='my-album-collect-delete'),
    path('my/artists/', MyArtistFollowView.as_view(), name='my-artist-follow'),
    path('my/artists/<int:artist_id>/', MyArtistFollowDeleteView.as_view(), name='my-artist-follow-delete'),
]
