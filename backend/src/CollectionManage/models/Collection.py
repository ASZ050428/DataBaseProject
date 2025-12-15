from django.db import models
from django.contrib.auth.models import User

class CollectionList(models.Model):
    list_id = models.AutoField(primary_key=True, db_column="LIST_ID", verbose_name="表ID")
    list_name = models.CharField(max_length=32, db_column="LIST_NAME", verbose_name="表名")
    create_time = models.DateTimeField(auto_now_add=True, db_column="CREATE_TIME", verbose_name="创建时间")

    class Meta:
        db_table = "user_favourite_songs_list"
        verbose_name = "收藏列表"
        verbose_name_plural = "收藏列表"
