from rest_framework import viewsets, filters, serializers, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from CommentManage.models import Comment
from common.views import BaseReadOnlyViewSet
from utils.response import api_response
from django.contrib.auth.models import User

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class CommentViewSet(BaseReadOnlyViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=content']


class MyCommentView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        song_id = request.query_params.get('song_id')
        qs = Comment.objects.filter(user=request.user)
        if song_id:
            qs = qs.filter(song_id=song_id)
        data = [
            {
                'id': c.comment_id,
                'song_id': c.song_id,
                'content': c.content,
                'create_time': c.create_time
            } for c in qs.order_by('-create_time')
        ]
        return api_response(data=data)
    def post(self, request):
        song_id = request.data.get('song_id')
        content = request.data.get('content')
        if not song_id or not content:
            return api_response(code=1, message='缺少参数', data=None)
        c = Comment.objects.create(user=request.user, song_id=song_id, content=content)
        return api_response(message='发表成功', data={'id': c.comment_id})


class SongCommentsView(APIView):
    permission_classes = []
    def get(self, request, song_id: int):
        qs = Comment.objects.filter(song_id=song_id).order_by('-create_time')
        data = [
            {
                'id': c.comment_id,
                'user_id': c.user_id,
                'content': c.content,
                'create_time': c.create_time
            } for c in qs
        ]
        return api_response(data=data)


class MyCommentDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, comment_id: int):
        qs = Comment.objects.filter(comment_id=comment_id, user=request.user)
        if not qs.exists():
            return api_response(code=2, message='未找到评论', data=None)
        qs.delete()
        return api_response(message='删除成功', data=None)
