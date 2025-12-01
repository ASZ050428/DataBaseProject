from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.SongView import SongViewSet, MySongCreateView

router = DefaultRouter()
router.register(r'', SongViewSet, basename='song')

urlpatterns = [
    path('', include(router.urls)),
    path('my/create/', MySongCreateView.as_view(), name='my-song-create'),
]
