from rest_framework import generics, permissions,viewsets, filters
from django.contrib.auth.models import User
from UserManage.models import UserProfile
from UserManage.serializers.UserSerializer import UserSerializer, RegisterSerializer, UserProfileSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from rest_framework.views import APIView
from common.views import BaseTokenObtainPairView, BaseRegisterView, BaseReadOnlyViewSet
from django.contrib.auth import authenticate
from utils.response import api_response

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
                p = getattr(u, 'profile', None)
                if p and p.roles:
                    role = p.roles or role
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


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'code': 0,
            'data': serializer.data,
            'message': '获取成功'
        })

    def update(self, request, *args, **kwargs):
        # 允许部分字段更新（兼容 PUT/PATCH）
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'code': 0,
            'data': serializer.data,
            'message': '更新成功'
        })

    def partial_update(self, request, *args, **kwargs):
        # 显式支持 PATCH，返回统一格式
        kwargs['partial'] = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'code': 0,
            'data': serializer.data,
            'message': '更新成功'
        })

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
        p = getattr(user, 'profile', None)
        if p and p.roles:
            role = p.roles
        return api_response(code=0, message='验证成功', data={'ok': True, 'role': role, 'user_id': user.id})


class IdentifyTypeView(APIView):
    """判断身份类型：根据用户名在用户表中读取 profile.roles"""
    permission_classes = []
    def get(self, request):
        username = request.query_params.get('username')
        if not username:
            return api_response(code=1, message='缺少用户名', data=None)
        u = User.objects.filter(username=username).first()
        if not u:
            return api_response(code=2, message='未找到用户', data={'type': 'unknown'})
        p = getattr(u, 'profile', None)
        t = 'user'
        if p and p.roles:
            t = p.roles
        return api_response(code=0, message='成功', data={'type': t, 'user_id': u.id})
