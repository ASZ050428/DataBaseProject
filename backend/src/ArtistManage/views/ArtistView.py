from rest_framework import generics, permissions,viewsets, filters
from django.contrib.auth.models import User
from UserManage.models import UserProfile
from UserManage.serializers.UserSerializer import UserSerializer, RegisterSerializer, UserProfileSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.response import api_response
from ArtistManage.models.Aritist import Artist
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

class ArtistRegisterView(APIView):
    """歌手注册：创建用户账号并标记角色为 artist，同时创建 Artist 记录"""
    permission_classes = []
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        artist_name = request.data.get('name') or username
        if not username or not password:
            return api_response(code=1, message='缺少用户名或密码', data=None)
        if User.objects.filter(username=username).exists():
            return api_response(code=2, message='用户名已存在', data=None)
        user = User.objects.create_user(username=username, password=password)
        # 创建或更新资料角色
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.roles = 'artist'
        profile.save()
        # 创建 Artist 业务实体
        Artist.objects.create(name=artist_name)
        return api_response(code=0, message='歌手注册成功', data={'user_id': user.id, 'username': username})

class UpgradeArtistView(APIView):
    """普通用户升级为歌手（SQL实现）"""
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        user_id = request.user.id
        name = request.data.get('name') or request.user.username
        with connection.cursor() as cursor:
            cursor.execute("SELECT roles FROM user_profile WHERE user_id=%s", [user_id])
            row = cursor.fetchone()
        if row and (row[0] or '') == 'artist':
            return api_response(code=0, message='用户已是歌手', data={'user_id': user_id})
        with connection.cursor() as cursor:
            if row:
                cursor.execute("UPDATE user_profile SET roles='artist' WHERE user_id=%s", [user_id])
            else:
                cursor.execute("INSERT INTO user_profile (user_id, roles) VALUES (%s, 'artist')", [user_id])
        artist_id = None
        with connection.cursor() as cursor:
            cursor.execute("SELECT artist_id FROM artist WHERE name=%s", [name])
            arow = cursor.fetchone()
            if not arow:
                cursor.execute("INSERT INTO artist (name, create_time, update_time) VALUES (%s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)", [name])
                artist_id = cursor.lastrowid
                if not artist_id:
                    cursor.execute("SELECT artist_id FROM artist WHERE name=%s ORDER BY artist_id DESC LIMIT 1", [name])
                    r = cursor.fetchone()
                    artist_id = r[0] if r else None
            else:
                artist_id = arow[0]
        return api_response(code=0, message='升级成功', data={'user_id': user_id, 'artist_id': artist_id, 'name': name})

# 个人资料视图：继承基类逻辑，专注于 Artist 特有的特有处理
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # 确保获取当前登录用户的艺术家资料（若有扩展字段可在此处处理）
        return self.request.user.profile
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'code': 0,
            'data': serializer.data,
            'message': '艺术家资料获取成功'  # 提示信息更贴合业务
        })

    def update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'code': 0,
            'data': serializer.data,
            'message': '艺术家资料更新成功'
        })

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
    queryset = User.objects.all()  # 可根据需求筛选艺术家用户（如通过角色筛选）
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=username', 'profile__realName']  # 支持按用户名和真实姓名搜索

    # 复写retrieve方法，确保保返回艺术家详情
    def retrieve(self, request, *args, **kwargs):
        instance = request.user  # 或根据ID查询指定艺术家
        serializer = self.get_serializer(instance)
        return Response({
            'code': 0,
            'data': serializer.data,
            'message': '艺术家详情获取成功'
        })
