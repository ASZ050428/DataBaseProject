from rest_framework import generics, permissions,viewsets, filters
from django.contrib.auth.models import User
from UserManage.models import UserProfile
from UserManage.serializers.UserSerializer import UserSerializer, RegisterSerializer, UserProfileSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from rest_framework.views import APIView
from common.views import BaseTokenObtainPairView, BaseRegisterView, BaseReadOnlyViewSet

class CustomTokenObtainPairView(BaseTokenObtainPairView):
    # 无需重复实现，直接继承基类逻辑
    pass

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
