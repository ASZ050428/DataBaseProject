from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.AlbumView import AlbumViewSet, MyAlbumCreateView, MyAlbumDeleteView, MyAlbumListView

router = DefaultRouter()
router.register(r'', AlbumViewSet, basename='album')

urlpatterns = [
    path('', include(router.urls)),
    path('my/list/', MyAlbumListView.as_view(), name='my-album-list'),
    path('my/create/', MyAlbumCreateView.as_view(), name='my-album-create'),
    path('my/<int:pk>/delete/', MyAlbumDeleteView.as_view(), name='my-album-delete'),
]
