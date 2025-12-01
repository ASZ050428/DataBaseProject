from rest_framework import viewsets, filters, serializers
from CommentManage.models import Comment
from common.views import BaseReadOnlyViewSet

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class CommentViewSet(BaseReadOnlyViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=content']
