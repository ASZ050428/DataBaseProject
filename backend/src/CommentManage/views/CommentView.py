from rest_framework import viewsets, filters, serializers, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from CommentManage.models import Comment
from common.views import BaseReadOnlyViewSet
from utils.response import api_response
from django.contrib.auth.models import User
from django.db import connection
from utils.jwt_required import jwt_required

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

    # 发表新评论
    @jwt_required
    def post(self, request):
        song_id = request.data.get('song_id')
        content = request.data.get('content')
        user_id = request.user_id

        if not song_id or not content:
            return api_response(code=1, message='缺少参数', data=None)
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO comment (user_id, song_id, content, create_time) VALUES (%s, %s, %s, CURRENT_TIMESTAMP)",
                [user_id, song_id, content],
            )
            new_id = cursor.lastrowid
            if not new_id:
                cursor.execute(
                    "SELECT comment_id FROM comment WHERE user_id=%s AND song_id=%s ORDER BY comment_id DESC LIMIT 1",
                    [user_id, song_id],
                )
                row = cursor.fetchone()
                new_id = row[0] if row else None
        return api_response(message='发表成功', data={'id': new_id})


class SongCommentsView(APIView):

    # 获取某首歌的评论列表
    def get(self, request ,song_id):
        with connection.cursor() as cursor:
            # 使用 JOIN 直接查询 username
            cursor.execute(
                """
                SELECT c.comment_id, u.username, c.content, c.create_time 
                FROM comment c
                JOIN users u ON c.user_id = u.user_id
                WHERE c.song_id=%s 
                ORDER BY c.create_time DESC
                """,
                [song_id],
            )
            rows = cursor.fetchall()
            
        data = [{ 'id': r[0], 'username': r[1], 'content': r[2], 'create_time': r[3] } for r in rows]
        return api_response(data=data)


class MyCommentDeleteView(APIView):

    # 删除自己的评论
    @jwt_required
    def delete(self, request, comment_id: int):
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM comment WHERE comment_id=%s AND user_id=%s",
                [comment_id, request.user_id],
            )
            affected = cursor.rowcount
        if affected == 0:
            return api_response(code=2, message='未找到评论', data=None)
        return api_response(message='删除成功', data=None)
