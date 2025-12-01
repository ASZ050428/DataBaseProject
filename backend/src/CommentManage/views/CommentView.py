from rest_framework import viewsets, filters, serializers, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from CommentManage.models import Comment
from common.views import BaseReadOnlyViewSet
from utils.response import api_response
from django.contrib.auth.models import User
from django.db import connection

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
        sql = "SELECT comment_id, song_id, content, create_time FROM comment WHERE user_id=%s"
        params = [request.user.id]
        if song_id:
            sql += " AND song_id=%s"
            params.append(song_id)
        sql += " ORDER BY create_time DESC"
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            rows = cursor.fetchall()
        data = [{ 'id': r[0], 'song_id': r[1], 'content': r[2], 'create_time': r[3] } for r in rows]
        return api_response(data=data)
    def post(self, request):
        song_id = request.data.get('song_id')
        content = request.data.get('content')
        if not song_id or not content:
            return api_response(code=1, message='缺少参数', data=None)
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO comment (user_id, song_id, content, create_time, update_time, is_deleted) VALUES (%s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 0)",
                [request.user.id, song_id, content],
            )
            new_id = cursor.lastrowid
            if not new_id:
                cursor.execute(
                    "SELECT comment_id FROM comment WHERE user_id=%s AND song_id=%s ORDER BY comment_id DESC LIMIT 1",
                    [request.user.id, song_id],
                )
                row = cursor.fetchone()
                new_id = row[0] if row else None
        return api_response(message='发表成功', data={'id': new_id})


class SongCommentsView(APIView):
    permission_classes = []
    def get(self, request, song_id: int):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT comment_id, user_id, content, create_time FROM comment WHERE song_id=%s ORDER BY create_time DESC",
                [song_id],
            )
            rows = cursor.fetchall()
        data = [{ 'id': r[0], 'user_id': r[1], 'content': r[2], 'create_time': r[3] } for r in rows]
        return api_response(data=data)


class MyCommentDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, comment_id: int):
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM comment WHERE comment_id=%s AND user_id=%s",
                [comment_id, request.user.id],
            )
            affected = cursor.rowcount
        if affected == 0:
            return api_response(code=2, message='未找到评论', data=None)
        return api_response(message='删除成功', data=None)
