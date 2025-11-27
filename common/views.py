# common/views.py
from rest_framework import generics, permissions, viewsets, filters
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

class BaseTokenObtainPairView(TokenObtainPairView):
    """统一JWT令牌返回格式"""
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return Response({
            "code": 0,
            "data": response.data
        })

class BaseRegisterView(generics.CreateAPIView):
    """统一注册逻辑"""
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            'code': 0,
            'data': response.data,
            'message': '注册成功'
        })

class BaseReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    """统一只读视图集的响应格式"""
    filter_backends = [filters.SearchFilter]
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "code": 0,
            "data": serializer.data,
            "message": "获取成功"
        })
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'code': 0,
            'data': serializer.data,
            'message': '获取成功'
        })