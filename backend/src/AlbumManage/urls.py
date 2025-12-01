from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.AlbumView import AlbumViewSet, MyAlbumCreateView

router = DefaultRouter()
router.register(r'', AlbumViewSet, basename='album')

urlpatterns = [
    path('', include(router.urls)),
    path('my/create/', MyAlbumCreateView.as_view(), name='my-album-create'),
]
