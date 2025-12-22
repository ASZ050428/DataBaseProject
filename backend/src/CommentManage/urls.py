from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.CommentView import (
    CommentViewSet,
    MyCommentView,
    SongCommentsView,
    MyCommentDeleteView,
)

router = DefaultRouter()
router.register(r'', CommentViewSet, basename='comment')

urlpatterns = [
    path('my/', MyCommentView.as_view(), name='my-comments'),
    path('by-song/<int:song_id>/', SongCommentsView.as_view(), name='comments-by-song'),
    path('my/<int:comment_id>/', MyCommentDeleteView.as_view(), name='my-comment-delete'),
    path('', include(router.urls)),
]
