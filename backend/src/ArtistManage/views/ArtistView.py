from rest_framework import generics, permissions,viewsets, filters
from django.contrib.auth.models import User
from UserManage.serializers.UserSerializer import UserSerializer, RegisterSerializer
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

# 复用基类的JWT令牌视图，无需重复实现
class CustomTokenObtainPairView(BaseTokenObtainPairView):
    pass

# 复用基类的注册逻辑，仅保留 Artist 模块相关配置
class RegisterView(BaseRegisterView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

# 普通用户升级为歌手视图
class UpgradeArtistView(APIView):
    """普通用户升级为歌手"""
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        user = request.user
        name = request.data.get('name') or user.username
        
        # 检查是否已经是歌手 (SQL)
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM user_become_artist WHERE user_id=%s", [user.id])
            if cursor.fetchone():
                return api_response(code=0, message='用户已是歌手', data={'user_id': user.id})
            
        # 获取或创建 Artist
        artist, created = Artist.objects.get_or_create(artist_name=name)
        
        # 创建关联 (SQL)
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO user_become_artist (user_id, artist_id) VALUES (%s, %s)",
                [user.id, artist.artist_id]
            )
        
        return api_response(code=0, message='升级成功', data={'user_id': user.id, 'artist_id': artist.artist_id, 'name': name})

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)  # 复用update逻辑

# 注销视图：保持简洁，仅返回艺术家相关提示
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        return Response({
            "code": 0,
            "data": None,
            "message": "艺术家家账号已注销"
        })

# 验证码视图：保留基础逻辑，可根据艺术家模块需求扩展
class CodeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        # 此处可添加艺术家专属验证码逻辑（如身份验证等）
        return Response({
            "code": 0,
            "data": [],
            "message": "艺术家验证码获取成功"
        })

# 艺术家视图集：继承只读基类，专注于艺术家相关用户查询
class ArtistViewSet(BaseReadOnlyViewSet):  # 类名更贴合模块功能
    queryset = Artist.objects.none()
    serializer_class = UserSerializer # 这里可能需要一个 ArtistSerializer，但暂时先不管
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']

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
                'artist_name': r[1],
                'region': r[2],
                'bio': r[3]
            }
            for r in rows
        ]
        return api_response(data=data)

    # 复写retrieve方法，确保保返回艺术家详情
    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        with connection.cursor() as cursor:
            # 1. 获取歌手基本信息
            cursor.execute("SELECT artist_id, artist_name, region, bio FROM artist WHERE artist_id=%s", [pk])
            row = cursor.fetchone()
            
            if not row:
                 return api_response(code=2, message='未找到歌手', data=None)
            
            artist_info = {
                'id': row[0],
                'artist_name': row[1],
                'region': row[2],
                'bio': row[3]
            }

            # 2. 获取歌手的专辑
            cursor.execute(
                "SELECT album_id, album_name, release_time FROM album WHERE album_artist_id=%s ORDER BY release_time DESC",
                [pk]
            )
            albums = [
                {'album_id': r[0], 'album_name': r[1], 'release_time': r[2]}
                for r in cursor.fetchall()
            ]

            # 3. 获取歌手的歌曲
            cursor.execute(
                "SELECT song_id, title, duration, play_count, audio_url FROM song WHERE artist_id=%s ORDER BY play_count DESC",
                [pk]
            )
            songs = [
                {
                    'song_id': r[0], 
                    'title': r[1], 
                    'duration': r[2], 
                    'play_count': r[3],
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
