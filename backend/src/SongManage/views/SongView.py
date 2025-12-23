from rest_framework import viewsets, filters, serializers, permissions
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os
from SongManage.models import Song
from common.views import BaseReadOnlyViewSet
from utils.response import api_response
from ArtistManage.models import Artist
from AlbumManage.models import Album
from django.utils.dateparse import parse_date
from django.db import connection, transaction, IntegrityError

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'

class SongViewSet(BaseReadOnlyViewSet):
    queryset = Song.objects.none()
    serializer_class = SongSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=title']
    def list(self, request, *args, **kwargs):
        search = request.query_params.get('search')
        sql = (
            "SELECT song_id, title, artist_name, album_id, duration, release_date, play_count, audio_url "
            "FROM song "
            "JOIN artist ON song.artist_id = artist.artist_id"
        )
        params = []
        if search:
            sql += " WHERE title LIKE %s"
            params.append(f"%{search}%")
        sql += " ORDER BY release_date DESC"
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            rows = cursor.fetchall()

        data = [
            {
                'song_id': r[0],
                'title': r[1],
                'artist_name': r[2],
                'album_id': r[3],
                'duration': r[4],
                'release_date': r[5],
                'play_count': r[6],
                'audio_url': r[7],
            }
            for r in rows
        ]
        return api_response(data=data)


class MySongListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        artist_id = None
        with connection.cursor() as cursor:
            cursor.execute("SELECT artist_id FROM user_become_artist WHERE user_id=%s", [request.user.id])
            row = cursor.fetchone()
            if row:
                artist_id = row[0]
        
        if not artist_id:
             return api_response(code=1, message='仅歌手可查看发布列表', data=None)

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT song_id, title, album_id, duration, release_date, play_count, audio_url, artist_name "
                "FROM song "
                "JOIN artist ON song.artist_id = artist.artist_id "
                "WHERE song.artist_id=%s ORDER BY release_date DESC",
                [artist_id]
            )
            rows = cursor.fetchall()
        
        data = []
        for r in rows:
            album_title = None
            if r[2]: # album_id
                with connection.cursor() as cursor:
                    cursor.execute("SELECT album_name FROM album WHERE album_id=%s", [r[2]])
                    arow = cursor.fetchone()
                    if arow:
                        album_title = arow[0]

            data.append({
                'song_id': r[0],
                'title': r[1],
                'album_id': r[2],
                'album_title': album_title,
                'duration': r[3],
                'release_date': r[4],
                'play_count': r[5],
                'audio_url': r[6],
                'artist_name': r[7],
            })
        
        return api_response(data=data)


class MySongCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        # 检查用户是否是歌手 (通过 user_become_artist 表)
        artist_id = None
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT artist_id FROM user_become_artist WHERE user_id=%s", 
                [request.user.id]
            )
            row = cursor.fetchone()
            if row:
                artist_id = row[0]
        
        if not artist_id:
             return api_response(code=1, message='仅歌手可创建歌曲', data=None)

        title = request.data.get('title')
        album_id = request.data.get('album_id')
        duration = request.data.get('duration')
        release_date = request.data.get('release_date')
        
        # 获取上传的文件
        audio_file = request.FILES.get('audio_file')

        if not title or not artist_id or not duration or not release_date or not audio_file:
            return api_response(code=2, message='缺少参数 (需包含 audio_file, title, duration, release_date) 或 无法识别歌手身份', data=None)
        
        # 保存文件
        file_path = os.path.join('songs', audio_file.name)
        # 如果文件名重复，default_storage 会自动重命名
        saved_path = default_storage.save(file_path, ContentFile(audio_file.read()))
        # 生成 URL
        audio_url = os.path.join(settings.MEDIA_URL, saved_path).replace('\\', '/')

        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM artist WHERE artist_id=%s", [artist_id])
            arow = cursor.fetchone()
        if not arow:
            return api_response(code=3, message='歌手不存在', data=None)
        date = parse_date(release_date)
        if not date:
            return api_response(code=4, message='日期格式错误', data=None)
        if album_id:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1 FROM album WHERE album_id=%s", [album_id])
                albrow = cursor.fetchone()
            if not albrow:
                return api_response(code=5, message='专辑不存在', data=None)
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO song (title, artist_id, album_id, duration, release_date, audio_url, play_count) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                [title, artist_id, album_id, int(duration), str(date), audio_url, 0],
            )
            new_id = cursor.lastrowid
            if not new_id:
                cursor.execute(
                    "SELECT song_id FROM song WHERE title=%s AND artist_id=%s ORDER BY song_id DESC LIMIT 1",
                    [title, artist_id],
                )
                r = cursor.fetchone()
                new_id = r[0] if r else None
        return api_response(message='创建成功', data={'id': new_id, 'title': title, 'url': audio_url})

class MySongUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def patch(self, request, pk):
        artist_id = None
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT artist_id FROM user_become_artist WHERE user_id=%s", 
                [request.user.id]
            )
            row = cursor.fetchone()
            if row:
                artist_id = row[0]
        if not artist_id:
             return api_response(code=1, message='仅歌手可操作', data=None)
        
        # 验证歌曲归属
        with connection.cursor() as cursor:
            cursor.execute("SELECT artist_id FROM song WHERE song_id=%s", [pk])
            row = cursor.fetchone()
            if not row:
                return api_response(code=404, message='歌曲不存在', data=None)
            if row[0] != artist_id:
                return api_response(code=403, message='无权修改此歌曲', data=None)

        # 更新字段 (目前主要支持 album_id)
        album_id = request.data.get('album_id')
        # 注意: album_id 可能为 None (移出专辑)
        # request.data.get('album_id') 如果 key 不存在是 None，如果 key 存在且值为 null 也是 None (在 DRF/JSON 中)
        # 为了区分 "不更新" 和 "更新为 None"，我们可以检查 key 是否存在
        
        has_album_change = 'album_id' in request.data
        
        if has_album_change:
            # 验证 album_id 是否合法 (如果是 None 则跳过验证)
            if album_id is not None:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT album_artist_id FROM album WHERE album_id=%s", [album_id])
                    arow = cursor.fetchone()
                    if not arow:
                         return api_response(code=2, message='专辑不存在', data=None)
                    if arow[0] != artist_id:
                         return api_response(code=3, message='不能添加到其他歌手的专辑', data=None)
            
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE song SET album_id=%s, update_time=CURRENT_TIMESTAMP WHERE song_id=%s",
                    [album_id, pk]
                )
        
        return api_response(message='更新成功', data=None)

class MySongDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, pk):
        artist_id = None
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT artist_id FROM user_become_artist WHERE user_id=%s", 
                [request.user.id]
            )
            row = cursor.fetchone()
            if row:
                artist_id = row[0]
        if not artist_id:
             return api_response(code=1, message='仅歌手可操作', data=None)
             
        with connection.cursor() as cursor:
            cursor.execute("SELECT artist_id FROM song WHERE song_id=%s", [pk])
            row = cursor.fetchone()
            if not row:
                return api_response(code=404, message='歌曲不存在', data=None)
            if row[0] != artist_id:
                return api_response(code=403, message='无权删除此歌曲', data=None)
            
            try:
                with transaction.atomic():
                    # 1. 删除关联的收藏记录 (user_song_list_relation)
                    cursor.execute("DELETE FROM user_song_list_relation WHERE SONG_ID=%s", [pk])
                    
                    # 2. 删除歌曲本身
                    cursor.execute("DELETE FROM song WHERE song_id=%s", [pk])
            except IntegrityError as e:
                return api_response(code=500, message=f'数据库完整性错误: {str(e)}', data=None)
            except Exception as e:
                return api_response(code=500, message=f'删除失败: {str(e)}', data=None)
            
        return api_response(message='删除成功', data=None)
