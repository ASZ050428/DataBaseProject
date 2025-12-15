from rest_framework import generics, permissions,viewsets, filters
from django.contrib.auth.models import User
from UserManage.serializers.UserSerializer import UserSerializer, RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from rest_framework.views import APIView
from common.views import BaseTokenObtainPairView, BaseRegisterView, BaseReadOnlyViewSet
from django.contrib.auth import authenticate
from utils.response import api_response
from django.db import connection

class CustomTokenObtainPairView(BaseTokenObtainPairView):
    def post(self, request, *args, **kwargs):
        base = super().post(request, *args, **kwargs)
        username = request.data.get('username')
        role = 'user'
        user_id = None
        try:
            u = User.objects.filter(username=username).first()
            if u:
                user_id = u.id
                # 检查是否是歌手 (SQL查询关联表)
                with connection.cursor() as cursor:
                    cursor.execute("SELECT 1 FROM user_become_artist WHERE user_id=%s", [user_id])
                    if cursor.fetchone():
                        role = 'artist'
        except Exception:
            pass
        tokens = {}
        if hasattr(base, 'data'):
            tokens = base.data.get('data', {})
        
        flat = {
            'access': tokens.get('access'),
            'refresh': tokens.get('refresh'),
            'role': role,
            'user_id': user_id,
        }
        return api_response(code=0, message='登录成功', data=flat)

class RegisterView(BaseRegisterView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    # 继承基类的create方法，无需重复编写

class UserViewSet(BaseReadOnlyViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    search_fields = ['=username']  # 仅保留子类特有配置

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        # 前端只需丢弃JWT即可，后端可选实现黑名单
        return Response({
            "code": 0,
            "data": None,
            "message": "已注销"
        })
    
class CodeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        return Response({
            "code": 0,
            "data": [],
            "message": "成功"
        })


class VerifyPasswordView(APIView):
    """用户名+密码验证，返回角色与结果"""
    permission_classes = []
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return api_response(code=1, message='缺少用户名或密码', data=None)
        user = authenticate(username=username, password=password)
        if not user:
            return api_response(code=2, message='验证失败', data={'ok': False})
        role = 'user'
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM user_become_artist WHERE user_id=%s", [user.id])
            if cursor.fetchone():
                role = 'artist'
        return api_response(code=0, message='验证成功', data={'ok': True, 'role': role, 'user_id': user.id})


class IdentifyTypeView(APIView):
    """判断身份类型：查询关联表"""
    permission_classes = []
    def get(self, request):
        username = request.query_params.get('username')
        if not username:
            return api_response(code=1, message='缺少用户名', data=None)
        u = User.objects.filter(username=username).first()
        if not u:
            return api_response(code=2, message='未找到用户', data={'type': 'unknown'})
        t = 'user'
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM user_become_artist WHERE user_id=%s", [u.id])
            if cursor.fetchone():
                t = 'artist'
        return api_response(code=0, message='成功', data={'type': t, 'user_id': u.id})
