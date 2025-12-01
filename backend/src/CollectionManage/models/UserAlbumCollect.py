from django.db import models
from django.contrib.auth.models import User
from AlbumManage.models import Album

class UserAlbumCollect(models.Model):
    user_id = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        db_column="user_id",
        verbose_name="用户ID"
    )
    album_id = models.ForeignKey(
        Album, 
        on_delete=models.CASCADE, 
        db_column="album_id",
        verbose_name="专辑ID"
    )
    collect_time = models.DateTimeField(auto_now_add=True, verbose_name="收藏时间")

    class Meta:
        db_table = "user_album_collect"
        verbose_name = "用户专辑收藏"
        verbose_name_plural = "用户专辑收藏"
        unique_together = ("user_id", "album_id")  # 组合主键
