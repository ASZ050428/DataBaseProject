from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.SongView import SongViewSet, MySongCreateView, MySongUpdateView, MySongDeleteView, MySongListView

router = DefaultRouter()
router.register(r'', SongViewSet, basename='song')

urlpatterns = [
    path('', include(router.urls)),
    path('my/list/', MySongListView.as_view(), name='my-song-list'),
    path('my/create/', MySongCreateView.as_view(), name='my-song-create'),
    path('my/<int:pk>/', MySongUpdateView.as_view(), name='my-song-update'), # PATCH
    path('my/<int:pk>/delete/', MySongDeleteView.as_view(), name='my-song-delete'), # DELETE
]
