from rest_framework import generics, permissions,viewsets, filters
from UserManage.serializers.UserSerializer import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.response import api_response
from ArtistManage.models import Artist
from common.views import ( 
    BaseTokenObtainPairView,
    BaseRegisterView,
    BaseReadOnlyViewSet
)
from django.db import connection
from utils.jwt_required import jwt_required


# 普通用户升级为歌手视图
class UpgradeArtistView(APIView):
    # 用户升级为歌手
    @jwt_required
    def post(self, request):
        # 获取新创建的歌手名
        user_id = request.user_id
        name = request.data.get('name')
        if not name:
            name = None
            with connection.cursor() as cursor:
                cursor.execute("SELECT username FROM users WHERE user_id=%s", [user_id])
                row = cursor.fetchone()
                if row:
                    name = row[0]

        # 检查用户是否已是歌手
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM user_become_artist WHERE user_id=%s", [user_id])
            if cursor.fetchone():
                return api_response(code=0, message='用户已是歌手', data={'user_id': user_id})
        # 创建新歌手记录
        with connection.cursor() as cursor:
            # 检查歌手名是否已存在
            cursor.execute(
                "SELECT 1 FROM artist WHERE artist_name=%s", [name]
            )
            if cursor.fetchone():
                return api_response(code=1, message='歌手名称已存在', data=None)
            
            # 创建歌手
            cursor.execute(
                "INSERT INTO artist (artist_name) VALUES (%s)",
                [name]
            )
            artist_id = cursor.lastrowid
            if not artist_id:
                cursor.execute(
                    "SELECT artist_id FROM artist WHERE artist_name=%s",
                    [name]
                )
                row = cursor.fetchone()
                artist_id = row[0] if row else None

            # 关联用户与歌手
            cursor.execute(
                "INSERT INTO user_become_artist (user_id, artist_id) VALUES (%s, %s)",
                [user_id, artist_id]
            )
        return api_response(code=0, message='升级成功', data={'user_id': user_id, 'artist_id': artist_id, 'name': name})

class ArtistProfileView(APIView):
    
    # 获取用户对应的歌手ID
    def get_artist_id(self, user_id):
        with connection.cursor() as cursor:
            cursor.execute("SELECT artist_id FROM user_become_artist WHERE user_id=%s", [user_id])
            row = cursor.fetchone()
            return row[0] if row else None

    # 获取歌手信息
    @jwt_required
    def get(self, request):
        try:
            artist_id = self.get_artist_id(request.user_id)
            if not artist_id:
                return api_response(code=1, message='您还不是歌手')
            
            with connection.cursor() as cursor:
                cursor.execute("SELECT artist_name, region, bio FROM artist WHERE artist_id=%s", [artist_id])
                row = cursor.fetchone()
                if not row:
                    return api_response(code=1, message='歌手信息不存在')
                
                data = {
                    'name': row[0],
                    'region': row[1],
                    'bio': row[2]
                }
                return api_response(data=data)
        except Exception as e:
            return api_response(code=500, message=f'数据库连接失败: {str(e)}', data=None, status_code=500)

    # 更新歌手信息
    @jwt_required
    def put(self, request):
        artist_id = self.get_artist_id(request.user_id)
        if not artist_id:
            return api_response(code=1, message='您还不是歌手')
        
        name = request.data.get('name')
        region = request.data.get('region')
        bio = request.data.get('bio')

        if not name:
             return api_response(code=1, message='歌手名称不能为空')

        with connection.cursor() as cursor:
            # 检查歌手名称是否已被其他歌手使用
            cursor.execute(
                "SELECT 1 FROM artist WHERE artist_name=%s AND artist_id!=%s",
                [name, artist_id]
            )
            if cursor.fetchone():
                return api_response(code=2, message='歌手名称已存在')
            
            # 更新歌手信息
            cursor.execute(
                "UPDATE artist SET artist_name=%s, region=%s, bio=%s WHERE artist_id=%s",
                [name, region, bio, artist_id]
            )
        
        return api_response(message='更新成功')


class ArtistViewSet(BaseReadOnlyViewSet):

    # 模糊搜索歌手列表
    def list(self, request, *args, **kwargs):
        search = request.query_params.get('search')
        sql = "SELECT artist_id, artist_name, region, bio FROM artist"
        params = []
        if search:
            sql += " WHERE artist_name LIKE %s"
            params.append(f"%{search}%")
        
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            rows = cursor.fetchall()
        
        data = [
            {
                'id': r[0],
                'artist_id': r[0],
                'artist_name': r[1],
                'region': r[2],
                'bio': r[3]
            }
            for r in rows
        ]
        return api_response(data=data)

    # 获取歌手详情
    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        with connection.cursor() as cursor:
            # 获取歌手基本信息
            cursor.execute("SELECT artist_id, artist_name, region, bio FROM artist WHERE artist_id=%s", [pk])
            row = cursor.fetchone()
            
            if not row:
                 return api_response(code=2, message='未找到歌手', data=None)
            
            artist_info = {
                'id': row[0],
                'artist_id': row[0],
                'artist_name': row[1],
                'region': row[2],
                'bio': row[3]
            }

            # 获取歌手的专辑
            cursor.execute(
                "SELECT album_id, album_name, release_time FROM album WHERE album_artist_id=%s ORDER BY release_time DESC",
                [pk]
            )
            albums = [
                {'album_id': r[0], 'album_name': r[1], 'release_time': r[2]}
                for r in cursor.fetchall()
            ]

            # 获取歌手的歌曲
            cursor.execute(
                "SELECT song_id, title, duration, release_date, audio_url FROM song WHERE artist_id=%s ORDER BY release_date DESC",
                [pk]
            )
            songs = [
                {
                    'song_id': r[0], 
                    'title': r[1], 
                    'duration': r[2], 
                    'release_date': r[3],
                    'audio_url': r[4]
                }
                for r in cursor.fetchall()
            ]

        data = {
            **artist_info,
            'albums': albums,
            'songs': songs
        }
        return api_response(data=data)
