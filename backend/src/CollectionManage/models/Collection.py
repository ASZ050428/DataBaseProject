from django.db import models
from django.contrib.auth.models import User

class CollectionList(models.Model):
    list_id = models.AutoField(primary_key=True, verbose_name="表ID")
    list_name = models.CharField(max_length=100, verbose_name="表名")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    user_id = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        db_column="user_id",
        related_name="collection_lists",
        verbose_name="用户ID"
    )

    class Meta:
        db_table = "collection_list"
        verbose_name = "收藏列表"
        verbose_name_plural = "收藏列表"
